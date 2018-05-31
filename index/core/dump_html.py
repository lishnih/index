#!/usr/bin/env python
# coding=utf-8
# Stan 2007-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import logging
from inspect import ismethod
from xml.sax.saxutils import escape, prepare_input_source

from .backwardcompat import *


""" Отладочный вывод переменных различных типов
plain_val  возвращает строковое представление объекта
plain      возвращает развёрнутое представление объекта

html_type  возвращает тип объекта для html
html_val   html-версия функции plain_val
html       html-версия функции plain
html_r     вспомогательная функция для функции html
"""


def plain_val(obj):
    if obj is None:
        buf = '/is None/'
    elif isinstance(obj, numeric_types):
        buf = unicode(obj)
    else:
        try:
            buf = unicode(obj)
        except:
            buf = repr(obj)
            buf = buf.replace(r'\n', '\n')
            buf = buf.replace(r'\r', '')

    return buf


def plain(obj):
    buf = '\n'

    # === Iter ===
    buf += 'Iter свойства:\n==============\n'
    list_buf = ''
    if not isinstance(obj, string_types):
        try:
            for val in obj:
                list_buf += "{0}\n".format(plain_val(val))
        except:
            pass

    if list_buf:
        buf += list_buf
    buf += '\n'

    # === Dict ===
    buf += 'Dict свойства:\n==============\n'
    list_buf = ''
    if not isinstance(obj, string_types):
        try:
            for key, val in obj.items():
                list_buf += '{0:20}: {1}\n'.format(key, plain_val(val))
        except:
            pass

    if list_buf:
        buf += list_buf
    buf += '\n'

    # === dict ===
    buf += 'dict свойства:\n==============\n'
    if hasattr(obj, '__dict__'):
        d = obj.__dict__
        for key in sorted(d.keys()):
            if key[0:2] != '__':
                val = d.get(key)
                buf += '{0:20}: {1}\n'.format(key, plain_val(val))

    buf += '\n'

    # === dir ===
    buf += 'dir свойства:\n=============\n'
    dirs_buf = ''
    for key in dir(obj):
        val = getattr(obj, key)
        if not callable(val):
            if key[0:2] != '__':
                dirs_buf += '{0:20}: {1}\n'.format(key, plain_val(val))

    if dirs_buf:
        buf += dirs_buf
    buf += '\n'

    # === Callable ===
    buf += 'Callable свойства:\n==================\n'
    dirs_buf = ''
    for key in dir(obj):
        val = getattr(obj, key)
        if callable(val):
            if key[0:2] != '__':
                dirs_buf += '{0:20}: {1}\n'.format(key, plain_val(val))

    if dirs_buf:
        buf += dirs_buf
    buf += '\n'

    return buf


def html_type(obj):
    return escape(plain_val(type(obj)))


def html_val(obj, color=""):
    type_obj = html_type(obj)
    obj = escape(plain_val(obj))
    obj = obj.replace('\r\n', '<br />')
    obj = obj.replace('\r',   '<br />')
    obj = obj.replace('\n',   '<br />')
    if color:
        buf = '<span title="{0}" style="color: {1};">{2}</span>'.format(type_obj, color, obj)
    else:
        buf = '<span title="{0}">{1}</span>'.format(type_obj, obj)

    return buf


def html(obj, it=1, root=None, collection=[]):
    # Переменная collection постоянно накопляется, поэтому сбрасываем её при
    # новом использовании функции html
    if root is None:
        collection = []

    if root is obj:
        return '<span style="color: red;"><i>on self</i></span>'

    buf = ""

    if obj is None:
        buf = '<span style="color: gray;"><i>is None</i></span>'
    elif isinstance(obj, numeric_types):
        buf = html_val(obj, 'blue')
    elif isinstance(obj, simple_types):
        buf = html_val(obj)

    if buf:
        return buf

    # Использование "if obj in collection" в некоторых случаях недопустимо!
    for i in collection:
        if i is obj:
            return html_val(obj, "green")
    collection.append(obj)

    if isinstance(obj, (list, tuple)):
        buf = '<ul>\n'
        for value in obj:
            buf += '<li>{0}</li>'.format(html(value, it, obj, collection))
        buf += '</ul>\n'
    elif isinstance(obj, dict):
        buf = '<ul>\n'
        for key, value in obj.items():
            buf += '<li>{0}: {1}</li>'.format(key, html(value, it, obj, collection))
        buf += '</ul>\n'

    if buf:
        return buf

    # Итерацию проверяем только для объектов
    if not it:
        return html_val(obj, "dimgray")
    it -= 1

    buf = html_r(obj, it, root, collection)

    return buf


def html_r(obj, it=1, root=None, collection=[]):
    buf = '<table style="background-color: lightcyan; border: 1px solid black;">\n'
    buf += '  <tr><th colspan="2" style="background-color: cornflowerblue;">{0}</th></tr>\n'.format(html_val(obj))

    # === DIR ===
    dirs_buf = ''
    number = 0
    for key in dir(obj):
        val = getattr(obj, key)
        if not ismethod(val):
            if key[0:2] != '__':
                dirs_buf += '  <tr>' if number % 2 == 0 else '  <tr style="background-color: lightblue;">'
                dirs_buf += '    <td style="color: blue;"><b>{0}</b></td><td>{1}</td>\n'.format(key, html(val, it, obj, collection))
                dirs_buf += '  </tr>'
                number += 1
    if dirs_buf:
#       buf += '  <tr><th colspan="2" style="background-color: yellow;">Dirs свойства:</th></tr>\n{0}'.format(dirs_buf)
        buf += dirs_buf

    # === ITER ===
#     if not isinstance(obj, string_types):
#         list_buf = ''
#         try:
#             for val in obj:
#                 list_buf += '  <tr><td></td><td>{0}</td></tr>\n'.format(html(val, it, obj, collection))
#         except:
#             pass
#         if list_buf:
#             buf += '  <tr><th colspan="2" style="background-color: yellow;">Iter свойства:</th></tr>\n{0}'.format(list_buf)

    # === DICT ===
#     if hasattr(obj, '__dict__'):
#         buf += '  <tr><th colspan="2" style="background-color: yellow;">Dict свойства:</th></tr>\n'
#         d = obj.__dict__
#         for key in sorted(d.keys()):
#             if key[0:2] != '__':
#                 val = d.get(key)
#                 buf += '  <tr><td style="color: blue;"><b>{0}</b></td><td>{1}</td></tr>\n'.format(key, html(val, it, obj, collection))

    buf += '</table>\n'

    return buf
