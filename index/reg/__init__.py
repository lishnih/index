#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import logging
from PySide import QtGui

from ..core.backwardcompat import *
from ..core.items import FileItem
from ..core.dump import plain_type
from .result import reg_error, reg_exception


def reg_object(session, Object, object_dict, PARENT=None, style='', brief=None, required=[], plains=[]):
    if session:
        for i in required:
            if i not in object_dict or object_dict[i] is None:
                OBJECT = set_object(object_dict, PARENT, style=style, brief="Объект не сохранён - требуемые поля пусты!")
                return OBJECT

        new = dict((key, val) for (key, val) in plains)
        new.update(object_dict)

        OBJECT = Object(**object_dict)
        session.add(OBJECT)

        # Графика
        if style is not None:
            tree_item = show_object(OBJECT, PARENT, style=style, brief=brief)
            if tree_item:
                OBJECT._dict = object_dict

    else:
        OBJECT = set_object(object_dict, PARENT, style=style)

    return OBJECT


def reg_object1(session, Object, object_dict, PARENT=None, style='', brief=None, required=[], plains=[], override=None, keys=None):
    if session:
        for i in required:
            if i not in object_dict or object_dict[i] is None:
                OBJECT = set_object(object_dict, PARENT, style=style, brief="Объект не сохранён - требуемые поля пусты!")
                return OBJECT

        new = dict((key, val) for (key, val) in plains)
        new.update(object_dict)

        OBJECT = None

        if keys:
            object_find = {}
            for i in keys:
                if isinstance(i, string_types):
                    object_find[i] = object_dict[i]
                else:
                    i1, i2 = i
                    object_find[i1] = object_dict[i2]
        else:
            object_find = {key: value for key, value in object_dict.items() if hasattr(Object, key)}

        try:
            rows = session.query(Object).filter_by(**object_find).all()
    #       cond = [getattr(Object, key) == value for key, value in object_find.items()]
    #       rows = session.query(Object).filter(*cond).all()
            if rows:
                OBJECT = rows[0]

                l = len(rows)
                if l > 1:
                    reg_error(PARENT, "Найдено несколько одинаковых записей ({0})!".format(l), Object, object_find)
                    OBJECT._thesamerecords = l - 1

        except Exception as e:
            reg_exception(PARENT, e, Object, object_dict)

        if not OBJECT:
            OBJECT = Object(**object_dict)
            session.add(OBJECT)

        # Графика
        if style is not None:
            tree_item = show_object(OBJECT, PARENT, style=style, brief=brief)
            if tree_item:
                OBJECT._dict = object_dict

    else:
        OBJECT = set_object(object_dict, PARENT, style=style)

    return OBJECT


def set_object(OBJECT, PARENT, style='', brief=None):
    if isinstance(OBJECT, string_types):
        OBJECT = dict(name=OBJECT)
    if isinstance(OBJECT, dict):
        OBJECT = aObject(**OBJECT)
#       if not brief:
#           brief = OBJECT

    show_object(OBJECT, PARENT, style=style+'I', brief=brief)

    return OBJECT


def show_object(OBJECT, PARENT, style='', brief=None):
    if isinstance(PARENT, QtGui.QTreeWidget):
        tree_item = PARENT
        style = 'BIE'
    elif PARENT and hasattr(PARENT, 'tree_item'):
        tree_item = PARENT.tree_item
#   elif PARENT:
#       logging.warning("PARENT не имеет отображения: {0!r}".format(PARENT))
#       tree_item = None
    else:
        tree_item = None

    if tree_item:
        name = unicode(OBJECT.name) if hasattr(OBJECT, 'name') else \
               plain_type(OBJECT)

        OBJECT.tree_item = FileItem(tree_item, name, brief=brief, summary=OBJECT)

        if style:
            OBJECT.tree_item.set_style(style)

    return tree_item


class aObject(aStr):
    def __init__(self, **kargs):
        for key, val in kargs.items():
            setattr(self, key, val)

    def __unicode__(self):
        return "<Элемент>"
