#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, logging
import xlrd

from ...lib.data_funcs import filter_match, filter_list
from ...reg.result import reg_warning
from . import sheet


def proceed(filename, runtime, FILE):
    logging.debug("Обработка файла {0}".format(filename))

    model = runtime.get('m_module')
    options = runtime.get('options', {})
    session = runtime.get('session')

    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    ext = ext.lower()

    if ext == '.xls' or ext == '.xlsx':
        # Sheet
        if ext == '.xls':
            book = xlrd.open_workbook(filename, on_demand=True, formatting_info=True)
        else:
            book = xlrd.open_workbook(filename, on_demand=True)

        sheets = book.sheet_names()
        sheets_filter = options.get('sheets_filter')
        sheets_list = filter_list(sheets, sheets_filter)

        brief = [sheets, '---', sheets_list]
        if hasattr(FILE, 'tree_item'):
            FILE.tree_item.setBrief(brief)

        if ext == '.xlsx':
            reg_warning(FILE, "'formatting_info=True' not yet implemented!")

        FILE.nsheets = book.nsheets

        for name in sheets_list:
            sh = book.sheet_by_name(name)
            i = sheets.index(name)
            sheet.proceed_sheet(sh, runtime, FILE, i)
            book.unload_sheet(name)

        if hasattr(FILE, 'tree_item'):
            FILE.tree_item.setOk()
