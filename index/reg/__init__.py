#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging
from PySide import QtGui

from .result import reg_warning, reg_error, reg_exception

import models
from lib.items import DirItem, FileItem


def reg_object(Object, object_dict, PARENT=None, style='', brief=None):
    if isinstance(Object, basestring):
        try:
            Object = getattr(models, Object)
        except:
            OBJECT = set_object(object_dict, PARENT, style, brief)
            reg_error(OBJECT, "Объект не найден: '{0}'!".format(Object), Object, object_dict)
            return OBJECT

    object_reg = {}
    object_debug = {}
    for i in object_dict:
        if i in dir(Object):
            object_reg[i] = object_dict[i]
        else:
            object_debug[i] = object_dict[i]

    OBJECT = Object(**object_reg)

    # Графика
    if style != None:
        show_object(OBJECT, PARENT, style=style, brief=brief)

        for key, val in object_debug.items():
            key = "_debug_{0}".format(key)
            setattr(OBJECT, key, val)

    models.DBSession.add(OBJECT)

    return OBJECT


def reg_object1(Object, object_dict, PARENT=None, style='', brief=None):
    if isinstance(Object, basestring):
        try:
            Object = models.__getattribute__(Object)
        except:
            OBJECT = set_object(object_dict, PARENT, style, brief)
            reg_error(OBJECT, "Объект не найден: '{0}'!".format(Object), Object, object_dict)
            return OBJECT

    object_find = {}
    for i in object_dict:
        if i[0] != '_' and i in dir(Object):
            object_find[i] = object_dict[i]

    try:
        rows = models.DBSession.query(Object).filter_by(**object_find).all()
#       cond = [getattr(Object, i) == object_find[i] for i in object_find]
#       rows = models.DBSession.query(Object).filter(*cond).all()
        if rows:
            OBJECT = rows[0]
            l = len(rows)
            if l > 1:
#               cond_output = [unicode(i) for i in cond]
                reg_error(PARENT, "Найдено несколько одинаковых записей ({0})!".format(l), Object, object_find)
            show_object(OBJECT, PARENT, style=style, brief=brief)
            return OBJECT
    except Exception as e:
        reg_exception(PARENT, e, Object, object_find)

    OBJECT = reg_object(Object, object_dict, PARENT=PARENT, style=style, brief=brief)

    return OBJECT


def set_object(OBJECT, PARENT, style='', brief=None):
    if isinstance(OBJECT, basestring):
        OBJECT = dict(name=OBJECT)
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)

    show_object(OBJECT, PARENT, style=style, brief=brief)

    return OBJECT


def set_object1(OBJECT, PARENT, style='', brief=None):
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)

    tree_item = None
    count = PARENT.tree_item.childCount()
    for i in range(count):
        child = PARENT.tree_item.child(i)
        name = child.text(0)
        if name == OBJECT.name:
            tree_item = child
            break

    if tree_item:
        OBJECT.tree_item = tree_item
    else:
        show_object(OBJECT, PARENT, style=style, brief=brief)

    return OBJECT


def show_object(OBJECT, PARENT, style='', brief=None):
    if isinstance(PARENT, QtGui.QTreeWidget):
        tree_item = PARENT
        style = 'BIE'
    elif PARENT and hasattr(PARENT, 'tree_item'):
        tree_item = PARENT.tree_item
    else:
        logging.warning("Данный элемент не имеет отображения: {0!r}".format(PARENT))
        tree_item = None

    if tree_item:
        if not hasattr(OBJECT, 'name'):
            setattr(OBJECT, 'name', 'noname')
        name = unicode(OBJECT.name)
        OBJECT.tree_item = FileItem(tree_item, name, brief=brief, summary=OBJECT)

        if style:
            OBJECT.tree_item.set_style(style)


class aObject():
    def __init__(self, **kargs):
        for key, val in kargs.items():
            setattr(self, key, val)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "<Элемент>"
