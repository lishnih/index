# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainframe.ui'
#
# Created: Fri Apr 22 14:27:44 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.toolBox = QtGui.QToolBox(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBox.setObjectName("toolBox")
        self.page1 = QtGui.QWidget()
        self.page1.setGeometry(QtCore.QRect(0, 0, 256, 393))
        self.page1.setObjectName("page1")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.page1)
        self.verticalLayout_8.setSpacing(3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tree = QtGui.QTreeWidget(self.page1)
        self.tree.setObjectName("tree")
        self.verticalLayout_8.addWidget(self.tree)
        self.toolBox.addItem(self.page1, "")
        self.page2 = QtGui.QWidget()
        self.page2.setGeometry(QtCore.QRect(0, 0, 256, 393))
        self.page2.setObjectName("page2")
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.page2)
        self.verticalLayout_10.setSpacing(3)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.conf_tree = QtGui.QTreeWidget(self.page2)
        self.conf_tree.setObjectName("conf_tree")
        self.verticalLayout_10.addWidget(self.conf_tree)
        self.toolBox.addItem(self.page2, "")
        self.tabs = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setAcceptDrops(True)
        self.tabs.setObjectName("tabs")
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        self.verticalLayout = QtGui.QVBoxLayout(self.tab1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text1 = QtGui.QTextEdit(self.tab1)
        self.text1.setObjectName("text1")
        self.verticalLayout.addWidget(self.text1)
        self.tabs.addTab(self.tab1, "")
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName("tab2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text2 = QtGui.QTextEdit(self.tab2)
        self.text2.setObjectName("text2")
        self.verticalLayout_2.addWidget(self.text2)
        self.tabs.addTab(self.tab2, "")
        self.tab3 = QtGui.QWidget()
        self.tab3.setObjectName("tab3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.table3 = QtGui.QTableWidget(self.tab3)
        self.table3.setObjectName("table3")
        self.table3.setColumnCount(3)
        self.table3.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table3.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table3.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table3.setHorizontalHeaderItem(2, item)
        self.verticalLayout_3.addWidget(self.table3)
        self.tabs.addTab(self.tab3, "")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionTaskDir = QtGui.QAction(MainWindow)
        self.actionTaskDir.setObjectName("actionTaskDir")
        self.actionTaskFile = QtGui.QAction(MainWindow)
        self.actionTaskFile.setObjectName("actionTaskFile")
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionSources = QtGui.QAction(MainWindow)
        self.actionSources.setObjectName("actionSources")
        self.actionHandlers = QtGui.QAction(MainWindow)
        self.actionHandlers.setObjectName("actionHandlers")
        self.actionSpecifications = QtGui.QAction(MainWindow)
        self.actionSpecifications.setObjectName("actionSpecifications")
        self.actionDatabases = QtGui.QAction(MainWindow)
        self.actionDatabases.setObjectName("actionDatabases")
        self.actionModels = QtGui.QAction(MainWindow)
        self.actionModels.setObjectName("actionModels")
        self.actionAll = QtGui.QAction(MainWindow)
        self.actionAll.setObjectName("actionAll")
        self.actionOpen_folder = QtGui.QAction(MainWindow)
        self.actionOpen_folder.setObjectName("actionOpen_folder")
        self.menuFile.addAction(self.actionTaskDir)
        self.menuFile.addAction(self.actionTaskFile)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuSettings.addAction(self.actionOpen_folder)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.tabs.setCurrentIndex(2)
        QtCore.QObject.connect(self.actionTaskDir, QtCore.SIGNAL("triggered()"), MainWindow.OnTaskDir)
        QtCore.QObject.connect(self.actionTaskFile, QtCore.SIGNAL("triggered()"), MainWindow.OnTaskFile)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL("triggered()"), MainWindow.OnClose)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), MainWindow.OnAbout)
        QtCore.QObject.connect(self.actionAbout_Qt, QtCore.SIGNAL("triggered()"), MainWindow.OnAbout_Qt)
        QtCore.QObject.connect(self.toolBox, QtCore.SIGNAL("currentChanged(int)"), MainWindow.OnToolBoxChanged)
        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), MainWindow.OnTreeItemSelected)
        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"), MainWindow.OnTreeItemSelected)
        QtCore.QObject.connect(self.conf_tree, QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"), MainWindow.OnTreeItemSelected)
        QtCore.QObject.connect(self.tabs, QtCore.SIGNAL("currentChanged(int)"), MainWindow.OnTabChanged)
        QtCore.QObject.connect(self.actionOpen_folder, QtCore.SIGNAL("triggered()"), MainWindow.OnOpenFolder)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page1), QtGui.QApplication.translate("MainWindow", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.conf_tree.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page2), QtGui.QApplication.translate("MainWindow", "Conf", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab1), QtGui.QApplication.translate("MainWindow", "Brief", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab2), QtGui.QApplication.translate("MainWindow", "Tracing", None, QtGui.QApplication.UnicodeUTF8))
        self.table3.setSortingEnabled(True)
        self.table3.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.table3.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Handler", None, QtGui.QApplication.UnicodeUTF8))
        self.table3.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab3), QtGui.QApplication.translate("MainWindow", "Profiles", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTaskDir.setText(QtGui.QApplication.translate("MainWindow", "Task Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTaskDir.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTaskFile.setText(QtGui.QApplication.translate("MainWindow", "Task File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTaskFile.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Alt+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSources.setText(QtGui.QApplication.translate("MainWindow", "Sources", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHandlers.setText(QtGui.QApplication.translate("MainWindow", "Handlers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpecifications.setText(QtGui.QApplication.translate("MainWindow", "Specifications", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDatabases.setText(QtGui.QApplication.translate("MainWindow", "Databases", None, QtGui.QApplication.UnicodeUTF8))
        self.actionModels.setText(QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAll.setText(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_folder.setText(QtGui.QApplication.translate("MainWindow", "Open folder", None, QtGui.QApplication.UnicodeUTF8))

