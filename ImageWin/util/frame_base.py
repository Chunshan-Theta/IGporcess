import datetime
import shutil
from io import StringIO

import requests
from PIL import ImageFont, ImageDraw
from PIL.Image import Image
import PIL
from ImageWin.util.config import FONTDIR


class Box(object):
    def __init__(self, block_width: float, block_height: float):
        self.block_width = block_width
        self.block_height = block_height
        self.background_color: str = str()
        self.block_type: str = "general"
        self.box_label = None

    def to_pic(self) -> Image:
        raise NotImplementedError

    def resize(self, height: int, width: int):
        raise NotImplementedError

    def mask(self, im:Image, color) -> Image:
        gray_mask = PIL.Image.new(mode="RGBA", color=color, size=im.size)
        im.paste(im=gray_mask, box=(0, 0), mask=gray_mask)
        return im

    @classmethod
    def color_similarity(cls, im: Image, a: int = None) -> tuple:
        def non_white(colors: tuple):
            colors = (255,255,255,255) if isinstance(colors, int) else colors
            for c in colors:
                if c != 255:
                    return True
            return False

        R, G, B, A = 0, 0, 0, 0

        pixels = [i for i in im.getdata() if non_white(i)]
        pix_num = len(pixels)

        for pixel in pixels:
            R += pixel[0]
            G += pixel[1]
            B += pixel[2]
            if len(pixel) == 4:
                A += pixel[3]
            else:
                A += 10

        # empty_photo
        if all([R, G, B, A]) or pix_num == 0:
            return 255, 255, 255, 100

        return int(R / pix_num), int(G / pix_num), int(B / pix_num), int(A / pix_num) if a is None else a


class BoxImg(Box):
    def __init__(self, img_dir: str, block_width=12, block_height=12, border=15):
        super().__init__(block_width=block_width, block_height=block_height)
        self.img_dir = img_dir
        self.block_type = "Img"
        self.im: PIL.Image.Image = PIL.Image.open(self.get_photo(img_dir=img_dir))
        if self.im.height >4000 or self.im.width>4000:
            self.im = self.im.resize((int(self.im.width/4),int(self.im.height/4)))
        self.block_height, self.block_width = self.im.size
        self.border = border

        assert isinstance(self.im, Image), "Not found the Image."

    def check_image(self) -> bool:
        return True

    def show(self):
        self.im.show()

    def get_photo(self, img_dir: str = None, save_pic=False, save_pic_name="sample"):
        self.img_dir = self.img_dir if img_dir is None else img_dir
        r = requests.get(self.img_dir, stream=True, timeout=10)
        if r.status_code == 200:
            print("got photo")
            if save_pic:
                with open(f"./{save_pic_name}.png", 'wb') as f:
                    r.raw.decode_content = True

                    shutil.copyfileobj(r.raw, f)
            print("returned photo")
            return r.raw

        return None

    def resize(self, height: int, width: int):
        self.im = self.im.resize((width, height))
        self.block_width, self.block_height = width, height
        return self.im

    def to_pic(self) -> Image:
        new_im = PIL.Image.new(mode="RGBA", size=self.im.size, color=(255, 255, 255, 255))
        reset_now_pic = self.im.copy().resize(size=(v - self.border*2 for v in self.im.size))
        new_im.paste(im=reset_now_pic, box=(self.border, self.border))
        mask_color = self.color_similarity(im=new_im, a=15)
        new_im = self.mask(im=new_im, color=mask_color)
        return new_im


class BoxText(Box):

    def __init__(self, content: str, block_width=12, block_height=12, font_size=12, bold: bool = False,
                 text_color=(0, 0, 0, 255), text_xy=(0, 0), mask_color=(255, 97, 0, 20)):
        super().__init__(block_width=block_width, block_height=block_height)
        self.content = content
        self.text_size = 12
        self.block_type = "Text"
        self.im = PIL.Image.new(mode="RGBA", size=(1280, 1280), color=(255, 255, 255, 255))
        self.p_font = ImageFont.truetype(f"{FONTDIR}NotoSansCJKtc-Thin.otf", font_size) if not bold else \
            ImageFont.truetype(f"{FONTDIR}NotoSansMonoCJKtc-Bold.otf", font_size)
        self.fill = text_color
        self.text_xy = text_xy
        self.mask_color = mask_color

    def resize(self, height: int, width: int):
        self.im = self.im.resize((width, height))
        self.block_width, self.block_height = width, height
        return self.im

    def to_pic(self,text_xy=None) -> Image:

        draw = ImageDraw.Draw(self.im)
        text_xy = text_xy if text_xy is not None else self.text_xy
        draw.text(xy=text_xy, text=self.content, fill=self.fill, font=self.p_font)
        return self.mask(im=self.im, color=self.mask_color)


