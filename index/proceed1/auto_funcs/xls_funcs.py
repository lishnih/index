#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )
from lib.backwardcompat import *

import re

from ..lib.sheet_funcs import get_date


def prepare_str(_dict, item, remarks):
    val = _dict.get(item)
    if val and isinstance(val, string_types):
        _dict[item] = re.sub('[ \n\t]+', ' ', val.strip())


def proceed_int(_dict, item, remarks):
    val = _dict.get(item)
    if val == None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    else:
        try:
            _dict[item] = int(val)
        except:
            _dict[item] = None
            remarks.append(val)


def proceed_int_str(_dict, item, remarks):
    val = _dict.get(item)
    if val == None:
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


def proceed_float(_dict, item, remarks):
    val = _dict.get(item)
    if val == None:
        return
    elif val == '' or val == '-' or val == '---':
        _dict[item] = 0
    else:
        try:
            _dict[item] = float(val)
        except:
            _dict[item] = None
            remarks.append(val)


def proceed_date(_dict, item, remarks):
    val = _dict.get(item)
    if val:
        try:
            date, date_str = get_date(val)
            _dict[item] = date
            _dict[item+'_str'] = date_str
        except:
            _dict[item] = None
            remarks.append(val)


def iter_joints(_dict, item, remarks):
    val = _dict.get(item)
    joint_list = val.split(';')
    return 'joint', joint_list, 'proceed_joint'


def proceed_joint(_dict, item, remarks):
    val = _dict.get(item)
    _dict[item+'_pre']  = None
    _dict[item+'_line'] = None
    _dict[item+'_seq']  = None

    if isinstance(val, numeric_types):
        val = unicode(val)

    if val:
        res = re.match('([^-]+)-(.+)-(\d+)', val, re.UNICODE)
        if res:
            joint_pre, joint_line, joint_seq = res.groups()
            _dict[item+'_pre']  = joint_pre
            _dict[item+'_line'] = joint_line
            _dict[item+'_seq']  = joint_seq
            return

        res = re.match('(\d+)-(\d+)', val)
        if res:
            joint_pre, joint_seq = res.groups()
            _dict[item+'_pre']  = joint_pre
            _dict[item+'_seq']  = joint_seq
            return

        res = re.match('(.+) *стык № *(\d+)', val)
        if res:
            joint_pre, joint_seq = res.groups()
            _dict[item+'_pre']  = joint_pre
            _dict[item+'_seq']  = joint_seq
            return

    remarks.append(val)


def proceed_d_w_th(_dict, item, remarks):
    val = _dict.get(item)
    _dict['diameter1']  = None
    _dict['thickness1'] = None
    _dict['diameter2']  = None
    _dict['thickness2'] = None

    if val:
        if val == '---':
            return

        if isinstance(val, string_types):
            res = re.match('(?:Ду)?(\d+)[×XХxх ]*(\d*) *(?:/(?:Ду)?(\d+)[×XХxх ]*(\d*))?', val)
            if res:
                d1, th1, d2, th2 = res.groups()
                if d1:  _dict['diameter1']  = d1
                if th1: _dict['thickness1'] = th1
                if d2:  _dict['diameter2']  = d2
                if th2: _dict['thickness2'] = th2
                return

            res = re.match('(\d+\.?\d*)', val)
            if res:
                th1, = res.groups()
                _dict['thickness1'] = float(th1)
                return

        elif isinstance(val, (float, int)):
            _dict['thickness1'] = val
            return

    remarks.append(val)


def proceed_doc_w_date(_dict, item, remarks):
    _dict['doc_pre']  = None
    _dict['doc_seq']  = None
    _dict['doc_sign'] = None
    _dict['date']     = None
    _dict['date_str'] = None

    val = _dict.get(item)
    if val:
        res = re.match('(.*) от (.*)', val)
        if res:
            doc_str, date_str = res.groups()

            date, date_str = get_date(date_str)
            _dict['date'] = date
            _dict['date_str'] = date_str

            _dict['doc'] = doc_str
            res = re.match('(?:(.*)/)?(.*)', doc_str)
            if res:
                doc_pre, doc_seq = res.groups()

                _dict['doc_pre'] = doc_pre
                _dict['doc_seq'] = doc_seq
            return

    remarks.append(val)


def prepare_piece(_dict, item, remarks):
    if 'piece_type' not in _dict:
        _dict['piece_type'] = None
    if 'piece_scheme' not in _dict:
        _dict['piece_scheme'] = None
    name_list = filter(lambda x: x, [_dict['piece_type'], _dict['piece_name'], _dict['piece_scheme']])
    name_list = map(unicode, name_list)
    _dict['piece'] = " ".join(name_list)


def prepare_doc_vt_act(_dict, item, remarks):
    _dict['type'] = "Акт ВК"

    val = _dict.get(item)
    if val:
        _dict['doc_pre'] = ""
        _dict['doc_seq'] = val


def prepare_doc_invoice(_dict, item, remarks):
    _dict['type'] = "Накладная"

    val = _dict.get(item)
    if val:
        _dict['doc_pre'] = ""
        _dict['doc_seq'] = val


def prepare_dt_doc_name(_dict, item, remarks):
    _dict['type'] = "Протокол МИ"

    name_list = _dict[item+'_list']
    if name_list:
        pre, null, seq = name_list

        _dict['doc_pre'] = pre
        _dict['doc_seq'] = seq
