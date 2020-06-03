import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from uilt import color
import random
import os


## Get Text
txt_arr = []
with open("fighting.txt") as f:
    for row in f.readlines():
        if len(row)<1: continue
        txt_arr.append(row.strip("\n").strip("。").strip("！"))

## get pics
pic_name_arr = [i for i in os.listdir("./img/") if i[-3:] == "png"]


## init var
title_font = ImageFont.truetype('./font/NotoSansMonoCJKtc-Bold.otf',30)
subtitle_font = ImageFont.truetype('./font/NotoSansCJKtc-Regular.otf',25)
title_font_big = ImageFont.truetype('./font/NotoSansMonoCJKtc-Bold.otf',50)
subtitle_font_big = ImageFont.truetype('./font/NotoSansCJKtc-Regular.otf',30)

for _ in range(5):
    for txt in txt_arr:

        ## update var
        pic_file_name = random.choice(pic_name_arr)
        txt = txt.split("，")
        print(txt)

        ## open pic
        f_name = pic_file_name
        img = Image.open("./img/{}".format(f_name))

        ## update pic var
        img_width, img_height = img.size
        img_center = (img_width/2, img_height/2)
        img_center_block = [img_center[0]-250,0,img_center[0]+250,500]

        ## resize
        # img = img.crop([img_center[0]-250,img_height-500,img_center[0]+250,img_height])
        draw = ImageDraw.Draw(img)

        ## add text to pic
        if len(txt) == 1:
            draw.text((127+img_center_block[0], 400), txt[0], color.black,font=title_font if img_width> img_height else title_font_big )
            draw.text((125+img_center_block[0], 400),txt[0],color.yellow_gold,font=title_font if img_width> img_height else title_font_big)
        else:
            idx = random.randint(0,1)
            subtitle_font_len = len(txt[1-idx])*25

            draw.text((477 - subtitle_font_len+img_center_block[0], 400), txt[1-idx], color.black, font=subtitle_font if img_width> img_height else subtitle_font_big)
            draw.text((475 - subtitle_font_len+img_center_block[0], 400), txt[1 - idx], color.white,font=subtitle_font if img_width> img_height else subtitle_font_big)

            draw.text((27+img_center_block[0], 435), txt[idx], color.black, font=title_font if img_width> img_height else title_font_big)
            draw.text((25+img_center_block[0], 435), txt[idx], color.yellow_gold,font=title_font if img_width> img_height else title_font_big)

        ## save to png file
        img.save('./output/{}_{}'.format("，".join(txt),f_name))