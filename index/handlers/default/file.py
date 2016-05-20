#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ...reg import set_object


def reg_file(filename, runtime, DIR=None):
    basename = os.path.basename(filename)
    statinfo = os.stat(filename)
    size  = statinfo.st_size
    mtime = statinfo.st_mtime

    file_dict = dict(
        _dir = DIR,
        name = basename,
        mtime = mtime,
        size = size,
        statinfo = statinfo,
    )

    FILE = set_object(basename, DIR, brief=file_dict)

    return FILE


def proceed_file(filename, runtime, DIR=None, status=None):
    FILE = reg_file(filename, runtime, DIR)
    status.file = filename
