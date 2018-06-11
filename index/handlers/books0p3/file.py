#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os

from ...reg import set_object, reg_object
from ...reg.result import *

from .stuff.models import File
from .process import proceed


def reg_file(filename, runtime, DIR=None):
    basename = os.path.basename(filename)
    statinfo = os.stat(filename)
    size = statinfo.st_size
    mtime = statinfo.st_mtime

    file_dict = {
        '_dir': DIR,
        'name': basename,
        'mtime': mtime,
        'size': size,
    }

    session = runtime.get('session')
    FILE = reg_object(session, File, file_dict, DIR)

    return FILE


def proceed_file(filename, runtime, DIR=None, status=None):
    # Проверяем требование выйти
    if status.break_required:
        return

    FILE = reg_file(filename, runtime, DIR)
    status.file = filename

    try:
        proceed(filename, runtime, FILE)
        FILE.status = 1

#       reg_ok(FILE)
    except Exception as e:
        reg_exception(FILE, e)
        FILE.status = -1
        return
