#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from presets import PROJECT, projectpath, db_default


statinfo = os.stat(__file__)
__rev__ = int(statinfo.st_mtime) if statinfo else None


handler = os.path.basename(os.path.dirname(__file__))

xls_types_default = "/^[^~._].*\.xlsx?$/"


profiles = dict()


################################
### Неразрушающий контроль   ###
################################

profiles["Таблица ({0})".format(PROJECT)] = {
    'sources': [
        os.path.join(projectpath, "UCS1-数据库.xls")
    ],

    # Обработчик
    'handler': handler,
    'rev':     __rev__,

    # Фильтры для директорий и файлов
#   'dirs_filter':  None,
    'files_filter': xls_types_default,

    # Отображение файлов в виде списка или дерева
#   'treeview': 'tree',       # 'list' (default) or 'tree'

    # БД
    'db': db_default,

    # handler options:

    'sheets_filter': "/^[^_].*/",
#   'sheet_test':    (0, 0, "{def: (.+); rev: \w+}"),

    'default_group': 'without_groups',

    'without_groups': {
        'doc': {
            'doc_objects1': 'Doc',

            'doc_plains': [
                ('kind', 'Заключение'),
                ('type', 'RT'),
            ],

            'table': {
                'row_objects1': 'Joint',
                'row_objects':  'Joint_entry',

                'object_required': {
                    'Joint': [
                        'joint',
                    ],
                },

                'object_keys': {
                    'Joint': [
                        ('name', 'joint'),
                    ],
                },

                'check_column':   'H',
                'row_start':      0,
                'row_start_skip': 1,
                'row_stop':       10000,
                'row_stop_skip':  0,
#               'col_mode':       'column',

                'col_names': [
                    '',
                    'date',
                    '',
                    'report',
                    '',
                    'line',
                    'line2',
                    'seq',
                    'steel',
                    'dt',
                    'welders',
                    '', '', '',
                    '', '', '',
                    'decision',
                ],

#                 'col_funcs': [
#                     ('seq', 'proceed_seq'),
#                 ],
            },
        }, # 'doc'

    }, # Group

} # Profile
