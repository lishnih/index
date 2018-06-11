#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-29

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import glob
import importlib
import logging


modulesnames = []
modulepath = os.path.dirname(__file__)

for filename in glob.glob(os.path.join(modulepath, '*.py')):
    basename = os.path.basename(filename)
    if basename != '__init__.py':
        root, ext = os.path.splitext(basename)
        modulesnames.append(root)


functions = {}

for i in modulesnames:
    module = importlib.import_module('.' + i, __name__)

    for i in dir(module):
        obj = getattr(module, i)
        if callable(obj):
            if i in functions:
                logging.warning("Функция '{0}' уже загружена!".format(i))
            else:
                functions[i] = obj


logging.debug("auto_funcs загрузил следующие функции:")
logging.debug(functions)


def default_error_callback(func_name, e, *args, **kargs):
    msg = """(((((((
Функция '{0}' вызвала ошибку:
{1}!
Были переданый следующие параметры:
args: {2!r}
kargs: {3!r}
)))))))\n""".format(func_name, e, args, kargs)
    logging.error(msg)


def call(func_name, *args, **kargs):
    error_callback = kargs.pop('error_callback', default_error_callback)

    if func_name not in functions:
        error_callback(func_name, "Функция не найдена!", *args, **kargs)
        return

    try:
        func = functions[func_name]
        res = func(*args, **kargs)
    except Exception as e:
        error_callback(func_name, e, *args, **kargs)
    else:
        return res
