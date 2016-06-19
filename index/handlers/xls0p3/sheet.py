#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging
from sqlalchemy import MetaData

from ...reg import reg_object1
from ...reg.result import *
from .lib.backwardcompat import *
from .lib import models
from .lib.sheet_funcs import get_value, get_index


def suit_name(colname, column_names):
    i = 1
    while "{0}.{1}".format(colname, i) in column_names:
        i += 1

    return "{0}.{1}".format(colname, i)


def insert_dict(names, bind_dict):
    sql = u"INSERT INTO %s (%s) VALUES (%s)" % (table_name, keys, values)


def reg_sheet(sh, runtime, i, FILE=None):
    sheet_dict = dict(
        _file   = FILE,
#       _fileprocessing = FILE,
        name    = sh.name,
        seq     = i,
        ncols   = sh.ncols,
        nrows   = sh.nrows,
        visible = sh.visibility,
    )

    session = runtime.get('session')
    if session:
        SHEET = reg_object1(session, models.Sheet, sheet_dict, FILE)
    else:
        SHEET = set_object(basename, FILE, brief=sheet_dict)

    return SHEET, session


def proceed_sheet(sh, runtime, i, FILE=None):
    SHEET, session = reg_sheet(sh, runtime, i, FILE)

    if not session:
        return

    options = runtime.get('options', {})

    flush = options.get('flush')
    tablename = options.get('tablename')
    prefix = options.get('prefix', 'xls')
    isolated = options.get('isolated')
    names_row = options.get('names_row')
    names = options.get('names', [])

    ncols = options.get('ncols', sh.ncols)
    nrows = options.get('nrows', sh.nrows)
    start_from = options.get('start_from', 0)

    if tablename and isolated:
        tablename = '{0}_{1}'.format(tablename, i)

    if not tablename:
        tablename = sh.name

    if flush or isolated:
        session.flush()

    if isolated:
        tablename = '{0}_{1}'.format(FILE.id, tablename)

    if prefix:
        tablename = '{0}_{1}'.format(prefix, tablename)

    sh_column_names = []
    w = len(str(ncols))

    # Выбираем названия колонок, если указана соответствующая строка
    if names_row != None and sh.nrows > names_row:
        for j in range(sh.ncols):
#           colname = sh.cell(names_row, j).value
            colname = get_value(sh, names_row, j)
            if colname:
                if isinstance(colname, float):
                    colname = 'cf_{0}'.format(colname)

                if names and colname not in names:
                    reg_warning(SHEET, "Extra column name '{0}' found in sheet!".format(colname))

            else:
                colname = 'col_{0:0{width}}'.format(j, width=w)

            if colname in sh_column_names:
                if colname in names:
                    reg_warning(SHEET, "Possibly another column '{0}' will get lost!".format(colname))

                colname = suit_name(colname, sh_column_names)
            sh_column_names.append(colname)

    sh_column_names = sh_column_names + ['col_{0:0{width}}'.format(j, width=w) for j in range(len(sh_column_names), ncols)]

    # Определяемся с колонкой, по которой будут выбираться строки для записи
    col_index = None
    check_name = options.get('check_name')
    check_column = options.get('check_column')

    if check_name:
        if check_name in sh_column_names:
            col_index = sh_column_names.index(check_name)
        else:
            msg = "Column '{0}' is not in the list of column names".format(check_name)
            logging.warning(msg)
            reg_warning(SHEET, msg)

    if check_column:
        if col_index is None:
            col_index = get_index(check_column)
        else:
            msg = "Parameters 'check_name' and 'check_column' set simultaneously!"
            logging.warning(msg)
            reg_warning(SHEET, msg)

    # Выбираем из таблицы название колонок, если требуется сопоставление
    if names:
        metadata = MetaData(session.bind, reflect=True)
        if tablename in metadata.tables.keys():
            mtable = metadata.tables.get(tablename)
            column_names0 = [i.name for i in mtable.c][4:]
        else:
            column_names0 = names
    else:
        column_names0 = sh_column_names

    # Добавляем системные колонки
    column_names = ['dir', 'file', 'sheet', '_sheets_id'] + column_names0
    tablecols = len(column_names)

    sql = 'CREATE TABLE IF NOT EXISTS "{0}" ("{1}");'.format(tablename, '","'.join(column_names))
    session.execute(sql)

    reg_debug(SHEET, column_names)

    # В общем, случается такой баг, что если обрабатываются два файла с одинаковым именем листа,
    # и во втором листе будет больше колонок, то получим ошибку

    if sh.nrows > start_from:
        qmarks = ['?' for i in range(tablecols)]
        sql = 'INSERT INTO "{0}" VALUES ({1});'.format(tablename, ','.join(qmarks))
        for i in range(start_from, sh.nrows):
            needful = get_value(sh, i, col_index) if not col_index is None else True
            if needful:
                sh_values = sh.row_values(i, 0, ncols)

                if names:
                    bind_params = []
                    for i in column_names0:
                        if i in sh_column_names:
                            bind_params.append(sh_values[sh_column_names.index(i)])
                        else:
                            bind_params.append(None)
                else:
                    bind_params = sh_values
                    l = len(sh_values)
                    if ncols > l:
                        bind_params = sh_values + [None for i in range(ncols - l)]

                bind_params = [FILE._dir.name, FILE.name, SHEET.name, SHEET.id] + bind_params
                session.bind.execute(sql, bind_params)

#   reg_debug(SHEET, bind_params)
    reg_ok(SHEET)
