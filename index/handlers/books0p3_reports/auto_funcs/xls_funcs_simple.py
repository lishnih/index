#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-07

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import re

from ..stuff.backwardcompat import string_types


def prepare_str(_dict, item, remarks, *args, **kargs):
    val = _dict.get(item)

    if val and isinstance(val, string_types):
        _dict[item] = re.sub('[ \n\t]+', ' ', val.strip())


def proceed_int(_dict, item, remarks, *args, **kargs):
    val = _dict.get(item)

    if val is None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    else:
        try:
            _dict[item] = int(val)
        except:
            _dict[item] = None
            remarks.append(val)


def proceed_int_str(_dict, item, remarks, *args, **kargs):
    val = _dict.get(item)

    if val is None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    elif isinstance(val, string_types):
        _dict[item] = int(val) if val.isdigit() else val
    else:
        try:
            _dict[item] = int(val)
        except:
            _dict[item] = repr(val)


def proceed_float(_dict, item, remarks, *args, **kargs):
    val = _dict.get(item)

    if val is None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    else:
        if isinstance(val, string_types):
            val = val.replace(',', '.')
        try:
            _dict[item] = float(val)
        except:
            _dict[item] = None
            remarks.append(val)
