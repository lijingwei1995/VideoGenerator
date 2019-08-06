from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
            button.clicked.connect(self.change_to_next_page)
        
        # 各分页事件
        self.set_actions_page1()
        self.set_actions_page2()
        self.set_actions_page3()
        self.set_actions_page4()

    # def change_page(self):
    #     # QMessageBox.about(self, "click", "yes")
    #     button_page = self.sender().property("page_num")
    #     self.stackedWidget.setCurrentIndex(button_page - 1)
    #     # 按钮状态变换
    #     self.current_button.setEnabled(True)
    #     self.current_button = self.sender()
    #     self.current_button.setEnabled(False)

    def change_to_next_page(self, next_button):
        if next_button is False:
            next_button = self.sender()
        button_page = next_button.property("page_num")
        self.stackedWidget.setCurrentIndex(button_page - 1)
        self.current_button.setEnabled(True)
        self.current_button = next_button
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
            self.news_title = self.news_list[row][0]
            self.pickup_url = self.news_list[row][1]
            # 页面2读取新闻封面
            self.P2_WEV.load(QUrl(self.pickup_url))
            # 将标题传给页面2的Line Edit
            self.P2_LE_TITLE.setText(self.news_title)
            self.P2_L_TITLE.setText(self.news_title)
            # 页面1 -> 页面2
            self.change_to_next_page(self.B2)

    ##### page2 #####
    def set_actions_page2(self):
        # 生成WebEngineView及Mask
        self.P2_WEV = QWebEngineView(self.page_2)
        self.P2_WEV.setGeometry(QtCore.QRect(0, 30, 640, 270))
        self.P2_WEV.hide() 
        self.P2_WEV_MASK = QWidget(self.page_2)
        self.P2_WEV_MASK.setGeometry(QtCore.QRect(0, 30, 640, 270))
        self.P2_WEV.loadFinished.connect(self.page2_WEV_load_finished)
        # 生成标题label
        self.P2_LE_TITLE = QtWidgets.QLineEdit(self.page_2)
        self.P2_LE_TITLE.setGeometry(QtCore.QRect(0, 350, 641, 41))
        self.P2_LE_TITLE.setObjectName("P2_LE_TITLE")
        self.P2_LE_TITLE.textChanged.connect(lambda: self.P2_L_TITLE.setText(self.sender().text()))
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setGeometry(QtCore.QRect(0, 65, 625, 90))
        self.label_5.setStyleSheet( "font: 28pt \"Noto Sans Mono CJK\";\n"
                                    "color:white;\n"
                                    "background-color: rgba(0,0,0,0.5);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("  日网评论：")
        self.P2_L_TITLE = QtWidgets.QLabel(self.page_2)
        self.P2_L_TITLE.setGeometry(QtCore.QRect(0, 155, 625, 90))
        self.P2_L_TITLE.setStyleSheet(  "font: 28pt \"Noto Sans Mono CJK\";\n"
                                        "color:white;\n"
                                        "background-color: rgba(0,0,0,0.5);")
        self.P2_L_TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.P2_L_TITLE.setObjectName("P2_L_TITLE")
        
        # "打印"按钮的槽
        self.P2_B_PRINT.clicked.connect(self.page2_B_PRINT_clicked)

        # "滚动"按钮的槽
        self.P2_B_SCROLL.clicked.connect(lambda: self.P2_WEV.page().runJavaScript("window.scrollTo(0,215);"))

    def page2_WEV_load_finished(self):
        self.P2_WEV.page().runJavaScript("window.scrollTo(0,215);")
        self.P2_WEV.show()
        self.P2_B_PRINT.setText("打印")
        self.P2_B_PRINT.setEnabled(True)

    def page2_B_PRINT_clicked(self):
        # 截图，保存
        pixmap = self.page_2.grab(QtCore.QRect(2, 30, 640-15-2, 270-15))
        pixmap.save("cache/cover.png", "png")
        # 获取新闻摘要和评论地址
        self.pickup, self.comment_page_url = self.spider.scrape_news_pickup(self.pickup_url)

        if self.comment_page_url is None:
            QMessageBox.about(self, "错误", "此新闻不含有评论")

        # 传递值
        self.P3_TB_PICKUP.setText(self.pickup)
        self.P3_PTE_PICKUP.setPlainText(self.pickup)
        # 页面2 -> 页面3
        self.change_to_next_page(self.B3)

    ##### page3 #####
    def set_actions_page3(self):
        # 确定键
        self.P3_B_CONFIRM.clicked.connect(self.page3_B_CONFIRM_clicked)

    def page3_B_CONFIRM_clicked(self):
        # 画新闻摘要
        pixmap = QPixmap()
        pixmap.load("pickup_template.png")
        painter = QPainter()
        painter.begin(pixmap)
        # title
        painter.setFont(QFont("Noto Sans Mono CJK", 20))
        painter.drawText(20, 120, self.news_title)
        # pickup
        painter.setFont(QFont("Noto Sans Mono CJK", 14))
        option = QTextOption(Qt.AlignJustify)
        option.setWrapMode(QTextOption.WordWrap)
        painter.drawText(QtCore.QRectF(20, 140, 580, 330), self.P3_PTE_PICKUP.toPlainText(), option)
        painter.end()
        pixmap.save("cache/pickup.png", "png")

        # 抓取评论
        self.comment_num = 20
        self.current_comment = 0
        self.news_comments = self.spider.scrape_news_comments(self.comment_page_url, self.comment_num)
        self.news_comments_t = self.news_comments[:] # translate
        # 传递
        self.change_comment(self.current_comment)
        # 页面3 -> 页面4
        self.change_to_next_page(self.B4)

    ##### page4 #####
    def set_actions_page4(self):
        # 前后按钮
        self.P4_B_NEXT.clicked.connect(lambda: self.change_comment(self.current_comment + 1))
        self.P4_B_PREVIOUS.clicked.connect(lambda: self.change_comment(self.current_comment - 1))
    
    def change_comment(self, index):
        # 保存翻译编辑框值
        if self.P4_PTE_COMMENT.toPlainText() != "":
            self.news_comments_t[self.current_comment] = self.P4_PTE_COMMENT.toPlainText()
        # 值传递
        self.current_comment = index
        # 编辑框赋值
        self.P4_TB_COMMENT.setText(self.news_comments[self.current_comment])
        self.P4_PTE_COMMENT.setPlainText(self.news_comments_t[self.current_comment])
        # 数字显示
        self.P4_L_NUMBER.setText(str(self.current_comment+1) + "/" + str(self.comment_num))
        # 按钮可点性
        # PREVIOUS
        if self.current_comment == 0:
            self.P4_B_PREVIOUS.setEnabled(False)
        else:
            self.P4_B_PREVIOUS.setEnabled(True)
        # NEXT
        if self.current_comment == self.comment_num - 1:
            self.P4_B_NEXT.setEnabled(False)
        else:
            self.P4_B_NEXT.setEnabled(True)