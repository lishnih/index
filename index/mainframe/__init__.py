#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, re
from PySide import QtCore, QtGui, __version__ as pyside_version
from sqlalchemy import __version__ as sqlalchemy_version

from ..lib.backwardcompat import *
from ..lib.info import __pkgname__, __description__, __version__
from ..lib.settings import Settings
from ..lib.dump_html import html_val, html

from .mainframe_ui import Ui_MainWindow

from .thread1 import th                     # Поток (уже созданный)
from .status1 import status                 # Статус (уже созданный)
# from .view_db import view_db
from .view_conf import view_conf
from ..export import Proceed                # Модуль обработки


# Настройки: [HKCU\Software\lishnih@gmail.com\<app_section>]
company_section = "lishnih@gmail.com"
app_section = re.sub(r'\W', '_', os.path.dirname(os.path.dirname(__file__)))


class MainFrame(QtGui.QMainWindow):
    def __init__(self, files=None, source=None):
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

        # Назначаем потоку callback-функции
        th.set_callback(self.update_func, self.ending_func)

        # Drag and drop
#       self.ui.tabs.setAcceptDrops(True)
        self.ui.tabs.dragEnterEvent = self.dragEnterEvent
        self.ui.tabs.dropEvent = self.dropEvent
#       self.connect(self.ui.tabs, QtCore.SIGNAL("dropped1"), self.filesDropped)

        # Список вкладок
        self.tab_list = ('brief', 'tracing', 'sources', 'handlers', 'specifications', 'databases', 'models')
        self.tab_dict = dict(
            sources        = self.ui.table3,
#             handlers       = self.ui.table4,
#             specifications = self.ui.table5,
#             databases      = self.ui.table6,
#             models         = self.ui.table7,
        )

        # Загружаем данные во вкладки
        self.loadTabsData()

        # Инициализируем меню Save
        self.initSaveMenu()

        # Connect
        s = self.tab_dict['sources']
        header = s.verticalHeader()
        header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.OnTableItemRightClick)

        self.initSourcesCMenu()

        # Обрабатываем параметры
        self.proceed_args(files, source)


# Callback-функции для Таймера

    def convert_time(self, msecs):
        secs = int(msecs / 1000)
        hours = int(secs / 3600)
        secs = secs - hours * 3600
        mins = int(secs / 60)
        secs = secs - mins * 60
        time_str = "{0:02}:{1:02}:{2:02}".format(hours, mins, secs)
        return time_str


    def update_func(self, msecs):
        time_str = self.convert_time(msecs)

        status_text = "Processing '{0}' ...   |   {1}   |   Dirs: {2}, Files: {3} ({4})".format(status.message, time_str, status.dir, status.file, status.last_dir)

        self.ui.statusbar.showMessage(status_text)


    def ending_func(self, msecs, message=None):
        time_str = self.convert_time(msecs)

        if status.break_required:
            st = "Breaked"
        else:
            st = "Processed"

        status_text = "{0}   |   {1}   |   Dirs: {2}, Files: {3}".format(st, time_str, status.dir, status.file)

        if status.error:
            status_text += "   |   " + status.error

        if message:
            status_text += "   |   " + message

        self.ui.statusbar.showMessage(status_text)


# Save menu

    def initSaveMenu(self):
        self.ui.actionSources.setData('sources')
#         self.ui.actionHandlers.setData('handlers')
#         self.ui.actionSpecifications.setData('specifications')
#         self.ui.actionDatabases.setData('databases')
#         self.ui.actionModels.setData('models')


# Context menu (tables)

    def initSourcesCMenu(self):
        self.SourcesCMenu = QtGui.QMenu()
        self.SourcesCMenu.addAction("Proceed", self.OnSourcesProceed)
        self.SourcesCMenu.addAction("Delete", self.OnSourcesDelete)


# Tabs data

    def loadTabsData(self):
#         handler_names       = self.loadTableData('handlers',       self.tab_dict['handlers'])
#         specification_names = self.loadTableData('specifications', self.tab_dict['specifications'])
#         database_names      = self.loadTableData('databases',      self.tab_dict['databases'])
#         model_names         = self.loadTableData('models',         self.tab_dict['models'])
        handler_names = specification_names = database_names = model_names = []

        self.sources_names = self.loadTableData('sources', self.tab_dict['sources'])
        self.setAllComboDatas(self.tab_dict['sources'], handler_names, specification_names, database_names, model_names)


    def setAllComboDatas(self, table, handler_names, specification_names, database_names, model_names):
        for i in range(table.rowCount()):
            self.setComboData(table, i, 1, handler_names)
            self.setComboData(table, i, 2, specification_names)
            self.setComboData(table, i, 3, database_names)
            self.setComboData(table, i, 4, model_names)

        table.resizeColumnsToContents()


    def setComboData(self, table, i, j, names):
        l = names[:]
        notlisted = False
#       item = table.cellWidget(i, j)   # is QPlainTextEdit
        item = table.item(i, j)         # is QTableWidgetItem
        if item:
#           t = item.toPlainText()
            text = item.text()
            if text not in l:
                l.insert(0, text)
                notlisted = True
        else:
            l.insert(0, "None")
            notlisted = True

        box = QtGui.QComboBox()
        box.setEditable(True)
        box.addItems(l)

#         if notlisted:
#             pixmap = QtGui.QPixmap(12, 12)
#             pixmap.fill(QtGui.QColor('red'))  # QtGui.QColor.colorNames()
#             icon = QtGui.QIcon(pixmap)
#             box.setItemIcon(0, icon)

        table.setCellWidget(i, j, box)


    def loadTableData(self, branch, table):
        row_list = self.s.get(branch, [])
