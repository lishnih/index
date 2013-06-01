#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-14

import sys, os
from PySide import QtCore, QtGui
from sqlalchemy import types

import dragwidget_rc


def init_task(parent, sources=[], pos=None):
    name = os.path.basename(sources[0]) if sources else u"Новая задача"
    count = len(sources)
    if count > 1:
        name = name + "+"

    sources = set(sources)
    task = dict(name=name, pos=pos, img=":/images/file.png", sources=sources)
    return task


def draw_task(parent, task, offset=None, middle=None):
    taskIcon = QtGui.QLabel(parent)
    pos = task.get('pos')
    img = task.get('img', u":/images/file.png")

    if isinstance(pos, QtCore.QPoint):
        pos = pos.toTuple()
    if isinstance(offset, QtCore.QPoint):
        offset = offset.toTuple()

    taskIcon.taskData = task
    taskIcon.taskData['icon'] = taskIcon

    redraw(taskIcon)
    taskIcon.show()

    if pos:
        if middle:
            rect = taskIcon.rect()
            offset = (rect.width() // 2, rect.height() // 2)
        if offset:
            pos = correct_pos(pos, offset)
            task['pos'] = pos
        taskIcon.move(*pos)

    taskIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    return taskIcon


def redraw(child):
    taskData = child.taskData
    name = taskData.get('name', u"/Без имени/")
    img  = taskData.get('img',  u":/images/file.png")
    taskIcon = taskData.get('icon')

    sources = taskData.get('sources', [])
    count = len(sources)

    taskIcon.setText(u'<p align="center"><img src="{}"/><br/>{}<br/>Всего {} элем.</p>'.format(img, name, count))


def highlight(child):
    rect = child.rect()
    w, h = rect.width(), rect.height()
    pixmap = QtGui.QPixmap(w, h)
    pixmap.fill(QtGui.QColor(127, 127, 127, 63))

    taskData = child.taskData
    taskIcon = taskData.get('icon')
    taskIcon.setPixmap(pixmap)


def correct_pos(pos, offset):
    if offset:
        pos = (pos[0] - offset[0], pos[1] - offset[1])
    return pos
