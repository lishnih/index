#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import re

from models import Sheet
from reg import reg_object
from reg.result import reg_debug, reg_warning

from lib.sheet_funcs import get_str
from lib.sheet_parse import parse_doc, parse_table


def proceed_sheet(sh, options, FILE, i=None):
    sheet_dict = dict(
        _file = FILE,
        sh = sh,
        seq = i,
    )
    SHEET = reg_object(session, Sheet, sheet_dict, PARENT=FILE)

    sheet_test = options.get('sheet_test')
    groups = ()
    if sheet_test:
        row, col, test_pattern = sheet_test
        test_cell = get_str(sh, row, col)
        res = re.search(test_pattern, test_cell)
        if res:
            groups = res.groups()
            SHEET.sheet_test = test_cell
            SHEET.groups = groups
        else:
            msg = "В ({0},{1}) ожидается: '{2}', найдено: '{3}'".format(row, col, test_pattern, test_cell)
            reg_warning(SHEET, msg)

        TASK = FILE._dir._source._task
        reg_debug(TASK, test_cell)

    depth = options
    section = ["<options>"]
    for i in groups:
        if i in depth:
            depth = depth.get(i)
            section.append(i)
    SHEET.section = section

    deprecated_options = depth.get('deprecated')
    if deprecated_options:
        reg_warning(SHEET, 'deprecated')

    doc_options = depth.get('doc')
    if doc_options:
        SHEET.doc_options = doc_options
        parse_doc(sh, doc_options, SHEET)

    table_options = depth.get('table')
    if table_options:
        SHEET.table_options = table_options
        parse_table(sh, table_options, SHEET)
