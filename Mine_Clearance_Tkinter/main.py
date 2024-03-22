""" 
名称：《扫雷》 \\
作者：ZhouYafei \\
日期：2022/07 \\
英文：Mine Clearance \\
纪念：第一次使用Python和第一次使用GUI编写的第一个游戏程序
encoding: UTF-8
"""


# 更新内容:  删除上边栏+修改地雷生成函数+使用列表生成式

from tkinter import *
from tkinter import font
from random import randint


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 窗口相关 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
# 主窗口设置
win = Tk()
win.title("《扫雷2.4.0》: Made By ZYF")
win.geometry("600x550+500+200")
# win.overrideredirect(True)
BackGround = "darkslategray"
# win.configure(background=BackGround)
# 背景色
NormalBG = BackGround
StartBG = BackGround
DiffiBG = BackGround
# 字体格式
win.MyFont = font.Font(family="楷体", size=14, weight=font.BOLD, underline=1)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 全局变量 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
# 是否显示按钮
IsButtonSet = True
# 是否明示地雷 如果按钮大小不一致,可关闭此值或者修改mineExpress()函数
IsExpressMine = False
# 是否结束
IsOver = False
# 记录难度
recording = "默认"
# 初始左距 初始上距
RawLf = RawUp = 2
# 全局变量:长宽,地雷数量
width = 10
MineNum = 6
mine = set()
MaxWidth = 12
# 普通标签和按钮
lbl = []
btn = []
# 标签数值,已打开按钮
tag = []
opened = []


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 版本变量 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
# 2.0生成足量的Label Button
lbl = [[Label(win, text="L", padx=12, pady=5)
        for y in range(MaxWidth)] for x in range(MaxWidth)]
btn = [[] for x in range(MaxWidth)]
# 2.0生成足量的按钮分命令函数
for x in range(MaxWidth):
    for y in range(MaxWidth):
        exec("def hit_"+str(x)+"_"+str(y)+"():click("+str(x)+","+str(y)+")")
        exec(
            r'btn[x].append(Button(win,text="  ",padx=9,command=hit_'+str(x)+"_"+str(y)+"))")
# 2.1设置等级按钮 1/2/3


def 难度1():
    global width, MineNum, recording
    width = 8
    MineNum = 3
    # hideDifficulty()
    recording = "入手"
    难度等级.configure(text=recording+"难度")


def 难度2():
    global width, MineNum, recording
    width = 10
    MineNum = 10
    # hideDifficulty()
    recording = "入门"
    难度等级.configure(text=recording+"难度")


def 难度3():
    global width, MineNum, recording
    width = 12
    MineNum = 20
    # hideDifficulty()
    recording = "入定"
    难度等级.configure(text=recording+"难度")


# 2.1特殊标签和按钮
输赢 = Label(win, text="".center(10))
难度等级 = Label(win, text="当前难度: ", fg="blue")
简易 = Button(win, text="简易", width=10, command=难度1)
中等 = Button(win, text="中等", width=10, command=难度2)
困难 = Button(win, text="困难", width=10, command=难度3)
开始 = []
for i in range(MaxWidth):
    开始.append(Label(win, text=" ".center(18), height=2, width=35))
# 2.2再来一次函数
again = []


def ifOneMoreTime():
    again[1].grid(row=4+RawUp, column=width+RawLf)
    again[2].grid(row=5+RawUp, column=width+RawLf)
    难度等级.configure(text="再来一次")


def yesOneMoreTime():
    global IsOver, recording, width, MineNum
    IsOver = False
    recording = "默认"
    width = 10
    MineNum = 6
    输赢.grid_forget()
    delBtnLbl()
    hideAgain()
    setLevel()
    setStart()
    delRawlbl_row_col()


def noOneMoreTime():
    again[1].grid_forget()
    again[2].grid_forget()
    难度等级.configure(text=recording+"难度")


# 2.2变量
again.append(Button(win, text="↻", fg="blue",
             width=5, command=ifOneMoreTime))  # 0
again.append(Button(win, text="确定", fg="blue",
             width=5, command=yesOneMoreTime))  # 1
