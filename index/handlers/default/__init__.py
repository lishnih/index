#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from ...reg import set_object
from ...reg.result import reg_exception
from .dir import proceed_dir, proceed_dir_tree, reg_dir
from .file import proceed_file


def proceed(filename, runtime, ROOT=None, status=None):
    options = runtime.get('options', {})

    # Начинаем обработку
    if os.path.isdir(filename):
        logging.info("Обработка директории '{0}'".format(filename))

        treeview = options.get('treeview', 'list')
        # Dir
        if treeview == 'tree':
            proceed_dir_tree(filename, runtime, ROOT, status)
            if isinstance(status, dict):
                status['dirs'] += 1

        else:
            proceed_dir(filename, runtime, ROOT, status)

    elif os.path.isfile(filename):
        logging.info("Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, runtime, ROOT)

        # File
        proceed_file(filename, runtime, DIR)

    else:
        logging.warning("Не найден файл/директория '{0}'!".format(filename))
