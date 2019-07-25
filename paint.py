# -*- coding: utf-8 -*- 

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import cv2

class VGPaint:
    def __init__(self):
        self.font = ImageFont.truetype("font/font1.otf", 20)

    def paint_picture(self, method = "display"):
        im = Image.open("comment_template.png")
        draw = ImageDraw.Draw(im)

        # origin text
        box_position = (70, 15)
        box_width = 550
        box_height = 150

        text = "1981年，六小龄童参演\n首部电影《阿Q正传》上映。1986年，他主演的古装神话剧《西游记》播出，他因该剧被大众熟知，并获得第六届中国金鹰奖最佳男主角奖 [2-3]  。1993年秋，在电视连续剧《猴娃》中饰演其父六龄童，六小龄童凭借该剧获得中国第十二届“金鹰奖”最佳男配角奖 [4]  。2000年，其主演的古装神话剧《西游记续集》播出，他凭借该剧获得中央电视台颁发的全国十佳优秀演员奖。2003年，在古装武侠剧《连城诀》饰演花铁干，这是他首次饰演反派角色 [5]  。2007年6月，在古装历史神话剧《吴承恩与西游记》中同时饰演吴承恩和孙悟空两个角色 [6-7]  。2009年，参演历史军事情感剧《北平战与和》 [8]  。2015，参演古装神话剧《石敢当之雄峙天东》 [9]  。"

        self.paint_box(draw, box_position, box_width, box_height, "black")
        self.paint_textbox(draw, box_position, box_width, box_height, text, "black", self.font)
        
        if method == "display":

            im.show()
        elif method == "file":
            pass

    def paint_box(self, draw, position, width, height, color):
        xy = (position[0], position[1], position[0] + width, position[1] + height)
        draw.rectangle(xy, outline = color)

    def paint_textbox(self, draw, position, width, height, text, color, font):
        # xy = ((position[0], position[1]), (position[0] + width, position[1] + height))
        draw.multiline_text(position, text, color, font)





# import textwrap
# lines = textwrap.wrap(text, width=40)
# y_text = h
# for line in lines:
#     width, height = font.getsize(line)
#     draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
#     y_text += height
