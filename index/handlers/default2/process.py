#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging

from ...lib.data_funcs import filter_match, filter_list
from ...reg.result import reg_warning


def proceed(filename, runtime, FILE):
    logging.debug("Обработка файла {0}".format(filename))

    model = runtime.get('m_module')
    options = runtime.get('options', {})
    session = runtime.get('session')

    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    ext = ext.lower()

    # ...

    # Если обработка имела место, то можно пометить файл
    if hasattr(FILE, 'tree_item'):
        FILE.tree_item.setOk()
