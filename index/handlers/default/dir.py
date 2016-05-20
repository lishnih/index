#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ...reg import set_object
from .file import proceed_file


def reg_dir(dirname, runtime, ROOT=None):
    DIR = set_object(dirname, ROOT, style='B')

    return DIR


def proceed_dir(dirname, runtime, ROOT=None, status=None):
    for dirname, dirs, files in os.walk(dirname):
        if os.path.isdir(dirname):
            # Dir
            DIR = reg_dir(dirname, runtime, ROOT)
            status.dir = dirname

            if hasattr(DIR, 'tree_item'):
                DIR.tree_item.setExpanded(True)

            for basename in files:
                filename = os.path.join(dirname, basename)
                if os.path.isfile(filename):
                    # File
                    proceed_file(filename, runtime, DIR, status)

                else:
                    set_object(basename, DIR, style='D', brief="Файл не найден!")

                # Проверяем требование выйти
                if status.break_required == True:
                    return

        else:
            set_object(dirname, ROOT, style='D', brief="Директория не найдена!")


def proceed_dir_tree(dirname, runtime, ROOT=None, status=None):
    # Dir
    DIR = reg_dir(dirname, runtime, ROOT)
    status.dir = dirname

    if hasattr(DIR, 'tree_item'):
        DIR.tree_item.setExpanded(True)

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
            proceed_file(filename, runtime, DIR, status)

        else:
            set_object(basename, DIR, style='D', brief="Файл не найден!")

        # Проверяем требование выйти
        if status.break_required == True:
            return

    return DIR
