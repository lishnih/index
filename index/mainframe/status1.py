#!/usr/bin/env python
# coding=utf-8
# Stan 2015-06-05

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import logging

from PySide.QtCore import QObject, Signal, Slot


# http://www.pythoncentral.io/pysidepyqt-tutorial-creating-your-own-signals-and-slots/
class Status(QObject):
#   current_dir  = Signal(str, int)
#   current_file = Signal(str, int)
    finished = Signal()

    def __init__(self):
        QObject.__init__(self)

        self.reset()

    def reset(self, text=''):
        self.ndirs = self.nfiles = 0
        self.last_dir = ''
        self.break_required = None
        self.message = text
        self.error = ''

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        if isinstance(message, (list, tuple)):
            if not len(message):
                message = ''
            elif len(message) == 1:
                message = message[0]
            else:
                message = "{0} и др. значения".format(message[0])
        self._message = message

    @property
    def dir(self):
        return self.ndirs

    @dir.setter
    def dir(self, filename):
        self.last_dir = filename
        self.ndirs += 1

    @property
    def file(self):
        return self.nfiles

    @file.setter
    def file(self, filename):
        self.nfiles += 1

    @property
    def stop(self):
        pass

    @stop.getter
    def stop(self):
        self.finished.emit()


@Slot()
def onFinished():
    logging.info('Processing finished')


status = Status()
status.finished.connect(onFinished)