#         print(row_list)
        names = []
        row = 0
        for i in row_list:
            names.append(i[0])
            self.insertRowTableData(table, row, i)
            row += 1
        table.resizeColumnsToContents()
#       table.resizeRowsToContents()
        return names


    def insertRowTableData(self, table, row, t):
        column = 0
        table.insertRow(row)
        for j in t:
            text = QtGui.QTableWidgetItem(unicode(j)) # QLineEdit, QPlainTextEdit
            table.setItem(row, column, text)          # setCellWidget
            column += 1
            if column >= table.columnCount():
                break


# Drag and Drop

    # Событие, возникающее при захватывании объекта
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()


    # Событие, возникающее при передвижении объекта
#   dragMoveEvent = dragEnterEvent

#   def dragMoveEvent(self, event):
#       if event.mimeData().hasUrls:
#           event.setDropAction(QtCore.Qt.CopyAction)
#           event.accept()
#       else:
#           event.ignore()


    # Событие, возникающее при отпускании объекта
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            files = []
            for url in event.mimeData().urls():
                files.append(url.toLocalFile())

#           self.emit(QtCore.SIGNAL("dropped1"), files)
            self.filesDropped(files)
        else:
            event.ignore()


    def filesDropped(self, files):
        if self.tab_list[self.ui.tabs.currentIndex()] == 'sources':
            for i in files:
                if i not in self.sources_names:
                    self.insertRowTableData(self.tab_dict['sources'], 0, (i,))
                    self.sources_names.append(i)


# Context menu events


    def OnSourcesProceed(self):
        if th.isRunning():
            print("running...")
            return

        sources = self.tab_dict['sources']
        t = self.get_row_data(sources, self.current_row)
        source = t[0]

        # Запускаем обработку
        self.ui.tree.clear()
        th.start(Proceed, source, tree_widget=self.ui.tree, status=status)


    def OnSourcesDelete(self):
        print(self.current_row)


# Events

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

            # Запускаем обработку
            self.ui.tree.clear()
            th.start(Proceed, selected_dir, tree_widget=self.ui.tree, status=status)


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

            # Запускаем обработку
            self.ui.tree.clear()
            th.start(Proceed, selected_file, tree_widget=self.ui.tree)


    def OnClose(self):
        if th.isRunning():
            print("running...")
            return

        self.ui.tree.clear()


    def OnSaveMenu(self, action):
        branch = action.data()      # settings branch name
        if branch:
            self.save_table_data(branch)
        else:
            for i in self.tab_dict.keys():
                self.save_table_data(i)


    def OnOpenFolder(self):
        path = self.s.expand_prefix('~~~')
        os.startfile(path)


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
#           view_db(self.ui.db_tree, session)
        if current == 2:
            self.ui.conf_tree.clear()
            view_conf(self.ui.conf_tree, self.s)


    def OnTabChanged(self, current):
        pass


    def OnTableItemRightClick(self, pos):
        sources = self.tab_dict['sources']
        header = sources.verticalHeader()
        self.current_row = header.logicalIndexAt(pos)
#       self.SourcesCMenu.exec_(QtGui.QCursor.pos())
        self.SourcesCMenu.popup(QtGui.QCursor.pos())


#     def mousePressEvent(self, event):
#         if event.button() == QtCore.Qt.MouseButton.LeftButton:
#             self.mousePressEvent_Left(event)
#         elif event.button() == QtCore.Qt.MouseButton.RightButton:
#             self.mousePressEvent_Right(event)
#
#
#     def mousePressEvent_Left(self, event):
#         child = self.childAt(event.pos())
#         print(2, child)
#         if not child:
#             return
#
#
#     def mousePressEvent_Right(self, event):
#         child = self.childAt(event.pos())
#         print(3, child)
#         if not child:
#             return


    def OnAbout(self):
        msg  = "{0}\n".format(__description__)
        msg += "Version: {0}\n\n".format(__version__)

        msg += "Author: Stan <lishnih@gmail.com>\n"
        msg += "License: MIT\n\n"

        msg += "Python: {0}\n".format(sys.version)
        msg += "SQLAlchemy: {0}\n".format(sqlalchemy_version)
        msg += "PySide: {0}\n".format(pyside_version)
        msg += "Qt: {0}\n".format(QtCore.__version__)
        QtGui.QMessageBox.about(None, "About", msg)


    def OnAbout_Qt(self):
        QtGui.QApplication.aboutQt()


    def closeEvent(self, event):
        if th.isRunning():
#           th.terminate()
            status.break_required = True
            event.ignore()
            return

        # Сохраняем состояние окна
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

        event.accept()


# Сервисные функции


    def save_table_data(self, branch):      # settings branch name
        self.s.set(branch, [])
        table = self.tab_dict[branch]       # is QTableWidget
        for i in range(table.rowCount()):
            t = self.get_row_data(table, i)
            self.s.append(branch, t)


    def get_row_data(self, table, row):
        l = []
        for i in range(table.columnCount()):
            box = table.cellWidget(row, i)  # is QComboBox
            if box:
                text = box.currentText()
                if text == 'None':
                    text = None
                l.append(text)
            else:
                item = table.item(row, i)   # is QTableWidgetItem
                if item:
                    text = item.text()
                    if text == 'None':
                        text = None
                    l.append(text)
                else:
                    l.append(None)
        return tuple(l)


    def proceed_args(self, files=None, source=None):
        # Следует отметить, что из командной строки передаётся массив файлов
        if files:
            if source:
                # Если задан source, то обрабатываем файлы с настройками для source
                files = (source, files)

            # Запускаем обработку
            th.start(Proceed, files, tree_widget=self.ui.tree, status=status)