again.append(Button(win, text="取消", fg="blue",
             width=5, command=noOneMoreTime))  # 2
# 2.3添位的标签
rawlbl_row = []
rawlbl_col = []
# 2.3生成rawlbl_row
for x in range(RawLf+MaxWidth):
    rawlbl_row.append(list())
    for y in range(RawUp):
        rawlbl_row[x].append(Label(win, text=" ", padx=12, pady=5))
# 2.3rawlbl_col
for x in range(RawLf):
    rawlbl_col.append(list())
    for y in range(MaxWidth):
        rawlbl_col[x].append(Label(win, text=" ", padx=12, pady=5))
# 2.4点击开发者选项


def DeveloperButton():
    AlterBtn.grid_forget()
    EnterValue.grid(row=20, column=1)
    AlterWidth.grid(row=9, column=1)
    AlterMineNum.grid(row=10, column=1)
    AlterExpress.grid(row=11, column=1)
    WidthScale.grid(row=9, column=2)
    NumScale.grid(row=10, column=2)
    v0.grid(row=11, column=2)
    v1.grid(row=11, column=3)


def EnterValueButton():
    global width, MineNum, IsExpressMine
    难度等级.configure(text="自定义关")
    width = WidthScale.get()
    MineNum = NumScale.get()
    if v.get() == 1:
        IsExpressMine = False
    else:
        IsExpressMine = True
    delDeveloperButton()
    setAlter()


def delDeveloperButton():
    EnterValue.grid_forget()
    AlterWidth.grid_forget()
    AlterMineNum.grid_forget()
    AlterExpress.grid_forget()
    WidthScale.grid_forget()
    NumScale.grid_forget()
    v0.grid_forget()
    v1.grid_forget()


# 2.4开发者选项
TheFG = "Blue"
AlterBtn = Button(win, command=DeveloperButton,
                  text="Developer Options", fg="#9C9C9C", font=("楷体", 8, "italic"))
EnterValue = Button(win, command=EnterValueButton, text="确认".center(
    8), fg="red", font=("楷体", 12, "italic"))
AlterWidth = Label(win, text="设置宽度: ", fg=TheFG, font=("楷体", 11, "italic"))
AlterMineNum = Label(win, text="设置地雷数量: ", fg=TheFG, font=("楷体", 11, "italic"))
AlterExpress = Label(win, text="地雷是否可见: ", fg=TheFG, font=("楷体", 11, "italic"))
# 进度条
WidthScale = Scale(win, fg=TheFG, font=("楷体", 11, "italic"),
                   from_=4, to=12, orient="horizontal")
NumScale = Scale(win, fg=TheFG, font=("楷体", 11, "italic"),
                 from_=2, to=25, orient="horizontal")
# 2.4单选-地雷是否可见
v = IntVar()
v.set(1)
v0 = Radiobutton(win, fg=TheFG, text="不可见", font=(
    "楷体", 11, "italic"), variable=v, value=1)
v1 = Radiobutton(win, fg=TheFG, text="可见", font=(
    "楷体", 11, "italic"), variable=v, value=2)
# 2.5关闭窗口按钮
def theQuit(): win.quit()


# 2.5变量
""" QuitBtn = Button(win,text="✕",command=theQuit,width=3,height=1,fg="blue",font=(10))
QuitBtn.place(x=550,y=5) """


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 所有函数 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
# 按钮总命令函数
def click(x, y):
    global IsOver
    opened[x][y] = 1
    btn[x][y].grid_forget()
    # 踩到地雷-game voer
    if (x, y) in mine:
        endGame()
        if IsOver == False:
            输赢.configure(text="再接再厉", bg="DeepSkyBlue", fg="black")
            输赢.grid(row=width-2+RawLf, column=width+RawUp)
            IsOver = True
    # 普通按钮-if win
    else:
        buttonClick()
        # if is winned
        if getOpenValue() == width*width-MineNum and IsOver == False:
            endGame()
            输赢.configure(text="通过成功", bg="pink", fg="red")
            输赢.grid(row=width-2+RawLf, column=width+RawUp)
            IsOver = True

