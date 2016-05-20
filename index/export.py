#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, importlib, logging
from PySide import QtCore
import yaml

from .lib.backwardcompat import *
from .lib.settings import Settings
from .lib.data_funcs import get_list
from .lib.source_funcs import get_source_data
from .lib.db import initDb, initlinks, foreign_keys, foreign_keys_c
from .reg import set_object
from .reg.result import reg_error, reg_exception


def Proceed(sources, tree_widget=None, status=None):
    if isinstance(sources, tuple):
        as_source, files = sources
    else:
        as_source = None
        files = sources

    brief = {
                "Input files": files,
                "As source": as_source,
                "===": "===================="
            }
    ROOT = set_object("Root", tree_widget, brief=brief)

    # Сбрасываем данные статуса и устанавливаем сообщение
    if status:
        status.reset(sources)

    if isinstance(files, collections_types):
        for i in files:
            Proceed1(i, as_source if as_source else i, ROOT, status)
    else:
        Proceed1(files, as_source if as_source else files, ROOT, status)

    if hasattr(ROOT, 'tree_item'):
        ROOT.tree_item.setSelected(True)
#       tree_widget.emit(QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"), ROOT.tree_item)
#       tree_widget.window().OnTreeItemSelected(ROOT.tree_item)


def Proceed1(file1, as_source, ROOT=None, status=None):
    file1 = os.path.abspath(file1)
    as_source = os.path.abspath(as_source)
    as_source = as_source.replace('\\', '/')
    brief = {
                "File": file1,
                "Source": as_source,
                "===": "===================="
            }
    if hasattr(ROOT, 'tree_item'):
        ROOT.tree_item.appendBrief(brief)

    s = Settings()
    source_data = get_source_data(as_source, s)
    if not source_data:
        reg_error(ROOT, "No such source '{0}'!".format(as_source))
        status.error = "No such source '{0}'!".format(as_source)
        return

    source, handler, specification, database, model = source_data[:5]
    if hasattr(ROOT, 'tree_item'):
        ROOT.tree_item.appendBrief(dict(
            source_data = (source, handler, specification, database, model)
        ))

    # Загружаем модули (model, handler)
    try:
        current = __package__ + '.models.' + model
        model_module = importlib.import_module(current)
        current = __package__ + '.handlers.' + handler
        handler_module = importlib.import_module(current)
    except Exception as e:
        reg_exception(ROOT, e)
        status.error = "Error in module '{0}'!".format(current)
        return

    # Обработчик имеет точку входа 'proceed'
    if not hasattr(handler_module, 'proceed'):
        reg_error(ROOT, "No 'proceed' function in handler '{0}'!".format(handler))
        status.error = "No 'proceed' function in handler '{0}'!".format(handler)
        return

    # Загружаем модули (specification, database)
    home = os.path.dirname(__file__)
    try:
        current = os.path.join(home, 'specifications', '{0}.yaml'.format(specification))
        with open(current, 'r') as f:
            spec_data = yaml.load(f)
        current = os.path.join(home, 'databases', '{0}.yaml'.format(database))
        with open(current, 'r') as f:
            dbconfig = yaml.load(f)
    except Exception as e:
        reg_exception(ROOT, e)
        status.error = "Error in yaml file '{0}'!".format(current)
        return

    if not spec_data:
        spec_data = dict()

    # Инициализируем БД
    try:
        session = initDb(dbconfig, base=model_module.Base)
        initlinks(model_module.Base)
    except Exception as e:
        reg_exception(ROOT, e)
        status.error = "Error during db init!"
        return

    runtime = dict(
        handler = handler,
        h_module = handler_module,

        model = model,
        m_module = model_module,

        specification = specification,
        options = spec_data,

        database = database,
        session = session
    )

    if hasattr(ROOT, 'tree_item'):
        set_object("runtime", ROOT, brief=dict(
            handler       = (handler, handler_module),
            model         = (model, model_module),
            specification = (specification, spec_data),
            database      = (database, session, foreign_keys, foreign_keys_c),
        ))

    # Производим обработку
    try:
        handler_module.proceed(file1, runtime, ROOT, status)
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)
        status.error = "Error during proceed!"
        session.rollback()


def main(files=None, source=None):
    if files:
        if source:
            files = (source, files)

        Proceed(files)
    else:
        logging.warning("Files not specified!")
