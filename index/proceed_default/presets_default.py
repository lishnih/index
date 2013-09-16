#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os


# Rev. 20130913


handler_default = os.path.basename(os.path.dirname(__file__))
handler_path_default = None
# handler_path_default = os.path.expanduser("~")


db_default = dict(
    # Sqlite
    dbtype = "sqlite",
    dbname = os.path.expanduser("~/default.sqlite"),

    # Mysql
#   dbtype = "mysql",
#   dbname = "default",
#   host   = "localhost",
#   user   = "root",
#   passwd = ""
)


profiles = dict()


profiles["Example (list)"] = {
    # Обработчик
    'handler':      handler_default,
    'handler_path': handler_path_default,

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


profiles["Example (tree)"] = {
    # Обработчик
    'handler':      handler_default,
    'handler_path': handler_path_default,

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
