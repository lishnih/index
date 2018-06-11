#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import re
import time
import calendar
import logging

import xlrd

from .backwardcompat import *


def get_int(sh, row, col, default=0):
    val = get_value(sh, row, col)
    if isinstance(val, int):
        return val
    elif isinstance(val, string_types):
        return int(val) if val.isdigit() else default
    return default


def get_str(sh, row, col):
    val = get_value(sh, row, col)
    return unicode(val)


def in_crange(row, col, crange):
    rlo, rhi, clo, chi = crange
    return 1 if row > rlo and row < rhi and col == clo else 0


# Возращает значение из ячейки [row, col] листа sh
def get_value(sh, row, col):
    # Этот блок проверяет, не является ли требуемая ячейка объединённой с другой ячейкой
    for crange in filter(lambda crange: in_crange(row, col, crange), sh.merged_cells):
        rlo, rhi, clo, chi = crange
        row, col = rlo, clo

    try:
        cell_type = sh.cell_type(row, col)
        val = None if cell_type == xlrd.XL_CELL_ERROR else sh.cell_value(row, col)
        if isinstance(val, string_types):
            val = val.strip()
    except IndexError:
        val = None
    return val


def get_index(letter):
    index_len = len(letter)
    if index_len == 1:
        return ord(letter.upper()) - 65
    else:
        i1 = (get_index(letter[0:-1]) + 1) * 26
        i2 = get_index(letter[-1])
        return i1 + i2


def get_date(date_str):
    date = 0
    try:            # пытаемся распознать дату из числа
        date_tuple = xlrd.xldate_as_tuple(int(date_str), 0)
        date_list = list(date_tuple)
        date_list.extend([0, 0, 0])
        date = int(time.mktime(date_list))
        date_str = "{0:02}.{1:02}.{2:02}".format(date_list[2], date_list[1], date_list[0])
    except:         # дата, возможно, записана в текстовом формате
        res = re.search(r"(\d{1,2}).(\d{1,2}).(\d{4}|\d{2})", date_str)
        if res:
            reslist = res.groups()
            day, month, year = reslist
            date_str = "{0}.{1}.{2}".format(day, month, year)
            year = int(year)
            date = calendar.timegm(time.strptime(date_str, "%d.%m.%Y")) if year >= 100 else \
                   calendar.timegm(time.strptime(date_str, "%d.%m.%y"))

    return date, date_str
