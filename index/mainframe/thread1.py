#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging
from PySide import QtCore


# Функции обработки запускаем отдельным процессом
# (чтобы не замораживать Gui)
class Thread(QtCore.QThread):
    def __init__(self):
        super(Thread, self).__init__()

        # Вывод
        self.timer = None
        self.message = ""


    def set_callback(self, update_func, ending_func, interval=1000):
        # Таймер
        self.timer = QtCore.QTimer(self)
        self.update_func = update_func
        self.ending_func = ending_func
        self.interval = interval
        self.timer.timeout.connect(self.update)


    def update(self):
        if self.isRunning():
            self.secs += self.interval
            if self.update_func:
                self.update_func(self.secs)
        else:
            self.timer.stop()
            if self.ending_func:
                self.ending_func(self.secs, self.message)


    def start(self, func, *args, **kargs):
        if self.timer:
            self.secs = 0
            self.timer.start(self.interval)

        self.func = func
        self.args = args
        self.kargs = kargs
        super(Thread, self).start()


    def run(self):
        if self.func:
            try:
                self.message = self.func(*self.args, **self.kargs)
            except Exception as e:
                msg = "Завершено с ошибкой: '{0}'".format(e)
                logging.exception(msg)
                self.message = msg


th = Thread()
