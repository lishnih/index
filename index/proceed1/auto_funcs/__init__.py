#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-29

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, glob, importlib, logging


functions = dict()


modulepath = os.path.dirname(__file__)
modulename = __name__


modulesnames = []
for filename in glob.glob(os.path.join(modulepath, '*.py')):
    basename = os.path.basename(filename)
    if basename != '__init__.py':
        root, ext = os.path.splitext(basename)
        modulesnames.append(root)


for i in modulesnames:
    module = importlib.import_module('.' + i, modulename)

    for i in dir(module):
        obj = getattr(module, i)
        if callable(obj):
            if i in functions:
                logging.warning("Функция '{0}' уже загружена!".format(i))
            else:
                functions[i] = obj


def empty_func(*args, **kargs):
    msg = """(((((((
Вызвана заглушка с параметрами:
args:  {0!r}
kargs: {1!r}
)))))))\n""".format(args, kargs)
    logging.warning(msg)


def default_error_callback(func_name, e, *args, **kargs):
    msg = """(((((((
Функция '{0}' вызвала ошибку:
{1}!
Были переданый следующие параметры:
args: {2!r}
kargs: {3!r}
)))))))\n""".format(func_name, e, args, kargs)
    logging.error(msg)


def get(func_name):
    if func_name not in functions:
        logging.warning("Функция не найдена: {0}, используем заглушку!".format(func_name))
        functions[func_name] = empty_func

    func = functions.get(func_name)
    return func


def call(func_name, *args, **kargs):
    func = get(func_name)
    error_callback = kargs.pop('error_callback', default_error_callback)

    try:
        res = func(*args, **kargs)
    except Exception as e:
        error_callback(func_name, e, *args, **kargs)
        res = None

    return res
