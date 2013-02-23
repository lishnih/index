#!/usr/bin/env python
# coding=utf-8
# Stan 2012-09-01

import xlrd

from models import DBSession
from models.links import link_objects
from reg import reg_object, reg_object1
from reg.result import reg_warning, reg_error, reg_exception
from auto_funcs import call
from lib.data_funcs import get_list
from lib.sheet_funcs import get_value, get_index
from lib.xlrd_macro import search_value


def e_func(func_name, Exception, e, *args, **kargs):
    OBJ = args[2]
    e = "/Error in '{}'/ {}".format(func_name, e)
    reg_exception(OBJ, Exception, e, *args, **kargs)


def parse_doc(sh, options, SHEET):
    doc_values = options.get('doc_values', [])
    doc_funcs  = options.get('doc_funcs', {})

    doc_objects  = get_list(options.get('doc_objects'))
    doc_objects1 = get_list(options.get('doc_objects1'))

    TASK = SHEET._file._dir._task
    doc_dict = dict(_task=TASK)
    test = ''

    last_y, last_x = None, None
    for key, params in doc_values:
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
                test += u"{} [{},{}]: '{}' + '{!r}'\n".format(key, last_y, last_x, val, val_list)
            else:
                reg_warning(SHEET, u"Значение не найдено: '{}', пропускаем лист!".format(params))
                return
        elif l == 2:
            y, x = params
            if isinstance(x, basestring):
                x = last_x + int(x)
            if isinstance(y, basestring):
                y = last_y + int(y)
            val = get_value(sh, y, x)
            doc_dict[key] = val
            test += u"{} [{},{}]: '{}'\n".format(key, y, x, val)
        elif l == 3:
            y, x = params
            if isinstance(x, basestring):
                x = last_x + int(x)
            if isinstance(y, basestring):
                y = last_y + int(y)
            val = get_value(sh, y, x)
            doc_dict[key] = val
            test += u"{} [{},{},{}]: '{}'\n".format(key, y, x, pattern, val)

    for item, funcs_name in doc_funcs.items():
        for func_name in get_list(funcs_name):
            call(func_name, doc_dict, item, SHEET, error_callback=e_func)

    if test:
        doc_dict['test'] = test

    if doc_dict:
        ROWS = []
        for doc_object in doc_objects:
            ROWS.append(reg_object(doc_object, doc_dict, SHEET))
        for doc_object in doc_objects1:
            ROWS.append(reg_object1(doc_object, doc_dict, SHEET))

        link_objects(SHEET, *ROWS)


def parse_table(sh, options, SHEET):
    for i in parse_table_iter(sh, options, SHEET):
        pass


def parse_table_iter(sh, options, SHEET):
    row_start      = options.get('row_start', 1)
    row_start_skip = options.get('row_start_skip', 0)
    row_stop       = options.get('row_stop', sh.nrows)
    row_stop_skip  = options.get('row_stop_skip', 0)
    col_names      = options.get('col_names', [])
    col_funcs      = options.get('col_funcs', {})

    check_name = options.get('check_name')
    col_index1 = col_names.index(check_name) if check_name else None

    check_column = options.get('check_column', 'A')
    col_index2 = get_index(check_column)

    typical_index = col_index1 or col_index2

    row_objects  = get_list(options.get('row_objects'))
    row_objects1 = get_list(options.get('row_objects1'))

    if isinstance(row_start, basestring):
        yx = search_value(sh, row_start)
        if not yx:
            reg_warning(SHEET, u"Начало таблицы не найдено: '{}', пропускаем лист!".format(row_start))
            return
        row_start = yx[0] + 1 + row_start_skip
        SHEET.row_start = row_start
    else:
        row_start = row_start - 1

    if isinstance(row_stop, basestring):
        yx = search_value(sh, row_stop)
        if not yx:
            reg_warning(SHEET, u"Конец таблицы не найден: '{}', индексируем весь лист!".format(row_stop))
            row_stop = sh.nrows
        else:
            row_stop = yx[0] - row_stop_skip
        SHEET.row_stop = row_stop

    for j in xrange(row_start, row_stop):
        typical_column = get_value(sh, j, typical_index)
        if typical_column:
            TASK = SHEET._file._dir._task
            row_dict = dict(_task=TASK, j=j)
            test = ''

            col = 0
            for col_name in col_names:
                if col_name:
                    if isinstance(col_name, basestring):
                        val = get_value(sh, j, col)
                        row_dict[col_name] = val
                        test += u"({}:{}) '{}': '{}'\n".format(j, col, col_name, val)
                    if isinstance(col_name, list):
                        inner_row = 0
                        for inner_col_name in col_name:
                            if inner_col_name:
                                val = get_value(sh, j + inner_row, col)
                                row_dict[inner_col_name] = val
                            inner_row += 1
                col += 1

            for item, funcs_name in col_funcs.items():
                for func_name in get_list(funcs_name):
                    call(func_name, row_dict, item, SHEET, error_callback=e_func)

            if test:
                row_dict['test'] = test

#             test_row = ''
#             for i in xrange(sh.ncols):
#                 val = get_value(sh, j, i)
#                 test_row += u"({}): '{}'\n".format(i, val)
#             row_dict['test_row'] = test_row

            if row_dict:
                ROWS = []
                for row_object in row_objects:
                    ROWS.append(reg_object(row_object, row_dict, SHEET))
                for row_object in row_objects1:
                    ROWS.append(reg_object1(row_object, row_dict, SHEET))

#                 try:
#                     DBSession.commit()
#                 except Exception, e:
#                     reg_exception(SHEET, Exception, e, name, source)

                link_objects(SHEET, *ROWS)

                yield row_dict, ROWS