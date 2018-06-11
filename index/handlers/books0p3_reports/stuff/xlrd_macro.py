#!/usr/bin/env python
# coding=utf-8
# Stan 2007-10-10, 2012-10-28

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import re
import xlrd                     # XLS reader

from .backwardcompat import *


"""
Интерфейс для работы c модулем xlrd
"""


# Возращает значение из ячейки [row, col] листа sh
# Это упрощённая функция и предназначена для использования в пределах этого модуля
def get_value(sh, row, col):
    try:
        cell_type = sh.cell_type(row, col)
        val = None if cell_type == xlrd.XL_CELL_ERROR else \
              sh.cell_value(row, col)
        if isinstance(val, string_types):
            val = val.strip()
    except IndexError:
        val = None

    return val


# Сравнивает ячейку [row, col] в листе sh с регулярным выражением seaching_regexp
# Возращает найденное по шаблону или None в противном случае
def contain_regexp(sh, row, col, seaching_regexp):
    val = get_value(sh, row, col)
    if val:
        val = unicode(val)
        result = re.search(seaching_regexp, val)
        return result

    return


# Ищет значение search в листе sh
# Возращает [row, col] если нашёл и None в противном случае
# sh - лист; seaching_regexp - регулярное выражение для поиска
def search_regexp(sh, seaching_regexp, y1=None, x1=None, y2=None, x2=None):
    if x1 is None:
        x1 = 0
    if x2 is None:
        x2 = sh.ncols
    if y1 is None:
        y1 = 0
    if y2 is None:
        y2 = sh.nrows

    for i in range(x1, x2):
        for j in range(y1, y2):
            if contain_regexp(sh, j, i, seaching_regexp):
                return j, i

    return
