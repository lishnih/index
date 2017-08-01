#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-06

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import re, logging

from .backwardcompat import *


def get_list(val):
    if val == None:
        return []
    elif isinstance(val, (list, tuple)):
        return val
    else:
        return [val]

    return []


def get_str_sequence(sequence_str):
    str_sequence = []

#   sequence_list = sequence_str.split(',')
#   for i in sequence_list:
#       if i:
#           i = i.strip()
#           str_sequence.append(i)

    sequence_list = re.findall('(")?(?(1)(.*?)|([^",]+))((?(1)"))[, ]*', sequence_str)
    for q1, i1, i2, q2 in sequence_list:
        i = i2.strip() if i2 else i1
        str_sequence.append(i)

    return str_sequence


def get_int_sequence(sequence_str, from_list=None):
    from_len = None if from_list == None else len(from_list)

    int_sequence = []
    str_sequence = get_str_sequence(sequence_str)
    for i in str_sequence:
        nosequence = True
        if i.isdigit():
            if not i == '0':
                i = int(i) - 1
                if i not in int_sequence:
                    int_sequence.append(i)
                nosequence = False
        else:
            res = re.match('^(\d*)-(\d*):?(\d*)$', i)
            if res:
                start, stop, step = res.group(1, 2, 3)
                start = int(start) - 1 if start else 0
                stop  = int(stop)      if stop  else from_len
                step  = int(step)      if step  else 1

            else:
                res = re.match('^(\d*):(-?\d*):?(\d*)$', i)
                if res:
                    start, stop, step = res.group(1, 2, 3)
                    start = int(start)    if start else 0
                    stop  = int(stop) + 1 if stop  else from_len
                    step  = int(step)     if step  else 1

                    if stop <= 0:
                        if from_len == None:
                            raise ValueError("Impossible to calculate the count of array! Array is not defined!")
                        stop = from_len - stop - 1

            if res:
                if stop == None:
                    raise ValueError("Impossible to calculate the count of array! Array is not defined!")

                for i in range(start, stop, step):
                    if i not in int_sequence:
                        int_sequence.append(i)
                nosequence = False

        if nosequence:
            raise ValueError("Wrong expression: '{0}'".format(i))

    int_sequence.sort()
    return int_sequence


def filter_match(name, filter, index=None):
    if filter == None:
        return True

    elif isinstance(filter, string_types):

        # Строка вида [i0, i1] интерпретируется как массив индексов
        res = re.match('^\[(.*)\]$', filter)
        if res:
            filter = res.group(1)
            index_list = get_int_sequence(filter)

            if index == None:
                assert None, 'index required!'
                return False

            return index in index_list

        # Строка вида (name0, name1) - как массив имён
        res = re.match('^\((.*)\)$', filter)
        if res:
            filter = res.group(1)
            names_list = get_str_sequence(filter)

            return name in names_list

        # Строка вида /patt/ - как шаблон
        res = re.match('^/(.*)/$', filter)
        if res:
            filter = res.group(1)

            return True if re.match(filter, name) else False

        # Все остальные строки принимаются как есть
        return filter == name

    elif isinstance(filter, list):

        return name in filter
