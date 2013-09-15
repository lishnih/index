#!/usr/bin/env python
# coding=utf-8
# Stan 2011-06-30

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

from PySide import QtCore, QtGui


class Item(QtGui.QTreeWidgetItem):
    def __init__(self, parent, item_name, brief=None, summary=None):
        super(Item, self).__init__(parent)
        self.res = None
        self.parent = parent

        self.setText(0, item_name)

        self.setBrief(brief)
        self.setSummary(summary)


    def setBrief(self, brief=None):
        self.setData(0, QtCore.Qt.UserRole, brief)


    def appendBrief(self, brief, once=False):
        if brief:
            brief_list = self.data(0, QtCore.Qt.UserRole)

            if not isinstance(brief_list, list):
                brief_list = [brief_list]

            if not(once and brief in brief_list):
                brief_list.append(brief)

            self.setBrief(brief_list)


    def setSummary(self, summary=None):
        self.setData(1, QtCore.Qt.UserRole, summary)


    def setOk(self, message=None):
        self.appendBrief(message)
        self.setResult(0)


    def setWarning(self, message=None):
        self.appendBrief(message)
        self.setResult(-1)


    def setError(self, message=None):
        self.appendBrief(message)
        self.setResult(-2)


# setResult - для внутреннего использования
# Коды для res:
# None - неопределено, значение по умолчанию
#    0 - объект/дочерние объекты обработаны успешно
#   -1 - warning во время обработки
#   -2 - error   во время обработки

    def setResult(self, res=None):
        if res == None:
            return

        if self.res == None or self.res > res:
            self.res = res

            if   res ==  0:
                self.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))
            elif res == -1:
                self.setForeground(0, QtGui.QBrush(QtCore.Qt.darkYellow))
            elif res == -2:
                self.setForeground(0, QtGui.QBrush(QtCore.Qt.red))

            if isinstance(self.parent, Item):
                self.parent.setResult(res)


    def set_style(self, style=''):
        if 'B' in style:
            self.set_bold()
        if 'I' in style:
            self.set_italic()
        if 'D' in style:
            self.set_quiet()
#           self.setDisabled(True)
        if 'E' in style:
            self.setExpanded(True)


    def set_bold(self):
        font = self.font(0)
        font.setBold(True)
        self.setFont(0, font)


    def set_italic(self):
        font = self.font(0)
        font.setItalic(True)
        self.setFont(0, font)


    def set_quiet(self):
        self.setForeground(0, QtGui.QBrush(QtCore.Qt.gray))


# Элемент дерева - директория
class DirItem(Item):
    def __init__(self, *args, **kargs):
        super(DirItem, self).__init__(*args, **kargs)

        self.set_bold()


# Элемент дерева - файл
class FileItem(Item):
    pass


# Элемент дерева - отключенный элемент
class DisabledItem(Item):
    def __init__(self, *args, **kargs):
        super(DisabledItem, self).__init__(*args, **kargs)

        self.set_italic()