class Frame(object):

    def __init__(self, default_size:tuple):
        self.background_color = "#FFFFFF"
        self.default_size = default_size

    def stack(self) -> list:
        raise NotImplementedError

    def stack_2_image(self) -> Image:
        raise NotImplementedError


class LineFrame(Frame):
    """
    |-------------|
    |-------------|
    |             |
    |-------------|
    |             |
    |-------------|
    |-------------|

    """

    def __init__(self, center_1_block: Box, center_2_block: Box, top_bar: Box, bottom_bar: Box, default_size:tuple):
        super().__init__(default_size=default_size)
        self.center_1_block = center_1_block
        self.center_2_block = center_2_block
        self.top_bar = top_bar
        self.bottom_bar = bottom_bar

    def stack(self) -> list:
        return [self.top_bar, self.center_1_block, self.center_2_block, self.bottom_bar]

    def stack_2_image(self) -> Image:

        im = PIL.Image.new(mode="RGBA", color=(255, 255, 255, 255), size=self.default_size)


        current_width, current_height = 0, 0
        for item in self.stack():
            print(f"item.block_width:{item.block_width}, item.block_height:{item.block_height}")
            item_im = item.to_pic()
            im.paste(im=item_im, box=(0, current_height))
            current_height += item.block_height


        return im


class WinFrame(Frame):
    """
    |-------------|
    |-------------|
    |      |      |
    |      |      |
    |      |      |
    |-------------|
    |-------------|

    """

    def __init__(self, center_right_block: Box, center_left_block: Box, top_bar: Box, bottom_bar: Box):
        super().__init__()
        self.center_right_block = center_right_block
        self.center_left_block = center_left_block
        self.top_bar = top_bar
        self.bottom_bar = bottom_bar

    def stack(self) -> list:
        return [self.top_bar, self.center_left_block, self.center_right_block, self.bottom_bar]


class EventLineFrame1Img1Text(LineFrame):

    def __init__(self, img_dir: str, content: str, image_title: str = "ForValue", default_size=(720, 720)):

        center_img_block, center_text_block, top_bar, bottom_bar = None, None, None, None

        # initiate block
        main_img = BoxImg(img_dir=img_dir,border=15)
        text_mask_color = BoxImg.color_similarity(im=main_img.im, a=20)
        main_content = BoxText(content=content, font_size=25, text_xy=(15, 0),mask_color=text_mask_color)
        top_bar = BoxText(content=image_title, font_size=95, text_color=(235, 235, 235, 255), mask_color=text_mask_color)
        bottom_bar = BoxText(content="每天來一點世界 | 點選標籤查詢更多當日活動", bold=True, font_size=20, text_color=(200, 200, 200, 255), text_xy=(15, 10),mask_color=text_mask_color)

        # setting args for super()
        center_img_block = main_img
        center_text_block = main_content

        center_img_block.box_label = "image block"
        top_bar.box_label = "top_bar"
        bottom_bar.box_label = "bottom_bar"
        center_text_block.box_label = "center_text_block"

        # assert args
        assert None not in [center_img_block, center_text_block, top_bar, bottom_bar], "Box Not Implemented"

        #
        super().__init__(center_1_block=center_img_block,
                         center_2_block=center_text_block,
                         top_bar=top_bar,
                         bottom_bar=bottom_bar,
                         default_size=default_size)


        # setting block
        unit_frame_width, unit_frame_height = (int(n/12) for n in self.default_size)
        center_1_block_width = int(12 * unit_frame_width)
        center_1_block_height = int(6 * unit_frame_height)
        self.center_1_block.resize(height=center_1_block_height, width=center_1_block_width)

        center_2_block_width = int(12 * unit_frame_width)
        center_2_block_height = int(3 * unit_frame_height)
        self.center_2_block.resize(height=center_2_block_height, width=center_2_block_width)

        top_block_width = int(12 * unit_frame_width)
        top_block_height = int(2 * unit_frame_height)
        self.top_bar.resize(height=top_block_height, width=top_block_width)

        bottom_block_width = int(12 * unit_frame_width)
        bottom_block_height = int(1 * unit_frame_height)
        self.bottom_bar.resize(height=bottom_block_height, width=bottom_block_width)


class EventWinFrame1Img1Text(WinFrame):

    def __init__(self, img_dir: str, content: str):

        center_left_block, center_right_block, top_bar, bottom_bar = None, None, None, None

        # initiate block
        main_img = BoxImg(img_dir=img_dir)
        main_content = BoxText(content=content)
        top_bar = BoxText(content="Needed setting!!")
        bottom_bar = BoxText(content="Needed setting!!")

        # setting args for super()
        center_left_block = main_img
        center_right_block = main_content

        # assert args
        assert None not in [center_left_block, center_right_block, top_bar, bottom_bar], "Box Not Implemented"

        #
        super().__init__(center_left_block=center_left_block,
                         center_right_block=center_right_block,
                         top_bar=top_bar,
                         bottom_bar=bottom_bar)