# 标签数值,已打开按钮---初始化


def Init_tag_opened():
    tag.clear()
    opened.clear()
    for x in range(width):
        opened.append(list())
        tag.append(list())
        for y in range(width):
            opened[x].append(0)
            tag[x].append(0)

# 计算标签数值


def setBtnLbl():
    for x in range(width):
        for y in range(width):
            # 刷新按钮显示
            btn[x][y].configure(text="  ")  # 2个空格 才不会列间有空隙
            # 检测该格本身是地雷否
            if (x, y) in mine:
                tag[x][y] = -1
                # 打上地雷标签
                lbl[x][y].configure(text="@", fg="red", padx=9, pady=5)
            else:
                lbl[x][y].configure(padx=12, pady=5)
                # 检测该格周围8个格子 计算数值
                for i in range(3):
                    for k in range(3):
                        # 跳过该格本身
                        if i == k == 1:
                            continue
                        # 如果周围一个格子时地雷 则让标签数值+1
                        if (x-1+i, y-1+k) in mine:
                            tag[x][y] += 1
                # 带上对应数值和前景色
                if tag[x][y] == 0:
                    timeFG = "lavender"  # "lavender"
                if tag[x][y] == 1:
                    timeFG = "DodgerBlue"  # 1E90FF
                if tag[x][y] == 2:
                    timeFG = "green"
                if tag[x][y] > 2:
                    timeFG = "red"

                lbl[x][y].configure(text=str(tag[x][y]), fg=timeFG)

# 标签,按钮---初始化


def Init_lbl_btn():
    # 先隐藏所有格子
    for x in range(MaxWidth):
        for y in range(MaxWidth):
            # lbl[x][y].configure(text="1")
            lbl[x][y].grid_forget()
            btn[x][y].grid_forget()
    # 再显示出需要的格子
    for x in range(width):
        for y in range(width):
            lbl[x][y].grid(row=x+RawLf, column=y+RawUp)
            if IsButtonSet == True:
                btn[x][y].grid(row=x+RawLf, column=y+RawUp)

# 生成地雷集合


def mineMake():
    mine.clear()
    while len(mine) < MineNum:
        a = randint(0, width-1)
        b = randint(0, width-1)
        # 随机块 1,单独地雷,25%   2/3,双子地雷,50%   4,三胞地雷,25%
        IsRand = randint(1, 4)
        # 情况1不处理
        mine.add((a, b))
        # 情况2,3,4统一处理
        if 1 <= a <= width-2 and 1 <= b <= width-2:  # 只使用不处于边界的坐标
            if 2 <= IsRand <= 4:
                # 周边8个位置随机一个
                x = randint(-1, 1)
                y = randint(-1, 1)
                if x == y == 0:
                    y = x = -1  # 默认为左上角
                mine.add((a+x, b+y))
                # 情况4特殊处理
                if IsRand == 4:
                    x = randint(-1, 1)
                    y = randint(-1, 1)
                    if x == y == 0:
                        y = x = 1  # 默认为右下角
                    mine.add((a+x, b+y))
    # 删除多出的
    while len(mine) > MineNum:
        mine.pop()

# 结束游戏


def endGame():
    for x, y in mine:
        btn[x][y].grid_forget()

    # 动画效果
"""    for n in range(6):
        for x in range(width):
            for y in range(width):
                if n%2==1: btn[x][y].grid_forget()
                else:btn[x][y].grid(row=x,column=y)
"""
# 触发按钮函数-删除必要的零值按钮


