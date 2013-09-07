#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, importlib, logging

from models import File
from reg import reg_object1
from reg.result import reg_error, reg_exception


proceed_name = __name__.rsplit('.', 1)[0]


def reg_file(filename, options, session, DIR):
    basename = os.path.basename(filename)

    file_dict = dict(_dir=DIR, name=basename)
    FILE = reg_object1(session, File, file_dict, DIR)

    return FILE


def proceed_file(filename, options, session, DIR):
    logging.debug("Processing file: {0}".format(filename))
    FILE = reg_file(filename, options, session, DIR)

    handlers_dict = options.get('handlers', {})
    for handler_name, handler_options in handlers_dict.items():
        try:
            handler_module = importlib.import_module('.' + handler_name, proceed_name)
        except Exception as e:
            reg_exception(FILE, e)
            return

        if not hasattr(handler_module, 'proceed'):
            reg_error(FILE, "No 'proceed' function in module '{0}'".format(handler_name))
            return

        logging.debug("by handle: {0}".format(handler_name))
        try:
            handler_module.proceed(filename, handler_options, session, FILE)
        except Exception as e:
            reg_exception(FILE, e)
