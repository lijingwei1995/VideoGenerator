from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

from spider import VGSpider
from paint import VGPaint

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 生成spider和paint类
        self.spider = VGSpider()
        self.paint = VGPaint()

        uic.loadUi("VG_UI/mainwindow.ui", self)
        self.set_actions()

    def set_actions(self):
        # 主界面
        # 定义导航按钮组
        self.nav_buttons = [
            self.B1, self.B2, self.B3
        ]
        self.current_button = self.B1
        self.current_button.setEnabled(False)

        # 换页事件
        for button in self.nav_buttons:
            button.clicked.connect(self.change_page)
        
        # 各分页事件
        self.set_actions_page1()

    def change_page(self):
        # QMessageBox.about(self, "click", "yes")
        button_page = self.sender().property("page_num")
        self.stackedWidget.setCurrentIndex(button_page - 1)
        # 按钮状态变换
        self.current_button.setEnabled(True)
        self.current_button = self.sender()
        self.current_button.setEnabled(False)

    ##### page1 #####
    def set_actions_page1(self):
        for category_tuple in self.spider.category_list:
            self.P1_CB_CAT.addItem(category_tuple[0], category_tuple[1])
        self.P1_CB_CAT.currentIndexChanged.connect(self.page1_CB_CAT_changed)

    def page1_CB_CAT_changed(self):
        self.category = self.sender().currentData()
        self.spider.scrape_news_topics(self.category)
