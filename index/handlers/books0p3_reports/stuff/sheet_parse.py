#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-01

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import re

from ....core.dump import plain
from ....reg import reg_object, reg_object1, set_object
from ....reg.result import *
from ..auto_funcs import call
from .backwardcompat import *
from .db import link_objects
from .data_funcs import get_list
from .sheet_funcs import get_value, get_index
from .xlrd_macro import search_regexp


def e_func(func_name, e, *args, **kargs):
    OBJ = args[3]
    e = "/Error in '{0}'/ {1}".format(func_name, e)
    reg_exception(OBJ, e, *args, **kargs)


def proceed_marks(sh, marks_values, SHEET):
    MARKS = set_object("Marks", SHEET)

    marks_dict = {}
    test = ""

    last_y, last_x = None, None
    for value_list in marks_values:
        l = len(value_list)
        if l == 2:
            key, needle = value_list

            yx = search_regexp(sh, needle)
            if yx:
                last_y, last_x = yx
                marks_dict[key+'_x'] = last_x
                marks_dict[key+'_y'] = last_y

                val = get_value(sh, last_y, last_x)
                marks_dict[key] = val

                val_list = []

                res = re.match(needle, val, re.UNICODE)
                if res:
                    val_list = list(res.groups())

                for i in range(last_x + 1, sh.ncols):
                    val2 = get_value(sh, last_y, i)
                    if val2:
                        val_list.append(val2)

                marks_dict[key+'_list'] = val_list

                test += "{0} [{1}]: ({2},{3}) {4} + {5}\n".format(key, plain(needle), last_y, last_x, plain(val), plain(val_list))

            else:
                last_y, last_x = None, None
                marks_dict[key+'_x'] = last_x
                marks_dict[key+'_y'] = last_y

                test += "{0} [{1}]: Выражение не найдено!\n".format(key, plain(needle))
                reg_error(SHEET, "Выражение не найдено: '{0}', зависимые ячейки не будут вычисляться!".format(needle))

        elif l == 3:
            key, y, x = value_list
            if isinstance(x, string_types) and last_x is not None:
                x = last_x + int(x)
            if isinstance(y, string_types) and last_y is not None:
                y = last_y + int(y)

            if isinstance(x, int) and isinstance(y, int):
                val = get_value(sh, y, x)
                marks_dict[key] = val

                test += "{0} [{1},{2}]: {3}\n".format(key, y, x, plain(val))
            else:
                test += "{0} [{1},{2}]: Координата не вычислена!\n".format(key, y, x)

        elif l == 6:
            key, needle, y1, x1, y2, x2 = value_list

            last_y, last_x = None, None
            marks_dict[key+'_x'] = last_x
            marks_dict[key+'_y'] = last_y

            if isinstance(x1, string_types):
                if marks_dict[x1+'_x'] is None:
                    continue
                x1 = marks_dict[x1+'_x'] + 1
            if isinstance(x2, string_types):
                if marks_dict[x2+'_x'] is None:
                    continue
                x2 = marks_dict[x2+'_x']
            if isinstance(y1, string_types):
                if marks_dict[y1+'_y'] is None:
                    continue
                y1 = marks_dict[y1+'_y'] + 1
            if isinstance(y2, string_types):
                if marks_dict[y2+'_y'] is None:
                    continue
                y2 = marks_dict[y2+'_y']

            yx = search_regexp(sh, needle, y1, x1, y2, x2)
            if yx:
                last_y, last_x = yx
                marks_dict[key+'_x'] = last_x
                marks_dict[key+'_y'] = last_y

                val = get_value(sh, last_y, last_x)
                marks_dict[key] = val

                val_list = []

                res = re.match(needle, val, re.UNICODE)
                if res:
                    val_list = list(res.groups())

                for i in range(last_x + 1, sh.ncols):
                    val2 = get_value(sh, last_y, i)
                    if val2:
                        val_list.append(val2)

                marks_dict[key+'_list'] = val_list

                test += "{0} [{1},{2},{3},{4},{5}]: ({6},{7}) {8} + {9}\n".format(key, plain(needle), y1, x1, y2, x2, last_y, last_x, plain(val), plain(val_list))

            else:
                test += "{0} [{1},{2},{3},{4},{5}]: Выражение не найдено!\n".format(key, plain(needle), y1, x1, y2, x2)
                reg_error(SHEET, "Выражение не найдено: '{0}', зависимые ячейки не будут вычисляться!".format(needle))

    reg_debug(MARKS, test)

    return marks_dict


