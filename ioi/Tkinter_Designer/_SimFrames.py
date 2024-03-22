from tkinter import Frame,StringVar,Label,Entry,Menu
from tkinter.colorchooser import Chooser
# 仅可设定为某几个特定值的属性的字典
speatts = {
    'anchor':('n,ne,e,se,s,sw,w,nw,center'.split(',')),
    'cursor':('arrow,circle,cross,plus'.split(',')),
    'justify':('left,right,center'.split(',')),
    'relief':('flat,groove,raised,ridge,solid,sunken'.split(',')),
    'state':('normal,active,disabled'.split(',')),
    'compound':('left,right,top,bottom,center'.split(',')),
    'takefocus':(True,False),
}
""" def funcmaker(value):#根据字典的每个键的每个值产生不同的函数
    return lambda:print(type(value))
spefuns = {key:{value:funcmaker(value)  for value in values}  for key,values in speatts.items()} """
#print(spefuns)



class SimFrame(Frame):
    """ 基类1.0 : Only Label 只有标题标签和内容值"""
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self._fg = 'white'
        self.string = StringVar()
        self.label = Label(self,width=20,anchor='w')
        self.label['fg'] = self._fg
        self.label['bg'] = self.master['bg']
        self.config(*args, **kwargs)
        self['bg'] = self.master['bg']
        self.label.pack(side='left', anchor='w')



class SimFrame_txt(SimFrame):
    """ 派生类: Label & Entry """
    def __init__(self, master, *args, **kwargs):
        SimFrame.__init__(self, master, *args, **kwargs)
        self.box = Entry(self,textvariable=self.string)
        self.box['bg'] = self['bg']
        self.box['fg'] = self._fg
        self.box.pack(side='left', anchor='w')
        self.config(*args, **kwargs)




class SimFrame1(SimFrame):
    """ 基类2.0 : 增加新标签和新标签的作用函数\n
    在派生类中重写作用函数即可实现不同类执行不同功能"""
    def __init__(self, master, *args, **kwargs):
        SimFrame.__init__(self, master, *args, **kwargs)
        self.label_info = Label(self,textvariable=self.string,width=20,anchor='w')
        self.label_info['bg'] = self['bg']
        self.label_info['fg'] = self._fg
        self.label_info.pack(side='left', anchor='w')

        self.label_execute = Label(self,text=' ',bg=self['bg'],relief='groove',borderwidth=2)
        self.label_execute.bind('<Button-1>',self._execute_func)
        self.label_execute['width']=3
        self.label_execute['height']=1
        self.label_execute.pack(side='left', anchor='w',padx=5)

        self.config(*args, **kwargs)

    def _execute_func(self,event):
        """ 重写此作用函数即可实现不同功能 """
        ...




class SimFrame_colour(SimFrame1):
    """ 派生类: 颜色选择"""
    def __init__(self, master, *args, **kwargs):
        SimFrame1.__init__(self, master, *args, **kwargs)
        self.colour = 'gray'
        self.config(*args, **kwargs)

    def _execute_func(self,event):
        """ 重写的作用函数-colour """
        self.colour = ((Chooser().show())[1]).upper()
        self.string.set(self.colour)
        self.label_execute['bg'] = self.colour





class SimFrame_menu(SimFrame1):
    """ 派生类: 特值选择 """
    def __init__(self, master, *args, **kwargs):
        SimFrame1.__init__(self, master, *args, **kwargs)
        self.label_execute['text'] = '⿻'
        self.label_execute['bg'] = '#454545'
        self.menu = None
        self.config(*args, **kwargs)

    def _execute_func(self,event):
        """ 重写的作用函数-menu """
        self.menu = Menu(self, tearoff=False,fg='#0000FF')
        special_key = self.label['text'].replace(' ','')#特值属性的名称
        #根据特值属性的名称为其生成特定函数字典
        self.spefuns = {key:{value:self.funcmaker(value)  for value in values}  for key,values in speatts.items()}
        #为菜单增加命令,每个命令绑定特定的函数,每个函数作用为设置string为函数执行的值
        for value in speatts[special_key]:
            self.menu.add_command(label=str(value),command=self.spefuns[special_key][value])
        #添加分割线和不作用的Cancel命令 :)
        self.menu.add_separator()
        self.menu.add_command(label="Cancel")
        #弹出菜单
        self.menu.post(event.x_root+5, event.y_root)

    def funcmaker(self,value):
        """ 根据特值属性的不同值 设置其值 """
        return lambda:self.string.set(value)
        