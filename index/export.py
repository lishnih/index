#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, importlib, logging

from .lib.settings import Settings
from .lib.data_funcs import get_list
from .lib.db import initDb, initlinks, foreign_keys, foreign_keys_c
from .reg import set_object
from .reg.result import reg_error, reg_exception


def Proceed(sources, tree_widget=None, status=None):
    if isinstance(sources, tuple):
        as_source, files = sources
    else:
        as_source = files = sources

    brief = dict(
                Source_type = as_source,
                Files = files,
            )

    options = {}
    ROOT = set_object("Root", tree_widget, brief=brief)
    if hasattr(ROOT, 'tree_item'):
        ROOT.tree_item.setSelected(True)

    # Сбрасываем данные статуса и устанавливаем сообщение
    if status:
        status.reset(sources)

    # Загружаем обработчик
    handler = options.get('handler', "proceed_default")

    # Загружаем необходимые модули
    try:
        current = __package__+'.'+handler
        handler_module = importlib.import_module(current)
        models_module = importlib.import_module('.models', current)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    if not hasattr(handler_module, 'proceed'):
        reg_error(ROOT, "No 'proceed' function in handler '{0}'".format(handler))
        return

    # Инициализируем БД
    dbconfig = options.get('db', {})
    try:
        session = initDb(dbconfig, base=models_module.Base)
        initlinks(models_module.Base)

        set_object("session", tree_widget, brief=session)
#       set_object("foreign_keys", tree_widget, brief=foreign_keys)
#       set_object("foreign_keys_c", tree_widget, brief=foreign_keys_c)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    # Производим обработку
    sources = get_list(sources)
    for source in sources:
        handler_module.proceed(source, options, session, ROOT, status)

    # Завершаем транзакции
    try:
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)


def main(files=None, source=None):
    if files:
        if source:
            files = (source, files)

        Proceed(files)
    else:
        logging.warning("Files not specified!")
