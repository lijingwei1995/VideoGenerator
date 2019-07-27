from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

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
        self.set_actions_page2()

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
        self.category = "world"
        for category_tuple in self.spider.category_list:
            self.P1_CB_CAT.addItem(category_tuple[0], category_tuple[1])
        self.P1_CB_CAT.currentIndexChanged.connect(self.page1_CB_CAT_changed)
        self.P1_B_SELECT.clicked.connect(self.page1_B_SELECT_clicked)

        self.page1_LW_NEWS_update() # 默认执行一次采集

    def page1_CB_CAT_changed(self):
        self.P1_LW_NEWS.clear()
        self.category = self.sender().currentData()
        self.page1_LW_NEWS_update()
    
    def page1_LW_NEWS_update(self):
        self.news_list = self.spider.scrape_news_topics(self.category)
        for news_tuple in self.news_list:
            self.P1_LW_NEWS.addItem(news_tuple[0])

    def page1_B_SELECT_clicked(self):
        row = self.P1_LW_NEWS.currentRow()
        if row != -1:
            print(self.news_list[row][1])

    ##### page2 #####
    def set_actions_page2(self):
        self.P2_WEV = QWebEngineView(self.page_2)
        self.P2_WEV.setGeometry(QtCore.QRect(0, 30, 640, 270))
        self.P2_WEV.load(QUrl('https://news.yahoo.co.jp/pickup/6331434'))
        self.P2_WEV.loadFinished.connect(self.page2_WEV_load_finished)
        

    def page2_WEV_load_finished(self):
        self.P2_WEV.page().runJavaScript("window.scrollTo(0,215);")
        self.P2_B_PRINT.setEnabled(True)
        