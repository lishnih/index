#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging
import xlrd

from reg import reg_object1
from reg.result import reg_warning

from lib.data_funcs import filter_match, filter_list


def proceed(filename, options, session, FILE):
    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    ext = ext.lower()

    logging.debug("Возможная обработка файла {0}".format(filename))

    FILE.tree_item.setOk()
