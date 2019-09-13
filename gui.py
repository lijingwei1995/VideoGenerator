# -*- coding: utf-8 -*- 

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from spider import VGSpider
from paint import VGPaint
from translator import VGTranslator

import os
import time
import webbrowser

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 生成spider和paint类
        self.spider = VGSpider()
        self.paint = VGPaint()
        self.translator = VGTranslator()

        # 记录log
        # 新建文件夹
        # 生成文件夹名
        self.log_folder = time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time()))
        self.log_folder_path = "log/" + self.log_folder + "/"

        uic.loadUi("VG_UI/mainwindow.ui", self)
        self.set_actions()

    def __del__(self):
        pass
        # self.f_log.close()

    def write_log(self, str):
        if not os.path.exists(self.log_folder_path):
            os.mkdir(self.log_folder_path)
        self.f_log = open(self.log_folder_path + "log.txt", "a", encoding='utf-8')
        self.f_log.write(str)
        self.f_log.close()

    def set_actions(self):
        # 主界面
        # 定义导航按钮组
        self.nav_buttons = [
            self.B1, self.B2, self.B3, self.B4, self.B5
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
        self.set_actions_page5()

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
            # 翻译封面
            self.news_title = self.translator.translate(self.news_title)
            # 页面2读取新闻封面
            self.P2_WEV.load(QUrl(self.pickup_url))
            # 将标题传给页面2的Line Edit
            self.P2_LE_TITLE.setText(self.news_title)
            # self.P2_L_TITLE.setText(self.news_title)
            # 页面1 -> 页面2
            self.change_to_next_page(self.B2)

    ##### page2 #####
    def set_actions_page2(self):
        # 生成WebEngineView及Mask
        self.P2_WEV = QWebEngineView(self.page_2)
        self.P2_WEV.setZoomFactor(1.5)
        self.P2_WEV.setGeometry(QtCore.QRect(0, 30+140, 640+312, 270+125))
        # self.P2_WEV.hide() 
        # self.P2_WEV_MASK = QWidget(self.page_2)
        # self.P2_WEV_MASK.setGeometry(QtCore.QRect(0, 30+140, 640+312, 270+125))
        # self.P2_WEV.loadFinished.connect(self.page2_WEV_load_finished)

        # 标题的前景色和背景色
        def update_color_button(b, c):
            b.setStyleSheet("background-color:"+c.name()+";")
        def update_title_color():
            self.P2_L_TITLE.setStyleSheet(  "font: 52pt \"Noto Sans CJK Bold\";"
                                "color:"+self.title_font_color.name()+";"
                                "background-color:"+self.title_back_color.name()+";"
                                )
        def update_title_font_color():
            self.title_font_color = QColorDialog.getColor()
            update_color_button(self.P2_B_FONTCOLOR, self.title_font_color)
            update_title_color()
        def update_title_back_color():
            self.title_back_color = QColorDialog.getColor()
            update_color_button(self.P2_B_BACKCOLOR, self.title_back_color)
            update_title_color()

        # 默认
        self.title_font_color = QColor(255, 255, 255)
        self.title_back_color = QColor(0, 0, 0)
        update_color_button(self.P2_B_FONTCOLOR, self.title_font_color)
        update_color_button(self.P2_B_BACKCOLOR, self.title_back_color)

        # 改变
        self.P2_B_FONTCOLOR.clicked.connect(update_title_font_color)
        self.P2_B_BACKCOLOR.clicked.connect(update_title_back_color)

        # 生成标题label
        # self.P2_LE_TITLE = QtWidgets.QLineEdit(self.page_2)
        # self.P2_LE_TITLE.setGeometry(QtCore.QRect(0, 350, 641, 41))
        # self.P2_LE_TITLE.setObjectName("P2_LE_TITLE")
        self.P2_LE_TITLE.textChanged.connect(lambda: self.P2_L_TITLE.setText(self.sender().text()))
        # self.label_5 = QtWidgets.QLabel(self.page_2)
        # self.label_5.setGeometry(QtCore.QRect(0, 65+55, 625+312, 90))
        # self.label_5.setStyleSheet( "font: 45pt \"Noto Sans Mono CJK\";\n"
        #                             "color:white;\n"
        #                             "background-color: rgba(0,0,0,0.5);"
        #                             "font-weight:550"
        #                             )
        # self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        # self.label_5.setObjectName("label_5")
        # self.label_5.setText("  日本网友评论：")
        self.P2_L_TITLE = QtWidgets.QLabel(self.page_2)
        self.P2_L_TITLE.setGeometry(QtCore.QRect(0, 30, 940, 140))
        update_title_color()
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
        pixmap = self.page_2.grab(QtCore.QRect(0+2, 30, 935, 520)) # 起始坐标加长宽
        pixmap.save("cache/cover.png", "png")
        pixmap = self.page_2.grab(QtCore.QRect(0+2, 30+140, 935, 330))
        pixmap.save("cache/cover_bg.png", "png")
        self.paint.handle_cover_picture()
        # 获取新闻摘要和评论地址
        self.pickup, self.comment_page_url, self.detail_url = self.spider.scrape_news_pickup(self.pickup_url)

        self.pickup_t = self.translator.translate(self.pickup)

        if self.comment_page_url is None:
            QMessageBox.about(self, "错误", "此新闻不含有评论")

        # 传递值
        self.P3_TB_PICKUP.setText(self.pickup)
        self.P3_PTE_PICKUP.setPlainText(self.pickup_t)

        # 记录log
        # 写入标题
        self.write_log(self.detail_url+"\n\ntitle:日本网友评论："+self.P2_LE_TITLE.text()+"\n")


        # 页面2 -> 页面3
        self.change_to_next_page(self.B3)

    ##### page3 #####
    def set_actions_page3(self):
        # 确定键
        self.P3_B_CONFIRM.clicked.connect(self.page3_B_CONFIRM_clicked)
        # 打开原网页
        self.P3_B_OPEN_URL.clicked.connect(lambda: webbrowser.open(self.detail_url))

    def page3_B_CONFIRM_clicked(self):
        # 画新闻摘要
        pixmap = QPixmap()
        pixmap.load("template/pickup_template.png")
        painter = QPainter()
        painter.begin(pixmap)
        # title
        painter.setFont(QFont("Noto Sans CJK Bold", 30))
        painter.drawText(20, 180, self.P2_LE_TITLE.text())
        # pickup
        painter.setFont(QFont("Noto Sans CJK Bold", 21))
        option = QTextOption(Qt.AlignJustify)
        option.setWrapMode(QTextOption.WordWrap)
        painter.drawText(QtCore.QRectF(20, 210, 900, 550), self.P3_PTE_PICKUP.toPlainText(), option)
        painter.end()
        pixmap.save("cache/pickup.png", "png")

        # 记录log
        # 写入摘要
        self.write_log("\npickup:"+self.P3_PTE_PICKUP.toPlainText()+"\n")

        # 抓取评论
        self.comment_num = 10
        self.current_comment = 0
        try:
            self.news_comments, self.news_authors = self.spider.scrape_news_comments(self.comment_page_url, self.comment_num)
            self.news_comments_t = self.translator.translate_list(self.news_comments[:]) # translate
        except Exception as e:
            QMessageBox.about(self, "错误", str(e))
        else:
            # 传递
            self.change_comment(self.current_comment)
            # 页面3 -> 页面4
            self.change_to_next_page(self.B4)

    ##### page4 #####
    def set_actions_page4(self):
        # 前后按钮
        self.P4_B_NEXT.clicked.connect(lambda: self.change_comment(self.current_comment + 1))
        self.P4_B_PREVIOUS.clicked.connect(lambda: self.change_comment(self.current_comment - 1))
        # 完成按钮
        self.P4_B_FINISH.clicked.connect(self.page4_B_FINISH_clicked)
        # 生成单页按钮
        self.P4_B_CONVERT_ONE.clicked.connect(self.page4_B_CONVERT_ONE_clicked)

    
    def change_comment(self, index):
        # 保存翻译编辑框值
        if self.P4_PTE_COMMENT.toPlainText() != "":
            self.news_comments[self.current_comment] = self.P4_PTE_COMMENT_S.toPlainText()
            self.news_comments_t[self.current_comment] = self.P4_PTE_COMMENT.toPlainText()
        # 值传递
        self.current_comment = index
        # 编辑框赋值
        # self.P4_TB_COMMENT.setText(self.news_comments[self.current_comment])
        self.P4_PTE_COMMENT_S.setPlainText(self.news_comments[self.current_comment])
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

    def page4_paint_conmment_picture(self, i):
            a = self.news_authors[i]
            c = self.news_comments[i]
            ct = self.news_comments_t[i]

            # 生成评论图片
            pixmap = QPixmap()
            pixmap.load("template/comment_template2.png")
            painter = QPainter()
            painter.begin(pixmap)
            # author
            painter.setFont(QFont("Noto Sans CJK Bold", 15))
            painter.drawText(110, 55, a)
            # comments & translate
            painter.setFont(QFont("Noto Sans CJK Bold", 18))
            option = QTextOption(Qt.AlignJustify)
            option.setWrapMode(QTextOption.WordWrap)
            painter.drawText(QtCore.QRectF(110, 75, 810, 355), c, option)
            painter.setFont(QFont("Noto Sans CJK Bold", 21))
            painter.setPen(Qt.red)
            painter.drawText(QtCore.QRectF(110, 310, 800, 550), ct, option)
            
            painter.end()
            pixmap.save("cache/comment"+str(i+1)+".png", "png")

            # 记录log
            # 写入评论
            self.write_log(str(i+1)+"\t:"+ct+"\n\n")

    def page4_B_CONVERT_ONE_clicked(self):
        # 保存翻译编辑框值
        if self.P4_PTE_COMMENT.toPlainText() != "":
            self.news_comments[self.current_comment] = self.P4_PTE_COMMENT_S.toPlainText()
            self.news_comments_t[self.current_comment] = self.P4_PTE_COMMENT.toPlainText()
            # 写入评论
            self.write_log(str(self.current_comment+1)+"\t:"+self.news_comments_t[self.current_comment]+"\n\n")
            
        self.page4_paint_conmment_picture(self.current_comment)

    def page4_B_FINISH_clicked(self):
        # 提示效果
        # self.P4_L_HINT.setText("生成中...")
        
        # 保存翻译编辑框值
        if self.P4_PTE_COMMENT.toPlainText() != "":
            self.news_comments[self.current_comment] = self.P4_PTE_COMMENT_S.toPlainText()
            self.news_comments_t[self.current_comment] = self.P4_PTE_COMMENT.toPlainText()

        # 记录log
        self.write_log("\ncomments:\n")

        for i in range(self.comment_num):
            self.page4_paint_conmment_picture(i)

        
        # 生成视频
        command = "ffmpeg -y -f concat -safe 0 -i video_config.txt output/output.wmv"

        if os.system(command) == 0:
            QMessageBox.about(self, "成功", "完成")
            # self.P4_L_HINT.setText("")
        else:
            QMessageBox.about(self, "错误", "失败")
            # self.P4_L_HINT.setText("")

        # 打开log
        command ="start log\\" + self.log_folder + "\\log.txt"
        print(command)
        os.system(command)

        # 页面4 -> 页面5
        self.change_to_next_page(self.B5)

    ##### page5 #####
    def set_actions_page5(self):
        bgms = os.listdir("bgm/")
        for bgm in bgms:
            self.P5_LW_BGMS.addItem(bgm)

        self.P5_B_CONVERT_VIDEO.clicked.connect(self.page4_B_CONVERT_VIDEO_clicked)
        self.P5_B_ADD_BGM.clicked.connect(self.page4_B_ADD_BGM_clicked)

    def page4_B_CONVERT_VIDEO_clicked(self):
        command = "ffmpeg -y -f concat -safe 0 -i video_config.txt -b 1.2M output/output.wmv"
        if os.system(command) == 0:
            QMessageBox.about(self, "成功", "完成")
    
    def page4_B_ADD_BGM_clicked(self):
        item = self.P5_LW_BGMS.currentItem()
        if item is not None:
            bgm = item.text()
            command = "ffmpeg -y -i bgm/" + bgm + " -i output/output.wmv -shortest -b 1.2M output/output_final.wmv"
            if os.system(command) == 0:
                QMessageBox.about(self, "成功", "完成")
        else:
            QMessageBox.about(self, "错误", "未选择bgm")


