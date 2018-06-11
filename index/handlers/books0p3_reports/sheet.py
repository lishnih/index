#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import re

from ...reg import reg_object1, set_object
from ...reg.result import *
from .stuff.backwardcompat import *
from .stuff.sheet_funcs import get_str
from .stuff.sheet_parse import proceed_marks, parse_doc, parse_table
from .stuff.xlrd_macro import search_regexp
from .stuff import models


def reg_sheet(sh, runtime, i, FILE=None):
    sheet_dict = {
        '_file': FILE,
#       '_fileprocessing': FILE,
        'name': sh.name,
        'seq': i,
        'ncols': sh.ncols,
        'nrows': sh.nrows,
        'visible': sh.visibility,
    }

    session = runtime.get('session')
    if session:
        SHEET = reg_object1(session, models.Sheet, sheet_dict, FILE)
    else:
        SHEET = set_object(sheet_dict, FILE)

    return SHEET, session


def proceed_sheet(sh, runtime, i, FILE=None):
    SHEET, session = reg_sheet(sh, runtime, i, FILE)

    options = runtime.get('options', {})

    groups = []
    sheet_test = options.get('sheet_test')
    SHEET.sheet_test = sheet_test
    if sheet_test:
        if isinstance(sheet_test, string_types):
            yx = search_regexp(sh, sheet_test)
            if yx:
                row, col = yx
                test_cell = get_str(sh, row, col)
                SHEET.test_cell = test_cell
                res = re.search(sheet_test, test_cell)
                if res:
                    groups = res.groups()
                    SHEET.test_groups = groups
        elif isinstance(sheet_test, collections_types):
            l = len(sheet_test)
            if l == 2:
                row, col = sheet_test
                test_cell = get_str(sh, row, col)
                SHEET.test_cell = test_cell
                groups = [test_cell]
                if test_cell:
                    SHEET.test_groups = groups
            elif l == 3:
                row, col, test_pattern = sheet_test
                test_cell = get_str(sh, row, col)
                SHEET.test_cell = test_cell
                res = re.search(test_pattern, test_cell)
                if res:
                    groups = res.groups()
                    SHEET.test_groups = groups
            else:
                reg_error(SHEET, "Переменная 'sheet_test' неизвестной длины: '{0}', {1}".format(sheet_test, l))
                return
        else:
            reg_error(SHEET, "Переменная 'sheet_test' неизвестного типа: '{0}'".format(sheet_test))
            return

        DIR = FILE._dir
#       DIR = FILE._file._dir
        reg_debug(DIR, test_cell)

    # Здесь мы пробуем выбрать ветку groups из options (выборка может быть многоуровневой)
    group_options = options
    branch = []
    for i in groups:
        if i not in group_options:
            break
        group_options = group_options[i]
        branch.append(i)

    SHEET.branch = branch
    SHEET.group_options = group_options

    # Сообщаем, если ветка помечена как устаревшая
    if group_options.get('deprecated'):
        reg_warning(SHEET, "Group deprecated!")

    # Если в текущей ветке есть 'default_group', то считываем его и загружаем (перенаправление)
    default_group = group_options.get('default_group')
    if default_group:
        group_options = options.get(default_group)
        if not group_options:
            reg_warning(SHEET, "Проверьте характеристику листа: '{0!r}'".format(branch))
            reg_warning(SHEET, "Проверьте значение по умолчанию: '{0!r}'".format(default_group))
            return

    marks = {}
    if 'marks' in group_options:
        marks_values = group_options['marks']
        set_object("> Marks (options)", SHEET, brief=marks_values)
        marks = proceed_marks(sh, marks_values, SHEET)

    if 'doc' in group_options:
        doc_options = group_options['doc']
        set_object("> Doc (options)", SHEET, brief=doc_options)
        parse_doc(sh, doc_options, session, models, marks, SHEET)

    if 'docs' in group_options:
        for doc_options in group_options['docs']:
            set_object(">> Docs (options)", SHEET, brief=doc_options)
            parse_doc(sh, doc_options, session, models, marks, SHEET)

    if 'table' in group_options:
        table_options = group_options['table']
        set_object("> Table (options)", SHEET, brief=table_options)
        parse_table(sh, table_options, session, models, marks, SHEET)

    if 'tables' in group_options:
        for table_options in group_options['tables']:
            set_object(">> Tables (options)", SHEET, brief=table_options)
            parse_table(sh, table_options, session, models, marks, SHEET)

    reg_ok(SHEET)
