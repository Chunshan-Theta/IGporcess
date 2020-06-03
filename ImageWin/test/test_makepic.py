from ImageWin.util.task_pic_maker import PicTaskMaker
from ImageWin.util.frame_base import BoxImg, EventLineFrame1Img1Text

"""
a = BoxImg(img_dir='https://www.tainex1.com.tw/upload/activity/5e55c44b901a9.jpg')
a.show()
a.resize(height=480, width=1280)
a.show()


a = EventLineFrame1Img1Text(img_dir='https://www.tainex1.com.tw/upload/activity/5e55c44b901a9.jpg', content="welcome!")
a_img = a.stack_2_image()
a_img.save("./sample.png")
"""
a = PicTaskMaker()
a.task_exe()
