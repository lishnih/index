#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os
import xlrd

from .sheet import proceed_sheet

from models import File
from reg import reg_object, set_object
from reg.result import reg_warning, reg_error, reg_exception

from lib.data_funcs import filter_match, filter_list


def proceed(filename, options, FILE):
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
        FILE.tree_item.setBrief(brief)

        if ext == '.xlsx':
            reg_warning(FILE, "'formatting_info=True' not yet implemented!")

        nsheets = book.nsheets
        FILE.nsheets = nsheets

        for name in sheets_list:
            sh = book.sheet_by_name(name)
            i = sheets.index(name)
            proceed_sheet(sh, options, FILE, i)
            book.unload_sheet(name)

        return
