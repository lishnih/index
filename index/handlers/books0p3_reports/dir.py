#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os

from .file import proceed_file
from .stuff.data_funcs import filter_match
from .stuff.models import Dir

from ...reg import set_object, reg_object1
from ...reg.result import *


def reg_dir(dirname, runtime, ROOT=None):
    dir_dict = dict(name=dirname)

    session = runtime.get('session')
    DIR = reg_object1(session, Dir, dir_dict, ROOT, style='B')

    return DIR


def proceed_dir(dirname, runtime, ROOT=None, status=None):
    # Проверяем требование выйти
    if status.break_required:
        return

    options = runtime.get('options', {})
    dirs_filter = options.get('dirs_filter')
    files_filter = options.get('files_filter')

    for dirname, dirs, files in os.walk(dirname):
        # Dir
        DIR = reg_dir(dirname, runtime, ROOT)
        status.dir = dirname

        set_expanded(DIR)

        basename = os.path.basename(dirname)
        significant = filter_match(basename, dirs_filter)
        DIR.significant = significant

        for basename in files:
            filename = os.path.join(dirname, basename)
            if significant and filter_match(basename, files_filter):
                # File
                proceed_file(filename, runtime, DIR, status)

            else:
                set_object(basename, DIR, style='D', brief="Файл не обрабатывается!")


def proceed_dir_tree(dirname, runtime, ROOT=None, status=None):
    # Проверяем требование выйти
    if status.break_required:
        return

    options = runtime.get('options', {})
    dirs_filter = options.get('dirs_filter')
    files_filter = options.get('files_filter')

    # Dir
    DIR = reg_dir(dirname, runtime, ROOT)
    status.dir = dirname

    set_expanded(DIR)

    basename = os.path.basename(dirname)
    significant = filter_match(basename, dirs_filter)
    DIR.significant = significant

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
            if significant and filter_match(basename, files_filter):
                # File
                proceed_file(filename, runtime, DIR, status)

            else:
                set_object(basename, DIR, style='D', brief="Файл не обрабатывается!")

    return DIR