def buttonClick():
    # 执行(width//2+1)次遍历
    for times in range(width//2+1):
        # 遍历所有格子
        for x in range(width):
            for y in range(width):
                # 如果lbl[x][y]是零值 并且btn[x][y]已打开
                if tag[x][y] == 0 and opened[x][y] == 1:
                    # 检测周围8格
                    for i in range(3):
                        for k in range(3):
                            # 判断(x-1+i,y-1+k)值的有效性
                            if x-1+i < width and x-1+i >= 0 and y-1+k < width and y-1+k >= 0:
                                opened[x-1+i][y-1+k] = 1
                                btn[x-1+i][y-1+k].grid_forget()

# 得到已经打开的按钮的数量


def getOpenValue():
    n = 0
    for x in range(width):
        for y in range(width):
            n += opened[x][y]
    return n

# 明示地雷位置


def mineExpress():
    for x, y in mine:
        btn[x][y].configure(text="!", fg="DeepPink", padx=9)

# 根据现有参数 铺置网格


def openStart():
    delAlter()  # 隐藏开发者选项
    hideStart()  # 隐藏[开始]按钮
    Init_lbl_btn()  # 根据宽度显示出需要的单元格
    Init_tag_opened()  # tag[] opened[]全部置零
    mineMake()  # 得到地雷的位置
    setBtnLbl()  # 根据地雷位置计算标签数值 并给标签打上相应的数值
    if IsExpressMine == True:
        mineExpress()


开始.append(Button(win, text=" 开始 ", width=10,
          command=openStart, fg="black", font=win.MyFont))

# 点击[开始]按钮


def hideStart():
    开始[-1].grid_forget()
    for i in range(MaxWidth):
        开始[i].grid_forget()
    hideDifficulty()
    难度等级.grid(row=1+RawUp, column=width+RawLf)
    setAgain()
    global recording
    if recording != "入手" and recording != "入门" and recording != "入定":
        recording = "默认"
    setRawlbl_row_col()

# 放置[开始]按钮


def setStart():
    for i in range(MaxWidth):
        开始[i].grid(row=i, column=0)
    开始[-1].grid(row=7, column=1)
    # 放置开发者选项
    setAlter()

# 隐藏等级按钮


def hideDifficulty():
    简易.grid_forget()
    中等.grid_forget()
    困难.grid_forget()

# 放置难度按钮


def setLevel():
    难度等级.configure(text=recording+"难度")
    难度等级.grid(row=2, column=1)
    简易.grid(row=3, column=1)
    中等.grid(row=4, column=1)
    困难.grid(row=5, column=1)

# 隐藏再来一次按钮


def hideAgain():
    for i in range(3):
        again[i].grid_forget()

# 放置再来一次按钮


def setAgain():
    again[0].grid(row=3+RawUp, column=width+RawLf)

# 隐藏所有普通标签和按钮


def delBtnLbl():
    for x in range(MaxWidth):
        for y in range(MaxWidth):
            lbl[x][y].grid_forget()
            btn[x][y].grid_forget()

# 放置添位的标签


def setRawlbl_row_col():
    for x in range(RawLf+MaxWidth):
        for y in range(RawUp):
            rawlbl_row[x][y].grid(row=x, column=y)
    # rawlbl_col
    for x in range(RawLf):
        for y in range(MaxWidth):
            rawlbl_col[x][y].grid(row=x, column=y)

# 隐藏添位的标签


def delRawlbl_row_col():
    for x in range(RawLf+MaxWidth):
        for y in range(RawUp):
            rawlbl_row[x][y].grid_forget()
    # rawlbl_col
    for x in range(RawLf):
        for y in range(MaxWidth):
            rawlbl_col[x][y].grid_forget()

# 放置开发者选项


def setAlter():
    AlterBtn.grid(row=20, column=1)

# 隐藏开发者选项


def delAlter():
    AlterBtn.grid_forget()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 主函数 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
def main():
    setStart()
    setLevel()
    win.mainloop()


if __name__ == '__main__':
    main()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 各版本更新内容 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<#
"""
—————————————————————————————————————————————————————————————————
2.0版本程序中所有函数名如下:
[函数描述]             [函数声明]               [函数数量]
按钮总命令函数          def click(x,y)          1
按钮分命令函数          def hit_x_y()           MaxWidth * MaxWidth
刷新tag和opened        def Init_tag_opened()   1
计算标签的数值          def setBtnLbl()         1
刷新标签和按钮          def Init_lbl_btn()      1
生成地雷集合            def mineMake()          1
游戏结束后的操作        def endGame()           1
触发按钮函数            def buttonClick()       1
打开的按钮数量          def getOpenValue()      1
明示地雷位置            def mineExpress()       1
设置后-开始游戏         def openStart()         1 

2.0版本程序中所有全局变量如下:
[作用]             [名称]               [类型]
主窗口              win                 <class 'tkinter.Tk'>
是否显示按钮        IsButtonSet         <class 'bool'>
是否明示地雷        IsExpressMine       <class 'bool'>
是否结束            IsOver              <class 'bool'>
长宽                width               <class 'int'>
最大长宽            MaxWidth            <class 'int'>
地雷数量            MineNum             <class 'int'>
输赢                输赢                <class 'tkinter.Label'>
地雷集合            mine = {}           set(tuple())
普通标签列表        lbl = []            list(list(Label()))
普通按钮列表        btn = []            list(list(Button()))
标签数值列表        tag = []            list(list(int))
已打开按钮列表      opened = []         list(list(int))
—————————————————————————————————————————————————————————————————
"""
"""
—————————————————————————————————————————————————————————————————
2.1版本程序中增加函数名如下:
[函数描述]             [函数声明]               [函数数量]
隐藏开始按钮            def hideThem()
放置难度按钮            def setLevel()          
设置等级按钮            难度1/2/3()             3
隐藏等级按钮            def hideDifficulty()

2.1版本程序中增加全局变量如下:
[作用]             [名称]               [类型]
开始按钮            开始                list(Label()+Button())
难度等级标签        难度等级             Label()
简易按钮            简易                Button()
中等按钮            中等                Button()
困难按钮            困难                Button()
—————————————————————————————————————————————————————————————————
"""
"""
—————————————————————————————————————————————————————————————————
2.2版本程序中增加函数名如下:
[函数描述]             [函数声明]               [函数数量]
放置开始按钮            def setStart()
是否重来               def ifOneMoreTime()
确认重来               def yesOneMoreTime()
取消重来               def noOneMoreTime()
隐藏再来一次按钮        def hideAgain()
放置再来一次按钮        def setAgain()
隐藏所有普通标签和按钮  def delBtnLbl()

2.2版本程序中增加全局变量如下:
[作用]             [名称]               [类型]
再来一次            again               list(Button())
—————————————————————————————————————————————————————————————————
"""
"""
—————————————————————————————————————————————————————————————————
2.3版本程序中增加函数名如下:
[函数描述]             [函数声明]               [函数数量]
放置添位的标签          def setRawlbl_row_col()
隐藏添位的标签          def delRawlbl_row_col()

2.3版本程序中增加全局变量如下:
[作用]             [名称]               [类型]
初始左距            RawLf               int
初始上距            RawUp               int
添位的标签列表-行   rawlbl_row           list(Label())
添位的标签列表-列   rawlbl_col           list(Label())
标签及按钮的背景色  NormalBG             str
开始按钮的背景色    StartBG              str
难度的背景色        DiffiBG              str
自定义字体格式      win.MyFont           font.Font()
—————————————————————————————————————————————————————————————————
"""
"""
—————————————————————————————————————————————————————————————————
2.4版本程序中增加函数名如下:
[函数描述]             [函数声明]               [函数数量]
开发者选项功能          def DeveloperButton()
确认当前值              def EnterValueButton()
隐藏开发者选项内的选项   def delDeveloperButton()
放置开发者选项          def setAlter()
隐藏开发者选项          def delAlter()

2.4版本程序中增加全局变量如下:
[作用]             [名称]               [类型]
开发者选项          AlterBtn            Button()
确认当前值          EnterValue          Button()
设置宽度            AlterWidth          Label()
设置地雷数量        AlterMineNum        Label()
地雷是否可见        AlterExpress        Label()
长宽进度条          WidthScale          Scale()
数量进度条          NumScale            Scale()
单选-地雷不可见     v0                  Radiobutton()
单选-地雷可见       v1                  Radiobutton()
—————————————————————————————————————————————————————————————————
"""
