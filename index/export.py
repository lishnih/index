#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, importlib, logging
from PySide import QtCore
import yaml

from .lib.backwardcompat import *
from .reg import set_object
from .reg.result import reg_debug, reg_warning, reg_error, reg_exception


def Proceed(files, profile=None, tree_widget=None, status=None):
    if not profile:
        profile = 'default'

    brief = {
                "Input files": files,
                "Profile": profile,
                "===": "===================="
            }
    ROOT = set_object("Root", tree_widget, brief=brief)

    # Сбрасываем данные статуса и устанавливаем сообщение
    if status:
        status.reset(files)

    # Загружаем обработчик (handler)
    handler = __package__ + '.handlers.' + profile
    try:
        handler_module = importlib.import_module(handler)
    except Exception as e:
        reg_exception(ROOT, e)
        status.error = "Error in module '{0}'!".format(handler)
        return

    # Обработчик имеет точку входа 'proceed'
    if not hasattr(handler_module, 'proceed'):
        msg = "Function 'proceed' is missing in the handler '{0}'!".format(profile)
        reg_error(ROOT, msg)
        status.error = msg
        return

    if hasattr(handler_module, 'prepare'):
        runtime = handler_module.prepare(files, profile)
    else:
        runtime = None
        msg = "Function 'prepare' is missing in the handler '{0}'!".format(profile)
        reg_debug(ROOT, msg)

    brief = {
                "Runtime": runtime,
                "===": "===================="
            }
    set_object("runtime", tree_widget, brief=brief)

    if not isinstance(files, collections_types):
        files = [files]

    # Обработка
    for i in files:
        i = os.path.abspath(i)
        try:
            handler_module.proceed(i, runtime, ROOT, status)
        except Exception as e:
            reg_exception(ROOT, e)
            status.error = "Error during handle file '{0}'!".format(i)

    if hasattr(ROOT, 'tree_item'):
        ROOT.tree_item.setSelected(True)

    if hasattr(handler_module, 'ending'):
        handler_module.ending(files, profile, runtime)
    else:
        msg = "Function 'ending' is missing in the handler '{0}'!".format(profile)
        reg_debug(ROOT, msg)


def main(files=None, profile=None):
    if files:
        Proceed(files, profile)

    else:
        logging.warning("Files not specified!")
