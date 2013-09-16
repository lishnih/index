#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from ..reg import set_object
from ..reg.result import reg_exception
from .dir import proceed_dir, proceed_dir_tree, reg_dir
from .file import proceed_file


def proceed(source, options={}, session=None, ROOT=None, status=None):
    filename = os.path.abspath(source)

    if os.path.isdir(filename):
        logging.info("Обработка директории '{0}'".format(filename))

        treeview = options.get('treeview')
        # Dir
        if treeview == 'tree':
            proceed_dir_tree(filename, options, session, ROOT, status)
            if isinstance(status, dict):
                status['dirs'] += 1

        else:
            proceed_dir(filename, options, session, ROOT, status)

    elif os.path.isfile(filename):
        logging.info("Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, options, session, ROOT)

        # File
        proceed_file(filename, options, session, DIR)

    else:
        logging.warning("Не найден файл/директория '{0}'!".format(filename))

    try:
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)
