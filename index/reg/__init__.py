#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )
from lib.backwardcompat import *

import logging
from PySide import QtGui

from .result import reg_error, reg_exception

import models
from lib.items import FileItem


def reg_object(session, Object, object_dict, PARENT=None, style='', brief=None):
    if isinstance(Object, string_types):
        try:
            Object = getattr(models, Object)
        except:
            OBJECT = set_object(object_dict, PARENT, style, brief)
            reg_error(OBJECT, "Модель не найдена: '{0}'!".format(Object), Object, object_dict)
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

    session.add(OBJECT)

    return OBJECT


def reg_object1(session, Object, object_dict, PARENT=None, style='', brief=None):
    if isinstance(Object, string_types):
        try:
            Object = getattr(models, Object)
        except:
            OBJECT = set_object(object_dict, PARENT, style, brief)
            reg_error(OBJECT, "Модель не найдена: '{0}'!".format(Object), Object, object_dict)
            return OBJECT

    object_reg = {}
    object_debug = {}
    for i in object_dict:
        if i in dir(Object):
            object_reg[i] = object_dict[i]
        else:
            object_debug[i] = object_dict[i]

    object_find = {}
    for i in object_reg:
        object_find[i] = object_dict[i]

    try:
        rows = session.query(Object).filter_by(**object_find).all()
#       cond = [getattr(Object, i) == object_find[i] for i in object_find]
#       rows = session.query(Object).filter(*cond).all()
        if rows:
            OBJECT = rows[0]
            l = len(rows)
            if l > 1:
                reg_error(PARENT, "Найдено несколько одинаковых записей ({0})!".format(l), Object, object_find)
            show_object(OBJECT, PARENT, style=style, brief=brief)
            return OBJECT

    except Exception as e:
        reg_exception(PARENT, e, Object, object_find)

    OBJECT = Object(**object_reg)

    # Графика
    if style != None:
        show_object(OBJECT, PARENT, style=style, brief=brief)

        for key, val in object_debug.items():
            key = "_debug_{0}".format(key)
            setattr(OBJECT, key, val)

    session.add(OBJECT)

    return OBJECT


def set_object(OBJECT, PARENT, style='', brief=None):
    if isinstance(OBJECT, string_types):
        OBJECT = dict(name=OBJECT)
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)

    show_object(OBJECT, PARENT, style=style, brief=brief)

    return OBJECT


def set_object1(OBJECT, PARENT, style='', brief=None):
    if isinstance(OBJECT, string_types):
        OBJECT = dict(name=OBJECT)
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


# Не использовать вне этого модуля
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


class aObject(aStr):
    def __init__(self, **kargs):
        for key, val in kargs.items():
            setattr(self, key, val)

    def __unicode__(self):
        return "<Элемент>"
