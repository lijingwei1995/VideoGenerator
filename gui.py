from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("VG_UI/mainwindow.ui", self)
        self.set_actions()

    def set_actions(self):
        # 定义导航按钮组
        self.nav_buttons = [
            self.B1, self.B2, self.B3
        ]
        self.current_button = self.B1
        self.current_button.setEnabled(False)

        # 换页事件
        for button in self.nav_buttons:
            button.clicked.connect(self.change_page)

    def change_page(self):
        # QMessageBox.about(self, "click", "yes")
        button_page = self.sender().property("page_num")
        self.stackedWidget.setCurrentIndex(button_page - 1)
        # 按钮状态变换
        self.current_button.setEnabled(True)
        self.current_button = self.sender()
        self.current_button.setEnabled(False)

