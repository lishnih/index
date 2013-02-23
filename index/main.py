#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

import sys
from PySide import QtCore, QtGui

from mainframe import MainFrame             # Основное окно
# from systray import SysTray               # Трей


# def init_translator():
#     translator = QtCore.QTranslator()
#     translator.load("ru")
#     app.installTranslator(translator)


def main(args=None):
#   init_translator()                       # i18n
#   tray = SysTray()                        # Трей

    app = QtGui.QApplication(sys.argv)      # Приложение

    frame = MainFrame(args)                 # Инициализируем
    frame.show()                            # Отображаем

    res = app.exec_()                       # Цикл
    return res


if __name__ == '__main__':
    import argparse
    from lib.argparse_funcs import readable_dir, readable_file_or_dir_list

    parser = argparse.ArgumentParser(description='Indexing files and directories.')
    parser.add_argument('files', action=readable_file_or_dir_list, nargs='*',
                        help='files and directories to proceed')
    parser.add_argument('--setdatadir', action=readable_dir, nargs='?', const='/',
                        help='set data directory', metavar='DATADIR')
    parser.add_argument('--datadir', action='store_true',
                        help='get data directory')

    args = parser.parse_args()

    sys.exit(main(args))