#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os


__rev__ = 20130918


handler = os.path.basename(os.path.dirname(__file__))
handler_path = None


db_default = {
    # Sqlite
    'dbtype': "sqlite",
    'dbname': os.path.expanduser("~/default.sqlite"),

    # Mysql
#     'dbtype': "mysql",
#     'dbname': "default",
#     'host':   "localhost",
#     'user':   "root",
#     'passwd': "",
}


profiles = dict()


profiles["Example list ({0})".format(handler)] = {
    # Обработчик
    'handler': handler,
    'rev':     __rev__,

    # Фильтры для директорий и файлов
#   'dirs_filter':  None,
#   'files_filter': None,

    # Отображение файлов в виде списка или дерева
#   'treeview':  'tree',      # 'list' (default) or 'tree'

    # БД
    'db': db_default,

    # handler options:

    # ...

}


profiles["Example tree ({0})".format(handler)] = {
    # Обработчик
    'handler': handler,
    'rev':     __rev__,

    # Фильтры для директорий и файлов
#   'dirs_filter':  None,
#   'files_filter': None,

    # Отображение файлов в виде списка или дерева
    'treeview':  'tree',      # 'list' (default) or 'tree'

    # БД
    'db': db_default,

    # handler options:

    # ...

}
