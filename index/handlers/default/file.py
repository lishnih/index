#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ...reg import reg_object1
from ...reg.result import reg_exception
from .process import proceed


def reg_file(filename, options, session, model, DIR=None):
    basename = os.path.basename(filename)
    statinfo = os.stat(filename)
    size  = statinfo.st_size
    mtime = statinfo.st_mtime

    file_dict = dict(_dir=DIR, name=basename, size=size, mtime=mtime)
    FILE = reg_object1(session, model.File, file_dict, DIR)

    return FILE


def proceed_file(filename, options, session, model, DIR=None):
    FILE = reg_file(filename, options, session, model, DIR)

    try:
        proceed(filename, options, session, model, FILE)
    except Exception as e:
        reg_exception(FILE, e)
        return
