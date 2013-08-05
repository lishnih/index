#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-01

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import xlrd

from models import DBSession
from models.links import link_objects
from reg import reg_object, reg_object1
from reg.result import reg_warning, reg_error, reg_exception
from auto_funcs import call
from lib.data_funcs import get_list
from lib.sheet_funcs import get_value, get_index
from lib.xlrd_macro import search_value


def e_func(func_name, e, *args, **kargs):
    OBJ = args[2]
    e = "/Error in '{0}'/ {1}".format(func_name, e)
    reg_exception(OBJ, e, *args, **kargs)


def parse_doc(sh, options, SHEET):
    doc_values = options.get('doc_values', {})
    doc_funcs  = options.get('doc_funcs', {})

    doc_objects  = get_list(options.get('doc_objects'))
    doc_objects1 = get_list(options.get('doc_objects1'))

    doc_dict = dict()
    test = ""

    last_y, last_x = None, None
    for key, params in doc_values.items():
        l = len(params)
        if isinstance(params, basestring):
            yx = search_value(sh, params)
            if yx:
                last_y, last_x = yx
                val = get_value(sh, last_y, last_x)
                doc_dict[key] = val
                val_list = []
                for i in xrange(last_x + 1, sh.ncols):
                    val2 = get_value(sh, last_y, i)
                    if val2:
                        val_list.append(val2)
                doc_dict[key+'_list'] = val_list
                test += "{0} [{1},{2}]: {3} /{4!r}/ + /{5!r}/\n".format(key, last_y, last_x, val, val, val_list)
            else:
                reg_warning(SHEET, "Значение не найдено: '{0}', пропускаем лист!".format(params))
                return
        elif l == 2:
            y, x = params
            if isinstance(x, basestring):
                x = last_x + int(x)
            if isinstance(y, basestring):
                y = last_y + int(y)
            val = get_value(sh, y, x)
            doc_dict[key] = val
            test += "{0} [{1},{2}]: {3} /{4!r}/\n".format(key, y, x, val, val)
        elif l == 3:
            y, x = params
            if isinstance(x, basestring):
                x = last_x + int(x)
            if isinstance(y, basestring):
                y = last_y + int(y)
            val = get_value(sh, y, x)
            doc_dict[key] = val
            test += "{0} [{1},{2},{3}]: {4} /{5!r}/\n".format(key, y, x, pattern, val, val)

    remarks = {}
    for item, funcs_name in doc_funcs.items():
        for func_name in get_list(funcs_name):
            remarks1 = []
            call(func_name, doc_dict, item, remarks1, error_callback=e_func)
            if remarks1:
                remarks[func_name] = remarks1
    if remarks:
        reg_warning(SHEET, remarks)
        SHEET.remarks = remarks

    if doc_dict:
        ROWS = []
        for doc_object in doc_objects:
            ROWS.append(reg_object(doc_object, doc_dict, SHEET, brief=test))
        for doc_object in doc_objects1:
            ROWS.append(reg_object1(doc_object, doc_dict, SHEET, brief=test))

        link_objects(SHEET, *ROWS)


def parse_table(sh, options, SHEET):
    for i in parse_table_iter(sh, options, SHEET):
        pass


def parse_table_iter(sh, options, SHEET):
    row_start      = options.get('row_start', 1)
    row_start_skip = options.get('row_start_skip', 0)
    row_stop       = options.get('row_stop', sh.nrows)
    row_stop_skip  = options.get('row_stop_skip', 0)
    col_mode       = options.get('col_mode', 'column')
    col_names      = options.get('col_names', [])
    col_funcs      = options.get('col_funcs', {})

    check_name = options.get('check_name')
    col_index1 = col_names.index(check_name) if check_name else None

    check_column = options.get('check_column')
    col_index2 = get_index(check_column) if check_column else None

    typical_index = col_index1 or col_index2

    row_objects  = get_list(options.get('row_objects'))
    row_objects1 = get_list(options.get('row_objects1'))

    if isinstance(row_start, basestring):
        yx = search_value(sh, row_start)
        if not yx:
            reg_warning(SHEET, "Начало таблицы не найдено: '{0}', пропускаем лист!".format(row_start))
            return
        row_start = yx[0] + 1 + row_start_skip
        SHEET.row_start = row_start
    else:
        row_start = row_start - 1

    if isinstance(row_stop, basestring):
        yx = search_value(sh, row_stop)
        if not yx:
            reg_warning(SHEET, "Конец таблицы не найден: '{0}', индексируем весь лист!".format(row_stop))
            row_stop = sh.nrows
        else:
            row_stop = yx[0] - row_stop_skip
        SHEET.row_stop = row_stop

    for j in xrange(row_start, row_stop):
        typical_column = get_value(sh, j, typical_index) if typical_index else True
        if typical_column:
            row_dict = dict(j=j)
            test = "Номер строки: {0}\n".format(j)

            if col_mode == 'column':
                i = 0
                for col_name in col_names:
                    if col_name:
                        if isinstance(col_name, basestring):
                            val = get_value(sh, j, i)
                            row_dict[col_name] = val
                            test += "({0}:{1}) {2}: {3} /{4!r}/\n".format(j, i, col_name, val, val)
                        if isinstance(col_name, list):
                            inner_row = 0
                            for inner_col_name in col_name:
                                if inner_col_name:
                                    val = get_value(sh, j + inner_row, i)
                                    row_dict[inner_col_name] = val
                                inner_row += 1
                    i += 1
            elif col_mode == 'value':
                col = 0
                for i in xrange(sh.ncols):
                    val = get_value(sh, j, i)
                    if val:
                        col_name = col_names[col]
                        row_dict[col_name] = val
                        test += "({0}:{1}) {2}: {3} /{4!r}/\n".format(j, i, col_name, val, val)
                        col += 1
                        if col > len(col_names):
                            break

            remarks = {}
            res = None
            for item, funcs_name in col_funcs.items():
                for func_name in get_list(funcs_name):
                    remarks1 = []
                    res = call(func_name, row_dict, item, remarks1, error_callback=e_func)
                    # item1, list1, func1
                    if remarks1:
                        remarks[func_name] = remarks1
            if remarks:
                reg_warning(SHEET, remarks)
                SHEET.remarks = remarks
            if res:
                SHEET.res = res

#             test_row = ''
#             for i in xrange(sh.ncols):
#                 val = get_value(sh, j, i)
#                 test_row += "({0}): {1} /{2!r}/\n".format(i, val, val)
#             row_dict['test_row'] = test_row

            if row_dict:
                ROWS = []
                for row_object in row_objects:
                    obj = reg_object(row_object, row_dict, SHEET, brief=test)
                    obj._row = row_dict
                    ROWS.append(obj)
                for row_object in row_objects1:
                    obj = reg_object1(row_object, row_dict, SHEET, brief=test)
                    obj._row = row_dict
                    ROWS.append(obj)

#                 try:
#                     DBSession.commit()
#                 except Exception as e:
#                     reg_exception(SHEET, e, name, source)

                link_objects(SHEET, *ROWS)

                yield row_dict, ROWS
