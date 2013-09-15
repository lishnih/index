#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from .models import File
from .handler import proceed
from reg import reg_object1
from reg.result import reg_exception


def reg_file(filename, options, session, DIR=None):
    basename = os.path.basename(filename)

    file_dict = dict(_dir=DIR, name=basename)
    FILE = reg_object1(session, File, file_dict, DIR)

    return FILE


def proceed_file(filename, options, session, DIR=None):
    FILE = reg_file(filename, options, session, DIR)

    try:
        proceed(filename, options, session, FILE)
    except Exception as e:
        reg_exception(FILE, e)
        return
