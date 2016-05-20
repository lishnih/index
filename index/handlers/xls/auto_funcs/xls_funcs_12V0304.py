#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import re

from ..lib.backwardcompat import numeric_types, string_types
from ..lib.sheet_funcs import get_date


def proceed_date(_dict, item, remarks, *args, **kargs):
#   val = _dict.get(item)

    val_list = _dict.get(item+'_list', [])
    val = val_list[0] if len(val_list) else None

    if val:
        try:
            date, date_str = get_date(val)
            _dict[item] = date
            _dict[item+'_str'] = date_str
            return
        except:
            pass

    _dict[item] = None
    remarks.append(val)


def proceed_doc_date(_dict, item, remarks, *args, **kargs):
#   val = _dict.get(item)

    val_list = _dict.get(item+'_list', [])

    val = val_list[2] if len(val_list) > 2 else None
    if val:
        try:
            date, date_str = get_date(val)
            _dict['date'] = date
            _dict['date_str'] = date_str
        except:
            pass

    val = val_list[0] if len(val_list) else None
    if val:
        if isinstance(val, float):
            val = int(val)

        _dict['doc'] = val
        return

    _dict['doc'] = None
    _dict['date'] = None
    remarks.append(val)


def proceed_doc(_dict, item, remarks, *args, **kargs):
#   val = _dict.get(item)

    val_list = _dict.get(item+'_list', [])
    val = val_list[0] if len(val_list) else None

    if val:
        if isinstance(val, float):
            val = int(val)

        _dict[item] = val
        return

    _dict[item] = None
    remarks.append(val)


def proceed_doc_2(_dict, item, remarks, *args, **kargs):
#   val = _dict.get(item)

    val_list = _dict.get(item+'_list', [])
    val = val_list[1] if len(val_list) > 1 else None

    if val:
        if isinstance(val, float):
            val = int(val)

        _dict[item] = val
        return

    _dict[item] = None
    remarks.append(val)


def proceed_joint(_dict, item, remarks, *args, **kargs):
    val = _dict.get(item)

#   val_list = _dict.get(item+'_list', [])
#   val = val_list[0] if len(val_list) else None

    if val:
        if isinstance(val, numeric_types):
            _dict[item+'_seq'] = int(val)
            _dict[item] = unicode(int(val))
            return

        res = re.match('(^[^-]*?)[ -]*(\d+) ?([^-]*)$', val, re.UNICODE)
        if res:
            joint_pre1, joint_seq, joint_sign1 = res.groups()
            _dict[item+'_pre1']  = joint_pre1
#           _dict[item+'_pre2']  = joint_pre2
            _dict[item+'_seq']   = joint_seq
            _dict[item+'_sign1'] = joint_sign1
#           _dict[item+'_sign2'] = joint_sign2

            _dict[item] = joint_pre1 + '-' + joint_seq
            if joint_sign1:
                _dict[item] += ' ' + joint_sign1
            return

    _dict[item] = None
    remarks.append(val)
