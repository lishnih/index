#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os
import xlrd

from . import sheet
from models import Handler
from reg import reg_object1
from reg.result import reg_warning

from lib.data_funcs import filter_match, filter_list


handler_name = __name__.rsplit('.', 1)[1]


def reg_handler(handlername, options, session, FILE):
    handler_dict = dict(name=handlername)
    HANDLER = reg_object1(session, Handler, handler_dict, FILE)

    return HANDLER


def proceed(filename, options, session, FILE):
    HANDLER = reg_handler(handler_name, options, session, FILE)

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

        FILE.nsheets = book.nsheets

        for name in sheets_list:
            sh = book.sheet_by_name(name)
            i = sheets.index(name)
            sheet.proceed_sheet(sh, options, session, FILE, HANDLER, i)
            book.unload_sheet(name)

        HANDLER.tree_item.setOk()
