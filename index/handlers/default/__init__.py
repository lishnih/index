#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-07

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import logging

from .dir import proceed_dir, proceed_dir_tree, reg_dir
from .file import proceed_file

from ...reg.result import *


# def opening(files, profile, options=None):
#     return


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


# def closing(files, profile, runtime):
#     return
