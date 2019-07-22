# -*- coding: utf-8 -*- 

# from cv2 import cv2
# import numpy
# img = cv2.imread("comment_template.png")
# cv2.putText(img, "你好", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))
# cv2.imshow("result.jpg", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

font_file="font1.otf"
font = ImageFont.truetype(font_file, 20)

im = Image.open("comment_template.png")
draw = ImageDraw.Draw(im)
draw.text((100, 50), "", (0,0,0), font=font)
im.show()

import textwrap
lines = textwrap.wrap(text, width=40)
y_text = h
for line in lines:
    width, height = font.getsize(line)
    draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
    y_text += height