def parse_doc(sh, doc_options, session, models, marks_dict, SHEET):
    doc_plains = doc_options.get('doc_plains', [])
    doc_values = doc_options.get('doc_values', [])
    doc_funcs  = doc_options.get('doc_funcs',  [])

    doc_objects  = get_list(doc_options.get('doc_objects'))
    doc_objects1 = get_list(doc_options.get('doc_objects1'))

    object_required = doc_options.get('object_required', {})
    object_keys     = doc_options.get('object_keys', {})

    # Plains
    doc_dict = dict((key, value) for (key, value) in doc_plains)

    # Values
    for value_list in doc_values:
        key, ref_key = value_list
        d = dict([(key+i, marks_dict[ref_key+i])
            for i in ['', '_list', '_x', '_y'] if ref_key+i in marks_dict])
        doc_dict.update(d)

    # Funcs
    remarks = {}
    for func_list in doc_funcs:
        key = func_list[0]
        func_list = func_list[1:]
        for func_name in func_list:
            remarks1 = []
            call(func_name, doc_dict, key, remarks1, SHEET, error_callback=e_func)
            if remarks1:
                remarks[func_name+'/'+key] = remarks1

    if remarks:
        reg_warning(SHEET, remarks)
        SHEET.remarks = remarks

    # Set Object
    if doc_dict:
        doc_plain = plain(doc_dict)

        ROWS = []

        doc_dict['_sheet'] = SHEET

        for doc_object in doc_objects:
            try:
                Object = getattr(models, doc_object)
            except:
                OBJECT = set_object(doc_dict, SHEET)
                reg_error(OBJECT, "Модель не найдена: '{0}'!".format(doc_object))
            else:
                OBJECT = reg_object(session, Object, doc_dict, SHEET)
                ROWS.append(OBJECT)

                reg_debug(OBJECT, doc_plain)

        for doc_object in doc_objects1:
            try:
                Object = getattr(models, doc_object)
            except:
                OBJECT = set_object(doc_dict, SHEET)
                reg_error(OBJECT, "Модель не найдена: '{0}'!".format(doc_object))
            else:
                required = object_required.get(doc_object)
                keys = object_keys.get(doc_object)
                OBJECT = reg_object1(session, Object, doc_dict, SHEET, required=required, keys=keys)
                ROWS.append(OBJECT)

                reg_debug(OBJECT, doc_plain)

        if ROWS:
            link_objects(*ROWS)

            # Parse tables
            if 'table' in doc_options:
                table_options = doc_options['table']
                set_object("Doc/Table (options)", SHEET, brief=table_options)
                parse_table(sh, table_options, session, models, marks_dict, SHEET, ROWS)

            if 'tables' in doc_options:
                for table_options in doc_options['tables']:
                    set_object("Doc/Tables (options)", SHEET, brief=table_options)
                    parse_table(sh, table_options, session, models, marks_dict, SHEET, ROWS)

        else:
            OBJECT = set_object(doc_dict, SHEET)

    else:
        OBJECT = set_object("No doc", SHEET)


def parse_table(sh, options, session, models, marks_dict, SHEET, DOC_ROWS=[]):
    for row_dict, ROWS in parse_table_iter(sh, options, session, models, marks_dict, SHEET):
        if ROWS:
            ROWS.extend(DOC_ROWS)
            link_objects(*ROWS)


