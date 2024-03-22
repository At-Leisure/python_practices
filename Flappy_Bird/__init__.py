""" # $FlappyBird_{~~_{python-3.10.8}}$
PythonPackages : pygame pillow ...

## 0.x 版本 - 基本实现游戏运行 - 2022/12/04
#### $~~~~~~...$
1) - 实现显示小鸟
2) - 实现显示圆柱
3) - 检测是否碰到和通过
4) - 实现显示数字
5) - 丰富小鸟的动画
6) - 实现游戏重新开始

## 1.x 版本 进一步完善游戏的外观 - 
#### $~~~~~~优化代码架构，添加开始、设置界面等其他有关游戏的画面$
1) - 优化代码
2) - 开始界面
3) - 设置界面
4) - 
5) - 

## 2.x 版本 - 添加材质包功能 - 
#### $~~~~~~类似于方块游戏minecraft，采用json文件来判断替换的图片$
1) - 使用子线程添加启动动画
2) - 
3) - 

## ... """
from pathlib import Path
from PIL import Image

from .resrc import resource





# 改变大小-进行压缩或反压缩


def resize_picture(path, rate):
    img = Image.open(path)
    width = img.size[0]   # 获取宽度
    height = img.size[1]   # 获取高度
    img = img.resize((int(width*rate), int(height*rate)), Image.ANTIALIAS)
    img.save(path.split('\\')[-1])

# 改变透明度


def change_alpha(path):
    img = Image.open(path)
    img = img.convert('RGBA')  # 修改颜色通道为RGBA
    x, y = img.size  # 获得长和宽

    # 设置每个像素点颜色的透明度
    for i in range(x):
        for k in range(y):
            color = img.getpixel((i, k))
            color = color[:-1] + (100, )
            img.putpixel((i, k), color)
    img.save(path.split('\\')[-1])
