# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/ljw/HDD/Github/VideoGenerator/VG_UI/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.B1 = QtWidgets.QPushButton(self.centralwidget)
        self.B1.setEnabled(True)
        self.B1.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.B1.setProperty("page_num", 1)
        self.B1.setObjectName("B1")
        self.B2 = QtWidgets.QPushButton(self.centralwidget)
        self.B2.setGeometry(QtCore.QRect(10, 40, 25, 25))
        self.B2.setProperty("page_num", 2)
        self.B2.setObjectName("B2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(30, 0, 20, 351))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(50, 10, 541, 341))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setGeometry(QtCore.QRect(0, 0, 321, 31))
        self.label.setObjectName("label")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 321, 31))
        self.label_2.setObjectName("label_2")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.stackedWidget.addWidget(self.page_3)
        self.B3 = QtWidgets.QPushButton(self.centralwidget)
        self.B3.setGeometry(QtCore.QRect(10, 70, 25, 25))
        self.B3.setProperty("page_num", 3)
        self.B3.setObjectName("B3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setObjectName("menubar")
        self.menuVideo_Generator = QtWidgets.QMenu(self.menubar)
        self.menuVideo_Generator.setObjectName("menuVideo_Generator")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuVideo_Generator.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.B1.setText(_translate("MainWindow", "1"))
        self.B2.setText(_translate("MainWindow", "2"))
        self.label.setText(_translate("MainWindow", "欢迎！\n"
"当前目标：雅虎（日本）新闻，请选择新闻类别"))
        self.label_2.setText(_translate("MainWindow", "修改新闻翻译页"))
        self.B3.setText(_translate("MainWindow", "3"))
        self.menuVideo_Generator.setTitle(_translate("MainWindow", "Video Generator"))
