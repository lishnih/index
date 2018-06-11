#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07, 2016-04-22

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import logging

from .dir import proceed_dir, proceed_dir_tree, reg_dir
from .file import proceed_file
from .stuff.db import initDb, utilDb
from .stuff.models import Base

from ...core.settings import Settings
from ...reg.result import *


def opening(files, profile, options=None):
    s = Settings(profile)
    s.saveEnv()

    if not options:
        options = s.get_group('options')

    db_name = options.get('db_name', profile)
    if db_name:
        db_uri = options.get('db_uri', "{0}:///{1}/{2}.sqlite".format('sqlite', s.system.path, db_name))
        session = initDb(dict(db_uri=db_uri), base=Base)

        archive_db = options.get('archive_db')
        clear_db = options.get('archive_db')
        prefix = options.get('prefix', 'xls')
        utilDb(session, archive_db=archive_db, clear_db=clear_db, prefix=prefix)
    else:
        db_uri = None
        session = None

    runtime = {
        'db_uri': db_uri,
        'session': session,
        'options': options,
    }
    return runtime


def proceed(filename, runtime=None, ROOT=None, status=None):
    if not runtime:
        runtime = {}
    options = runtime.get('options', {})

    # Начинаем обработку
    if os.path.isdir(filename):
        logging.info(["Processing directory", filename])

        treeview = options.get('treeview', 'list')
        # Dir
        if treeview == 'tree':
            proceed_dir_tree(filename, runtime, ROOT, status)

        else:
            proceed_dir(filename, runtime, ROOT, status)

    elif os.path.isfile(filename):
        logging.info(["Processing file", filename])

        # Dir
        dirname = os.path.dirname(filename)
        DIR = reg_dir(dirname, runtime, ROOT)
        status.dir = '-'

        set_expanded(DIR)

        # File
        proceed_file(filename, runtime, DIR, status)

    else:
        logging.warning(["Directory/file not found", filename])


def closing(files, profile, runtime):
    session = runtime.get('session')
    if session:
        session.commit()
