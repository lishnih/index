#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ...lib.source_funcs import get_sha256_module
from ...reg import reg_object1


def reg_handler(runtime, ROOT):
    handler = runtime.get('h_module')
    model = runtime.get('m_module')
    options = runtime.get('options', {})
    session = runtime.get('session')

    # Вычисляем данные модулей (model, handler)
    h_sha256 = get_sha256_module(handler)
    h_name = handler.__name__

    m_sha256 = get_sha256_module(model)
    m_name = model.__name__

    handler_dict = dict(
                        name=h_name,
#                       rev=rev,
                        hash="{0}_{1}".format(h_sha256, m_sha256),
                        extras=options,
                       )

    HANDLER = reg_object1(session, model.Handler, handler_dict, ROOT, brief=handler_dict)

    return HANDLER
