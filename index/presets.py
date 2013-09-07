#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

# Rev. 20130907


db_default = dict(
    dbtype = "sqlite",
    dbname = os.path.expanduser("~/pgu235.sqlite"),

#     dbtype   = "mysql",
#     dbname   = "pgu235",
#     host     = "localhost",
#     user     = "root",
#     passwd   = "54321"
)


profiles = dict()


################################
### Сварка                   ###
################################

profiles["Журналы Сварки"] = {
    'ver': 1,

#   'dirs_filter':  None,
    'files_filter': "/^.+\.xlsx?$/",

    'db': {
        'dbtype': "mysql",
        'dbname': "pgu235_welding",
        'host':   "localhost",
        'user':   "root",
        'passwd': "54321"
    },

    'handlers': {

        'index_xls': {
            'sheets_filter':    "Сварка",
#           'sheet_test':       [0, 0, ''],

            'table':    {
                'row_start':        3,
                'check_column':     'C',
                'row_objects':      'Joint_entry',
                'row_objects1':     'Joint',
                'col_names': [
                    '',
                    'date',
                    '',
                    'joint',
                    '',
                    '',
                    '',
                    '',
                    'welder',
                    '',
                    '',
                    'decision',
                    '',
                    '',
                    '',
                    'piece',
                    'd',
                    'th',
                    'steel',
                ],
                'col_funcs': {
                    'date':             'proceed_date',
                    'joint':            'proceed_joint',
                    'd':                'proceed_float',
                    'th':               'proceed_float',
                },
            },
        },

    },
}


################################
### Неразрушающий контроль   ###
################################

profiles["Журналы НК"] = {
    'ver': 1,

#   'dirs_filter':  None,
    'files_filter': "/^.+\.xlsx?$/",

    'db': db_default,

    'handlers': {

        'index_xls': {
            'sheets_filter':    '/^Журнал НК$/',
#           'sheet_test':       [0, 0, ''],

            'table':    {
                'row_start':        4,
                'check_column':     'I',
                'row_objects':      'Joint_entry',
                'row_objects1':     ('Doc', 'Joint'),
                'col_names': [
                    'y',
                    'joint',
                    'welders',
                    'method',
                    'd_w_th',
                    'conditon',
                    'tools',
                    'defects',
                    'report_w_date',
                    'decision',
                ],
                'col_funcs': {
                    'y':                'proceed_int',
                    'joint':            'proceed_joint',
                    'd_w_th':           'proceed_d_w_th',
                    'report_w_date':    ('prepare_str', 'proceed_doc_w_date'),
                }
            },
        },

    },
}


profiles["Заключения НК"] = {
    'ver': 1,

#   'dirs_filter':  None,
    'files_filter': "/^.+\.xlsx?$/",

    'db': {
        'dbtype': "mysql",
        'dbname': "pgu235_welding",
        'host':   "localhost",
        'user':   "root",
        'passwd': "54321"
    },

    'handlers': {

        'index_xls': {
#           'sheets_filter':    None,
            'sheet_test':       [0, 0, "{def: pgu235/(.+); rev: \w+}"],

            'СП_Астрахань_<Отдел>_<Документ>_001': {
                'deprecated': True,
            },

            'СП_Астрахань_ОКК_Акт-ВИК-МК_001': {
                'doc':    {
                    'doc_values': {
                        'doc_pre':          ( 9,  9),
                        'doc_seq':          ( 9, 11),
                        'date':             (12,  0),
                        'steel':            (26,  8),
                    },
                    'doc_funcs': {
                        'date':             'proceed_date',
                    },
                    'doc_objects':      'Doc',
#                   'doc_objects1':     'Doc',
                },
                'table':    {
                    'row_start':        '^размеров швов сварных соединений$',
                    'row_stop':         'наименование узла',
                    'row_objects':      'Joint_entry',
                    'col_mode':         'value',
                    'col_names': [
                        'joints',
                    ],
                    'col_funcs': {
                        'joints':           'iter_joints',
                    }
                },
            },

            'СП_Астрахань_ОКК_Заключение-УЗК-МК_001': {
                'deprecated': True,
            },

            'СП_Астрахань_ОКК_УЗК-арматура_001': {
                'deprecated': True,
            },
        },

    },
}


##############################
### Разрушающий контроль   ###
##############################

profiles["Протоколы РК"] = {
    'ver': 1,

#   'dirs_filter':  None,
    'files_filter': "/^Стил.+\.xlsx?$/",

    'db': {
        'dbtype': "mysql",
        'dbname': "pgu235_welding",
        'host':   "localhost",
        'user':   "root",
        'passwd': "54321"
    },

    'handlers': {

        'index_xls': {
#           'sheets_filter':    '',
#           'sheet_test':       [0, 0, ''],

            'doc':    {
                'doc_values': {
                    'doc_pre':          ( 8,  8),
#                   'doc_seq':          ( 8, 11),
                    'date':             (10,  0),
                },
                'doc_funcs': {
                    'date':             'proceed_date',
                },
                'doc_objects1':     'Doc',
            },

            'table':    {
                'row_start':        20,
                'check_column':     'C',
                'row_objects':      'Joint_entry',
                'row_objects1':     'Joint',
                'col_names': [
                    'scheme',
                    '',
                    'joint',
                ],
                'col_funcs': {
                    'joint':            'proceed_joint',
                }
            },
        },

    },
}
