# -*- coding: utf-8 -*- 

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter

# import cv2

class VGPaint:
    def __init__(self):
        self.font_file = "font/font1.otf"
        self.font_size = 18
        self.font = ImageFont.truetype(self.font_file, self.font_size)

    def paint_picture(self, method = "display"):
        im = Image.open("comment_template.png")
        draw = ImageDraw.Draw(im)

        # origin text
        box_position = (70, 15)
        box_width = 550
        box_height = 150
        text = ""

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
        import textwrap
        lines = textwrap.fill(text, width = 30)
        draw.multiline_text(position, lines, color, font)

    ### 自定义处理
    def handle_cover_picture(self):
        # 由原图生成高斯模糊+拉伸的背景
        im = Image.open("cache/cover_bg.png")
        im_bg = im.resize((935, 600))
        im_bg = im_bg.filter(ImageFilter.GaussianBlur(10))
        im_bg.paste(Image.open("cache/cover.png"), (0, 40))
        im_bg.save("cache/cover_f.png")
        im_bg = im_bg.resize((960, 600))
        im_bg.save("output/cover_bili.png")

    def calculate_img_in_box(self, img_size, box_size):
        d = 2
        max_rate = 0
        for i in range(d):
            rate = img_size[i] / box_size[i]
            if rate > max_rate:
                max_rate = rate
        
        resize = []
        pos = []
        for i in range(d):
            resize_l = img_size[i] / max_rate
            resize.append(int(resize_l))
            pos.append(int((box_size[i] - resize_l) / 2))

        return tuple(resize), tuple(pos)

    def paint_black_bg(self, folder, img_name, bg_size):
        im_bg = Image.new("RGB", bg_size, "black")
        im = Image.open(folder + "/" + img_name + ".jpg")

        size, pos = self.calculate_img_in_box(im.size, bg_size)
        
        im2 = im.resize(size)
        im_bg.paste(im2, pos)

        im_bg.save(folder + "/" + img_name + "_b.png")
        
        return im_bg

    # 居中打印，默认黑底白字
    def paint_center_textbox(self, box_size, font_size, text):
        font = ImageFont.truetype("font/NotoSansCJK-Bold.otf", font_size)
        text_width = font.getsize(text)
        im_bg = Image.new("RGB", box_size, "black")
        draw = ImageDraw.Draw(im_bg)
        # 计算字体位置
        text_coordinate = int((box_size[0]-text_width[0])/2), int((box_size[1]-text_width[1])/2)
        # 写字
        draw.text(text_coordinate, text, "white", font=font)
        # im_bg.save("cache2/cover_title.png")
        return im_bg

    def handle_cover_picture2(self, text):
        # 由原图生成高斯模糊+拉伸的背景
        im = Image.open("cache2/img (0).png")
        im_bg = im.resize((935, 600))
        im_bg = im_bg.filter(ImageFilter.GaussianBlur(10))
        im_bg.paste(Image.new("RGB", (935, 520), "black"), (0, 40))

        if im.size[0] / im.size[1] < 1.5:
            # thumb
            size, pos = self.calculate_img_in_box(im.size, (520, 540))
            im_bg.paste(im.resize(size), (pos[0], pos[1]+30))
            # title 分组
            g = 6
            n_g = int(len(text) / g)
            t_multi = [text[i*g:(i+1)*g] for i in range(n_g)]
            if len(text) > n_g * g:
                t_multi.append(text[n_g * g:])
            # paint
            single_l = 935 - 520 + pos[0]
            single_h = 120
            y_pos = int((520 - len(t_multi) * single_h) / 2) + 40
            for t in t_multi:
                im_bg.paste(self.paint_center_textbox((single_l, single_h), 64, t), (935 - single_l, y_pos))
                y_pos = y_pos + single_h
        else:
            size, pos = self.calculate_img_in_box(im.size, (935, 380))
            im_bg.paste(im.resize(size), (pos[0], 600-40-size[1]))
            im_bg.paste(self.paint_center_textbox((935, 600-80-size[1]), 64, text), (0, 40))
        
        im_bg.save("cache2/cover_f.png")
        im_bg = im_bg.resize((960, 600))
        im_bg.save("output/cover_bili.png") 
# import textwrap
# lines = textwrap.wrap(text, width=40)
# y_text = h
# for line in lines:
#     width, height = font.getsize(line)
#     draw.text(((w - width) / 2, y_text), line, font=font, fill=FOREGROUND)
#     y_text += height

# 测试代码
if __name__ == "__main__":
    p = VGPaint()
    # p.paint_black_bg("cache2", "img", (935, 600))
    # p.paint_center_textbox((935, 140), 64, "日本网友评论")
    p.handle_cover_picture2("韓国メディアが報じた。検察が同日未明に逮捕状を請")
    # t = "1234567890abcde"
    # g = 6
    # n_g = int(len(t) / g)
    # t2 = [t[i*g:(i+1)*g] for i in range(n_g)]
    # if len(t) > n_g * g:
    #     t2.append(t[n_g * g:])
    # print(t2)