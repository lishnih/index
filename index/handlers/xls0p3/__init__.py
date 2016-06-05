#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07, 2016-04-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from ...reg import set_object
from .dir import proceed_dir, proceed_dir_tree, reg_dir
from .file import proceed_file

from ...lib.settings import Settings
from .lib.db import initDb, utilDb
from .lib.models import Base


def prepare(files, profile, options=None):
    s = Settings(profile)
    s.saveEnv()

    if not options:
        options = s.get_group('options')

    db_name = options.get('db_name', profile)
    db_uri = options.get('db_uri', "{0}:///{1}/{2}.sqlite".format('sqlite', s.system.path, db_name))
    session = initDb(dict(db_uri=db_uri), base=Base)

    archive_db = options.get('archive_db')
    clear_db = options.get('archive_db')
    prefix = options.get('prefix', 'xls')
    utilDb(session, archive_db=archive_db, clear_db=clear_db, prefix=prefix)

    runtime = dict(
        db_uri = db_uri,
        session = session,
        options = options,
    )
    return runtime


def proceed(filename, runtime=None, ROOT=None, status=None):
    if not runtime:
        runtime = dict()
    options = runtime.get('options', {})

    # Начинаем обработку
    if os.path.isdir(filename):
        logging.info("Обработка директории '{0}'".format(filename))

        treeview = options.get('treeview', 'list')
        # Dir
        if treeview == 'tree':
            proceed_dir_tree(filename, runtime, ROOT, status)

        else:
            proceed_dir(filename, runtime, ROOT, status)

    elif os.path.isfile(filename):
        logging.info("Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, runtime, ROOT)
        status.dir = '-'

        if hasattr(DIR, 'tree_item'):
            DIR.tree_item.setExpanded(True)

        # File
        proceed_file(filename, runtime, DIR, status)

    else:
        logging.warning("Не найден файл/директория '{0}'!".format(filename))


def ending(files, profile, runtime):
    session = runtime.get('session')
    if session:
        session.commit()