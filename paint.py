# -*- coding: utf-8 -*- 

# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw

import PIL
import cv2

class VGPaint:
    def __init__(self):
        self.font = ImageFont.truetype("font1.otf", 20)
    def draw_comment(self):
        im = Image.open("comment_template.png")
        draw = ImageDraw.Draw(im)
        draw.text((100, 50), "", (0,0,0), font = self.font)
        im.show()




# import textwrap
# lines = textwrap.wrap(text, width=40)
# y_text = h
# for line in lines:
#     width, height = font.getsize(line)
#     draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
#     y_text += height
