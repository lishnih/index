#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from ...reg import set_object
from ...reg.result import reg_exception
from .handler import reg_handler
from .dir import proceed_dir, proceed_dir_tree, reg_dir
from .file import proceed_file


def proceed(source, options, session, model, ROOT=None, status=None):
    # Регистрируем обработчик
    HANDLER = reg_handler(options, session, model.Handler, ROOT)

    # Начинаем обработку
    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')

    if os.path.isdir(filename):
        logging.info("Обработка директории '{0}'".format(filename))

        treeview = options.get('treeview')
        # Dir
        if treeview == 'tree':
            proceed_dir_tree(filename, options, session, model, ROOT, HANDLER, status)
            if isinstance(status, dict):
                status['dirs'] += 1

        else:
            proceed_dir(filename, options, session, model, ROOT, HANDLER, status)

    elif os.path.isfile(filename):
        logging.info("Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, options, session, model.Dir, ROOT)

        # File
        proceed_file(filename, options, session, model, DIR, HANDLER)

    else:
        logging.warning("Не найден файл/директория '{0}'!".format(filename))
