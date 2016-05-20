#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import re

from ...reg import reg_object1
from ...reg.result import reg_debug, reg_warning, reg_error
from .lib.backwardcompat import *
from .lib.sheet_funcs import get_str
from .lib.sheet_parse import proceed_marks, parse_doc, parse_table
from .lib.xlrd_macro import search_regexp


def proceed_sheet(sh, runtime, FILE, i=None):
    model = runtime.get('m_module')
    options = runtime.get('options', {})
    session = runtime.get('session')

    sheet_dict = dict(
#       _file   = FILE,
        _fileprocessing = FILE,
        name    = sh.name,
        seq     = i,
        ncols   = sh.ncols,
        nrows   = sh.nrows,
        visible = sh.visibility,
    )
    SHEET = reg_object1(session, model.Sheet, sheet_dict, FILE)

    groups = []
    sheet_test = options.get('sheet_test')
    if sheet_test:
        if isinstance(sheet_test, string_types):
            yx = search_regexp(sh, sheet_test)
            test_cell = sheet_test
            if yx:
                groups = [test_cell]
                SHEET.test_groups = groups
        elif isinstance(sheet_test, collections_types):
            l = len(sheet_test)
            if len == 3:
                row, col, test_pattern = sheet_test
                test_cell = get_str(sh, row, col)
                SHEET.test_cell = test_cell
                res = re.search(test_pattern, test_cell)
                if res:
                    groups = res.groups()
                    SHEET.test_groups = groups
            else:
                reg_error(SHEET, "Проверьте переменную 'sheet_test': '{0}'".format(sheet_test))
                return
        else:
            reg_error(SHEET, "Проверьте переменную 'sheet_test': '{0}'".format(sheet_test))
            return

#       DIR = FILE._dir
        DIR = FILE._file._dir
        reg_debug(DIR, test_cell)

    # Здесь мы пробуем выбрать ветку groups из options
    group_options = options
    branch = []
    for i in groups:
        if i not in group_options:
            break
        group_options = group_options[i]
        branch.append(i)

    SHEET.branch = branch

    # Сообщаем, если ветка помечена как устаревшая
    if group_options.get('deprecated'):
        reg_warning(SHEET, "Group deprecated!")

    # Если в текущей ветке есть 'default_group', то считываем его и загружаем
    default_group = group_options.get('default_group')
    if default_group:
        group_options = options.get(default_group)
        if not group_options:
            reg_warning(SHEET, "Проверьте характеристику листа: '{0!r}'".format(branch))
            reg_warning(SHEET, "Проверьте значение по умолчанию: '{0!r}'".format(default_group))
            return

    marks = dict()
    if 'marks' in group_options:
        marks_values = group_options['marks']
        marks = proceed_marks(sh, marks_values, SHEET)

    if 'doc' in group_options:
        doc_options = group_options['doc']
        parse_doc(sh, doc_options, session, model, marks, SHEET)

    if 'docs' in group_options:
        for doc_options in group_options['docs']:
            parse_doc(sh, doc_options, session, model, marks, SHEET)

    if 'table' in group_options:
        table_options = group_options['table']
        parse_table(sh, table_options, session, model, marks, SHEET)

    if 'tables' in group_options:
        for table_options in group_options['tables']:
            parse_table(sh, table_options, session, model, marks, SHEET)
