#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ..lib.data_funcs import filter_match, filter_list
from ..reg import reg_object1, set_object
from .models import Dir
from .file import proceed_file


def reg_dir(dirname, options, session, ROOT=None):
    dir_dict = dict(name=dirname)
    DIR = reg_object1(session, Dir, dir_dict, ROOT, style='B')

    return DIR


def proceed_dir(dirname, options, session, ROOT=None, status=None):
    dirs_filter = options.get('dirs_filter')
    files_filter = options.get('files_filter')

    for dirname, dirs, files in os.walk(dirname):
        if os.path.isdir(dirname):
            if filter_match(dirname, dirs_filter):
                files_filtered = filter_list(files, files_filter)
                if dirs or files_filtered:
                    # Dir
                    DIR = reg_dir(dirname, options, session, ROOT)

                    for basename in files:
                        filename = os.path.join(dirname, basename)
                        if os.path.isfile(filename):
                            if basename in files_filtered:
                                # Перед обработкой файла проверяем требование выйти
                                if isinstance(status, dict) and status.get('break') == True:
                                    return

                                # File
                                proceed_file(filename, options, session, DIR)
                            else:
                                set_object(basename, DIR, style='D', brief="Файл не индексируется!")

                            if isinstance(status, dict):
                                status['files'] += 1

                        else:
                            set_object(filename, ROOT, style='D', brief="Файл не найден!")

                else:
#                   status['files'] += len(files)
                    set_object(dirname, ROOT, style='D', brief="Директория без индексных файлов!")

            else:
#               status['files'] += len(files)
                set_object(dirname, ROOT, style='D', brief="Директория не индексируется!")

            if isinstance(status, dict):
                status['dirs'] += 1

        else:
            set_object(dirname, ROOT, style='D', brief="Директория не найдена!")


def proceed_dir_tree(dirname, options, session, ROOT=None, status=None):
    # Dir
    DIR = reg_dir(dirname, options, session, ROOT)

    # Пролистываем содержимое директории
    try:
        ldir = os.listdir(dirname)
    except Exception as e:
        set_object(dirname, ROOT, style='D', brief="No access: {0}".format(dirname))
        return

    dirs_filter = options.get('dirs_filter')
    files_filter = options.get('files_filter')

    for basename in sorted(ldir):
        filename = os.path.join(dirname, basename)
        if os.path.isdir(filename):
            if filter_match(basename, dirs_filter):
                proceed_dir_tree(filename, options, session, DIR, status)

            else:
                set_object(filename, DIR, style='D', brief="Директория не индексируется!")

            if isinstance(status, dict):
                status['dirs'] += 1

    for basename in sorted(ldir):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            if filter_match(basename, files_filter):
                # Перед обработкой файла проверяем требование выйти
                if isinstance(status, dict) and status.get('break') == True:
                    return

                # File
                proceed_file(filename, options, session, DIR)

            else:
                set_object(basename, DIR, style='D', brief="Файл не индексируется!")

            if isinstance(status, dict):
                status['files'] += 1

    return DIR
