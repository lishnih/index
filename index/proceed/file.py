#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from .handler import proceed

from models import File
from reg import reg_object1
from reg.result import reg_warning, reg_error, reg_exception


def proceed_file(filename, options, DIR):
    basename = os.path.basename(filename)

    file_dict = dict(_dir=DIR, name=basename)
    FILE = reg_object1(File, file_dict, DIR)

    handler_options = options.get('handler')
    if handler_options:
        logging.debug("Handle: {0}".format(basename))
        try:
            proceed(filename, handler_options, FILE)
        except Exception as e:
            reg_exception(FILE, e)
