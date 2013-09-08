#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from .dir import reg_dir
from .file import proceed_file
from lib.data_funcs import get_list, filter_match, filter_list
from reg            import set_object
from reg.result     import reg_exception


def proceed(source, options={}, session=None, ROOT=None, status=None):
    filename = os.path.abspath(source)

    if os.path.isdir(filename):
        logging.info("Обработка директории '{0}'".format(filename))

        dirs_filter = options.get('dirs_filter')
        files_filter = options.get('files_filter')

        # Dir
        for dirname, dirs, files in os.walk(filename):
            if filter_match(dirname, dirs_filter):
                DIR = reg_dir(dirname, options, session, ROOT)

                files_filtered = filter_list(files, files_filter)

                for filename in files:
                    if filename in files_filtered:
                        # File
                        filename = os.path.join(dirname, filename)
                        proceed_file(filename, options, session, DIR)
                    else:
                        set_object(filename, DIR, style='D', brief="Этот файл не индексируется!")

                    if isinstance(status, dict):
                        status['files'] += 1

            else:
                set_object(dirname, ROOT, style='D', brief="Эта директория не индексируется!")

            if isinstance(status, dict):
                status['dirs'] += 1

    elif os.path.isfile(filename):
        logging.info("Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, options, ROOT)

        # File
        proceed_file(filename, options, session, DIR)

    else:
        logging.warning("Не найден файл/директория '{0}'!".format(filename))

    try:
        session.commit()
    except Exception as e:    # StatementError
        reg_exception(ROOT, e)
