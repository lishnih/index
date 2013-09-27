#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, logging
from PySide import QtCore, QtGui

from .mainframe import MainFrame            # Основное окно
# from .systray import SysTray              # Трей


# translator = QtCore.QTranslator()
# translator.load("ru")
# app.installTranslator(translator)


app = QtGui.QApplication(sys.argv)          # Приложение


def main(files=None, method=None):
#   tray = SysTray()                        # Трей

    frame = MainFrame(files, method)        # Инициализируем
    frame.show()                            # Отображаем

    res = app.exec_()                       # Цикл
    return res