def parse_table_iter(sh, options, session, models, marks_dict, SHEET):
    TABLE = set_object("Table", SHEET)

    table_objects  = get_list(options.get('table_objects'))
    table_objects1 = get_list(options.get('table_objects1'))

    object_required = options.get('object_required', {})
    object_plains   = options.get('object_plains', {})
    object_override = options.get('object_override', {})
    object_keys     = options.get('object_keys', {})

    row_start      = options.get('row_start', 0)
    row_start_skip = options.get('row_start_skip', 0)
    row_stop       = options.get('row_stop', sh.nrows)
    row_stop_skip  = options.get('row_stop_skip', 0)

    col_mode  = options.get('col_mode', 'column')
    col_names = options.get('col_names', [])
    col_funcs = options.get('col_funcs', {})

    check_name = options.get('check_name')
    col_index1 = col_names.index(check_name) if check_name else None

    check_column = options.get('check_column')
    col_index2 = get_index(check_column) if check_column else None

    typical_index = col_index1 or col_index2

    if isinstance(row_start, string_types):
        row_start = marks_dict[row_start+'_y']

        if row_start is None:
            reg_error(TABLE, "row_start не вычислено, таблица не обрабатывается!")
            return

    row_start += row_start_skip
    TABLE.row_start = row_start

    if isinstance(row_stop, string_types):
        row_stop = marks_dict[row_stop+'_y']

        if row_stop is None:
            reg_error(TABLE, "row_stop не вычислено, таблица не обрабатывается!")
            return

    row_stop -= row_stop_skip
    TABLE.row_stop = row_stop

    for j in range(row_start, row_stop):
        row_dict = {}
        typical_column = get_value(sh, j, typical_index) if typical_index else True
        if typical_column:
            test = "Номер строки: {0}\n".format(j)

            if col_mode == 'column':
                i = 0
                for col_name in col_names:
                    if col_name:
                        if isinstance(col_name, string_types):
                            val = get_value(sh, j, i)
                            row_dict[col_name] = val
                            test += "({0}:{1}) {2}: {3} /{4!r}/\n".format(j, i, col_name, val, val)

                        elif isinstance(col_name, list):
                            inner_row = 0
                            for inner_col_name in col_name:
                                if inner_col_name:
                                    val = get_value(sh, j + inner_row, i)
                                    row_dict[inner_col_name] = val
                                    test += "({0}:{1}+{2}) {3}: {4} /{5!r}/\n".format(j, i, inner_row, inner_col_name, val, val)
                                inner_row += 1
                    i += 1

            elif col_mode == 'value':
                col = 0
                for i in range(sh.ncols):
                    val = get_value(sh, j, i)
                    if val:
                        col_name = col_names[col]
                        row_dict[col_name] = val
                        test += "({0}:{1}) {2}: {3} /{4!r}/\n".format(j, i, col_name, val, val)
                        col += 1
                        if col > len(col_names):
                            break

            else:
                raise Exception("Undefined column mode: {0}".format(col_mode))

            # Funcs
            remarks = {}
            for func_list in col_funcs:
                key = func_list[0]
                func_list = func_list[1:]
                for func_name in func_list:
                    remarks1 = []
                    call(func_name, row_dict, key, remarks1, TABLE, error_callback=e_func)
                    if remarks1:
                        remarks[func_name+'/'+key] = remarks1

            if remarks:
                reg_warning(TABLE, remarks)
                TABLE.remarks = remarks

#           test_row = ''
#           for i in range(sh.ncols):
#               val = get_value(sh, j, i)
#               test_row += "({0}): {1} /{2!r}/\n".format(i, val, val)
#           row_dict['test_row'] = test_row

            # Set Object
            if row_dict:
#               reg_debug(TABLE, row_dict)
                reg_debug(TABLE, table_objects1)
                reg_debug(TABLE, table_objects)
                reg_debug(TABLE, "---")
                ROWS = []

                row_dict['_sheet'] = SHEET
                row_dict['dir'] = SHEET._file._dir.name   # !!!
                row_dict['file'] = SHEET._file.name       # !!!
                row_dict['y'] = j

                for table_object in table_objects:
                    try:
                        Object = getattr(models, table_object)
                    except:
                        OBJECT = set_object(row_dict, TABLE)
                        reg_error(OBJECT, "Модель не найдена: '{0}'!".format(table_object))
                    else:
                        required = object_required.get(table_object, [])
                        plains   = object_plains.get(table_object, [])
                        override = object_override.get(table_object, [])

#                       OBJECT = reg_object(session, Object, row_dict, TABLE,
#                           required=required, plains=plains, override=override)
                        OBJECT = reg_object(session, Object, row_dict, TABLE,
                            required=required)
                        ROWS.append(OBJECT)

                    reg_debug(OBJECT, test)

                for table_object in table_objects1:
                    try:
                        Object = getattr(models, table_object)
                    except:
                        OBJECT = set_object(row_dict, TABLE)
                        reg_error(OBJECT, "Модель не найдена: '{0}'!".format(table_object))
                    else:
                        required = object_required.get(table_object, [])
                        plains   = object_plains.get(table_object, [])
                        override = object_override.get(table_object, [])
                        keys     = object_keys.get(table_object, [])

                        OBJECT = reg_object1(session, Object, row_dict, TABLE,
                            required=required, plains=plains, override=override, keys=keys)
                        ROWS.append(OBJECT)

                    reg_debug(OBJECT, test)

                if ROWS:
                    yield row_dict, ROWS
                else:
                    row_dict['name'] = 'Несохранённый элемент таблицы'
                    OBJECT = set_object(row_dict, TABLE)

            else:
                OBJECT = set_object("No table", TABLE)
