#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging


# Rev. 20130805


################################
### Сварка                   ###
################################

welding = {
    'description':      "Обработка журналов сварки",
#   'dirs_filter':      None,
#   'dirs_level':       0,
    'files_filter':     "/^.+\.xlsx?$/",

    'handler':  {
        'sheets_filter':    "Сварка",
#       'sheet_test':       [0, 0, ''],

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
}


################################
### Неразрушающий контроль   ###
################################

ndt_register = {
    'description':      "Обработка журналов НК",
#   'dirs_filter':      None,
#   'dirs_level':       0,
    'files_filter':     "/^.+\.xlsx?$/",

    'handler':  {
        'sheets_filter':    '/^Журнал НК$/',
#       'sheet_test':       [0, 0, ''],
    
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
}


ndt_reports = {
    'description':      "Обработка заключений НК",
#   'dirs_filter':      None,
#   'dirs_level':       0,
    'files_filter':     "/^.+\.xlsx?$/",

    'handler':  {
    #   'sheets_filter':    None,
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
    #           'doc_objects1':     'Doc',
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
}


def main():
    for key, value in globals().items():
        if isinstance(value, dict):
            logging.info(key)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
