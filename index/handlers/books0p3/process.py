#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import logging

import xlrd

from ...reg.result import *
from .stuff.data_funcs import filter_match
from .sheet import proceed_sheet


def proceed(filename, runtime, FILE):
    options = runtime.get('options', {})

    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    ext = ext.lower()

    if ext in ['.xls', '.xlsx', '.xlsm', '.xlsb']:
        # Sheet
        if ext == '.xls':
            book = xlrd.open_workbook(filename, on_demand=True, formatting_info=True)
        else:
            reg_debug(FILE, "Option 'formatting_info=True' is not implemented yet!")
            book = xlrd.open_workbook(filename, on_demand=True)

        sheets = book.sheet_names()
        sheets_filter = options.get('sheets_filter')
        sheets_list = [i for i in sheets if filter_match(i, sheets_filter)]

        brief = [sheets, '---', sheets_list]
        reg_debug(FILE, brief)

        FILE.nsheets = book.nsheets

        for name in sheets_list:
            sh = book.sheet_by_name(name)
            i = sheets.index(name)
            proceed_sheet(sh, runtime, i, FILE)
            book.unload_sheet(name)
