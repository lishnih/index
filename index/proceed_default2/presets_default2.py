#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os


# Rev. 20130916


handler_default = os.path.basename(os.path.dirname(__file__))
handler_path_default = None
# handler_path_default = os.path.expanduser("~")

unique_keys = []


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


profiles["Example 2 (list)"] = {
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

    # По умолчанию, обработчики различаются между собой переменными
    # 'handler' и 'handler_path'
    # Плюс, в одном обработчике обработка файла будет повторяться
    # при разных настройках базы данных
    # Во всех остальных случаях обработка не будет выполняться повторно.

    # Но, обработчик может иметь несколько профилей
    # Чтобы различать эти профили введена переменная '__all__'
    # которая содержит перечень ключей
    '__all__': unique_keys,

    # handler options:

    # ...

}


profiles["Example 2 (tree)"] = {
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

    # Список уникальных ключей
    '__all__': unique_keys,

    # handler options:

    # ...

}
