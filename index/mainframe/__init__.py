#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, re, fnmatch
from PySide import QtCore, QtGui, __version__

from ..lib.backwardcompat import *
from ..lib.info import __pkgname__, __description__, __version__
from ..lib.settings import Settings
from ..lib.dump_html import html_val, html
from .mainframe_ui import Ui_MainWindow
from .thread1 import th                     # Поток (уже созданный)
# from .view_db import view_db
from ..export import Proceed                # Модуль обработки


# Настройки: [HKCU\Software\lishnih@gmail.com\<app_section>]
company_section = "lishnih@gmail.com"
app_section = re.sub(r'\W', '_', os.path.dirname(os.path.dirname(__file__)))


class MainFrame(QtGui.QMainWindow):
    def __init__(self, files=None, method=None):
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

        # Переменная для Proceed
        self.proceed_status = {}

        # Назначаем потоку callback-функции
        th.set_callback(self.update_func, self.ending_func)

        # Загружаем список настроек
        self.load_profiles()

        # Инициализируем метод
        self.set_method()

        # Обрабатываем параметры
        self.proceed_args(files, method)


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
            options = self.get_profile()
            th.start(Proceed, selected_dir, options, tree_widget=self.ui.tree, status=self.proceed_status)


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
            options = self.get_profile()
            th.start(Proceed, selected_file, options, tree_widget=self.ui.tree)


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
#           th.terminate()
            self.proceed_status['break'] = True
            event.ignore()
            return

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


    def load_profiles(self):
        self.profiles = self.s.get_group('profiles')

        alignmentGroup = QtGui.QActionGroup(self)
        alignmentGroup.addAction(self.ui.actionDefault)

        for key, val in self.profiles:
            action = QtGui.QAction(key, self, checkable=True)
            self.ui.menuTask.addAction(action)
            alignmentGroup.addAction(action)

        self.ui.actionDefault.setChecked(True)


    def set_method(self, method="Default"):
        self.current_method = method
        if method:
            self.set_status("Current method: {0}".format(method))


    def proceed_args(self, files=None, method=None):
        if files:
            if method:
                if self.profiles.contains(method, dict):
                    self.ui.actionDefault.setChecked(False)
                    self.set_method(method)
                    self.set_status(files)

                    options = self.get_profile()
                else:
                    text = "Required method not exists: '{0}'!".format(method)
                    QtGui.QErrorMessage(self).showMessage(text)
#                   msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Warning", text)
#                   msgBox.exec_()
                    return

            else:
                options = {}

            th.start(Proceed, files, options, tree_widget=self.ui.tree, status=self.proceed_status)


    def get_profile(self):
        name = self.current_method

        if name == "Default":
            return {}

        profile = self.profiles.get_group(name)
        return profile.get_dict()
