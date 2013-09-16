#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os
import xlrd

from ..reg import reg_object1
from .models import Handler


def reg_handler(options, session, ROOT):
    handler = options.get('handler', "proceed_default")
    handler_path = options.get('handler_path')

    dbconfig = options.get('db', {})

    unique_keys = options.get('__all__', [])
    unique_options = dict((key, options[key]) for key in unique_keys if key in options)

    handler_dict = dict(name=handler, path=handler_path, db=dbconfig, extras=unique_options)
    HANDLER = reg_object1(session, Handler, handler_dict, ROOT)

    return HANDLER
