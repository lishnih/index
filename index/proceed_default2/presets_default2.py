#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os


__rev__ = 20130918


handler = os.path.basename(os.path.dirname(__file__))
handler_path = None

unique_keys = []


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

    # Список уникальных ключей
    '__all__': unique_keys,

    # handler options:

    # ...

}
