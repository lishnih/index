#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, re, fnmatch
from PySide import QtCore, QtGui, __version__

from .mainframe_ui import Ui_MainWindow
from .thread1 import th                 # Поток (уже созданный)
from .view_db import view_db

from export import ProceedInit          # Модуль обработки

from lib.info import __description__, __version__
from lib.backwardcompat import *
from lib.settings import Settings
from lib.dump_html import html_val, html


# Настройки: [HKCU\Software\lishnih@gmail.com\<app_section>]
company_section = "lishnih@gmail.com"
app_section = re.sub(r'\W', '_', os.path.dirname(os.path.dirname(__file__)))


class MainFrame(QtGui.QMainWindow):
    def __init__(self, args=None):
        super(MainFrame, self).__init__()

        # Загружаем элементы окна
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Восстанавливаем состояние окна
        self.settings = QtCore.QSettings(company_section, app_section)
        self.restoreGeometry(self.settings.value("geometry"))
        self.restoreState(self.settings.value("windowState"))

        # Настройки
        self.s = Settings()
        self.s.saveEnv()

        # Переменная для ProceedInit
        self.proceed_status = {}

        # Назначаем потоку callback-функции
        th.set_callback(self.update_func, self.ending_func)

        # Инициализируем datadir
        self.s.init_path('datadir', '~~~')

        # Обрабатываем параметры
        self.proceed_args(args)

        # Обновляем задачи
        self.proceed_methods()
        self.set_method()   # Auto is default
        self.default_method = 'C:\\Users\\SP0025\\.config\\index\\welding.pickle'


# Callback-функции для Таймера

    def convert_time(self, msecs):
        secs = int(msecs / 1000)
        hours = int(secs / 3600)
        secs = secs - hours * 3600
        mins = int(secs / 60)
        secs = secs - mins * 60
        time_str = "{:02}:{:02}:{:02}".format(hours, mins, secs)
        return time_str


    def update_func(self, msecs):
        time_str = self.convert_time(msecs)
        status_text = "{0}   |   Processing {1}".format(self.sb_message, time_str)

        if self.proceed_status:
            status_text += "   |   " + ", ".join(["{0}: {1}".format(i, self.proceed_status[i]) for i in self.proceed_status.keys()])

        self.ui.statusbar.showMessage(status_text)


    def ending_func(self, msecs, message=None):
        time_str = self.convert_time(msecs)
        status_text = "{0}   |   Processed in {1}".format(self.sb_message, time_str)

        if self.proceed_status:
            status_text += "   |   " + ", ".join(["{0}: {1}".format(i, self.proceed_status[i]) for i in self.proceed_status.keys()])

        if message:
            status_text += "   |   " + message

        self.ui.statusbar.showMessage(status_text)


# События

    def OnTaskDir(self):
        if th.isRunning():
            print("running...")
            return

        # Предлагаем выбрать пользователю директорию
        dialog = QtGui.QFileDialog(None, "Select Dir")
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            # Выбираем директорию
            fileNames = dialog.selectedFiles()
            selected_dir = fileNames[0]

            self.ui.tree.clear()

            # Отображаем путь в Статусбаре
            self.set_status(selected_dir)

            # Запускаем обработку
            th.start(ProceedInit, selected_dir, filename=self.default_method, tree_widget=self.ui.tree, status=self.proceed_status)


    def OnTaskFile(self):
        if th.isRunning():
            print("running...")
            return

        # Предлагаем выбрать пользователю файл
        dialog = QtGui.QFileDialog(None, "Select File")
        if dialog.exec_():
            # Выбираем файл
            fileNames = dialog.selectedFiles()
            selected_file = fileNames[0]

            self.ui.tree.clear()

            # Отображаем путь в Статусбаре
            self.set_status(selected_file)

            # Запускаем обработку
            th.start(ProceedInit, selected_file, filename=self.default_method, tree_widget=self.ui.tree)


    def OnClose(self):
        if th.isRunning():
            print("running...")
            return

        self.ui.tree.clear()


    def OnTaskMenu(self, action):
        self.set_method(action.text())


    def OnTreeItemSelected(self, item, prev=None):
        if not item:
            self.ui.text1.setHtml('')
            self.ui.text2.setHtml('')
            return

        tmpl = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head></head>
<body>
  <h3>{0}</h3>
  {1}
</body>
</html>"""
        it = 1

        text1 = item.data(0, QtCore.Qt.UserRole)
        if text1 is not None:
            obj_dump = html(text1, it)
            text1 = tmpl.format("", obj_dump)
        self.ui.text1.setHtml(text1)

        if th.isRunning():
            return

        text2 = item.data(1, QtCore.Qt.UserRole)
        if text2 is not None:
            obj_name = html_val(text2)
            obj_dump = html(text2, it)
            text2 = tmpl.format(obj_name, obj_dump)
        self.ui.text2.setHtml(text2)


    def OnToolBoxChanged(self, current):
        if current == 1:
            self.ui.db_tree.clear()
            view_db(self.ui.db_tree)


    def OnAbout(self):
        msg  = "{0}\n".format(__description__)
        msg += "Version: {0}\n\n".format(__version__)

        msg += "Author: Stan <lishnih@gmail.com>\n"
        msg += "License: MIT\n\n"

        msg += "Python: {0}\n".format(sys.version)
        msg += "PySide: {0}\n".format(__version__)
        msg += "Qt: {0}\n".format(QtCore.__version__)
        QtGui.QMessageBox.about(None, "About", msg)


    def OnAbout_Qt(self):
        QtGui.QApplication.aboutQt()


    def closeEvent(self, event):
        if th.isRunning():
            th.terminate()
            event.ignore()

        # Сохраняем состояние окна
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        event.accept()


# Сервисные функции


    def set_status(self, message=''):
        if isinstance(message, (list, tuple)):
            message = "{0} и др. значения".format(message[0])
        self.sb_message = message
        self.ui.statusbar.showMessage(self.sb_message)


    def proceed_args(self, args):
        if args.files:
            # Отображаем путь в Статусбаре
            self.set_status(args.files)

            # Запускаем обработку
            args = dict(args._get_kwargs())

            datadir  = self.s.get("datadir", '.')
            method   = args.get("method", "Default")
            filename = os.path.join(datadir, "{0}.pickle".format(method))

            th.start(ProceedInit, args['files'], filename=filename, tree_widget=self.ui.tree)


    def set_method(self, method=""):
        self.default_method = method
        if method:
            self.set_status("Current method: {0}".format(method))


    def proceed_methods(self):
        datadir = self.s.get("datadir")

        matches = []
        for root, dirnames, filenames in os.walk(datadir):
            for filename in fnmatch.filter(filenames, '*.pickle'):
                matches.append(os.path.join(root, filename))

        alignmentGroup = QtGui.QActionGroup(self)
        alignmentGroup.addAction(self.ui.actionAuto)
        alignmentGroup.addAction(self.ui.actionDefault)

        for i in matches:
            action = QtGui.QAction(i, self, checkable=True)
            self.ui.menuTask.addAction(action)
            alignmentGroup.addAction(action)

        self.ui.actionAuto.setChecked(True)
