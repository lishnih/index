#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import logging

from PySide import QtCore, QtGui

from .mainframe import MainFrame            # Основное окно


# translator = QtCore.QTranslator()
# translator.load("ru")
# app.installTranslator(translator)


app = QtGui.QApplication(sys.argv)          # Приложение


def main(files=None, profile=None, options=None):
    frame = MainFrame(files, profile, options)  # Инициализируем
    frame.show()                                # Отображаем

    res = app.exec_()                       # Цикл
    return res
