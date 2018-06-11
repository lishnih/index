#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os

from .file import proceed_file

from ...reg import set_object
from ...reg.result import *


def reg_dir(dirname, runtime, ROOT=None):
    DIR = set_object(dirname, ROOT, style='B')

    return DIR


def proceed_dir(dirname, runtime, ROOT=None, status=None):
    # Проверяем требование выйти
    if status.break_required:
        return

    for dirname, dirs, files in os.walk(dirname):
        # Dir
        DIR = reg_dir(dirname, runtime, ROOT)
        status.dir = dirname

        set_expanded(DIR)

        for basename in files:
            # File
            filename = os.path.join(dirname, basename)
            proceed_file(filename, runtime, DIR, status)


def proceed_dir_tree(dirname, runtime, ROOT=None, status=None):
    # Проверяем требование выйти
    if status.break_required:
        return

    # Dir
    DIR = reg_dir(dirname, runtime, ROOT)
    status.dir = dirname

    set_expanded(DIR)

    # Пролистываем содержимое директории
    try:
        ldir = os.listdir(dirname)
    except Exception as e:
        set_object(dirname, ROOT, style='D', brief="No access: {0}".format(dirname))
        return

    for basename in sorted(ldir):
        filename = os.path.join(dirname, basename)
        if os.path.isdir(filename):
            proceed_dir_tree(filename, runtime, DIR, status)

    for basename in sorted(ldir):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            # File
            proceed_file(filename, runtime, DIR, status)

    return DIR
