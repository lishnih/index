#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import os
import logging
from importlib import import_module

from .core.backwardcompat import *
from .reg import set_object
from .reg.result import *


def Proceed(files='', profile='', options={}, tree_widget=None, status=None):
    files = files or options.get('files')
    profile = profile or options.get('profile', 'default')

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
        handler_module = import_module(handler)
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

    if hasattr(handler_module, 'opening'):
        runtime = handler_module.opening(files, profile, options)
    else:
        runtime = {}
        msg = "Function 'opening' is missing in the handler '{0}'!".format(profile)
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

    set_selected(ROOT)

    if hasattr(handler_module, 'closing'):
        handler_module.closing(files, profile, runtime)
    else:
        msg = "Function 'closing' is missing in the handler '{0}'!".format(profile)
        reg_debug(ROOT, msg)


def main(files=None, profile=None, options=None):
    if files:
        Proceed(files, profile, options)

    else:
        logging.warning("Files not specified!")
