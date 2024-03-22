from tkinter import Frame,Label,Button
from ._SimFrames import SimFrame_colour,SimFrame_txt,SimFrame_menu
from ._ListButton import ListButton
from ._PowerWidgets import PowerWidget,PowerLabel,PowerButton

class PowerFrame_ATTS(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self._pendant = None#可控制的控件
        self._atts_new = None#挂件的新增属性
        self._atts_txt = None#挂件的文本属性
        self._atts_spe = None#挂件的特值属性
        self._atts_colour = None#挂件的色值属性
        self._atts_tuple = None#挂件的元组属性
        self._separates = {#各类属性的标题提示的分隔标签
            'unique': Label(self,text='unique information',bg=self['bg'],fg='gray'),
            'colour': Label(self,text='colour information',bg=self['bg'],fg='gray'),
            'txt': Label(self,text='text information',bg=self['bg'],fg='gray'),
            'spe': Label(self,text='special information',bg=self['bg'],fg='gray'),
            'tuple': Label(self,text='tuple information',bg=self['bg'],fg='gray'),
        }
        #AttsFrame的顶部标题在其内部实现放置
        self.title = Label(self, text='AttributesFrame', bg = self.master.colors['WgtsFrame'], fg = 'gray')
        #右下角的[Apply]&[Back]按钮
        self._apply_button = Button(self, text='Apply', bg=self['bg'], activebackground=self['bg'],
            fg='skyblue', underline=0, command=self._apply)
        self._back_button = Button(self, text='Back', bg=self['bg'], activebackground=self['bg'],
            fg='skyblue', underline=0, command=self._back)

        self.title.pack()

        self.config(*args, **kwargs)

    def _receive_ctrl_request(self, pendant, event) -> None:
        """ 接收'接力棒' PowerWidget → PowerTk.manager → PowerTk.AttsFrame
        接受发送信息的挂件本身和触发发送信息事件的事件, AttsFrame成功接收信息后会产生输出成功的消息\n
        pendant->PowerWidget发送信息的挂件本身\n
        event->触发发送信息事件的事件"""
        print('{PowerTk.AttsFrame} recrived message from {'+str(pendant)+'} successed ✓')
        
        self._forget_oldatts(self._pendant)#处理旧挂件的属性的放置
        self._place_newatts(pendant)#进行新挂件的属性的放置
        self._pendant = pendant#处理旧挂件后再更新当前可控挂件
        self._back()#复位一下显示的各种属性

    def _forget_oldatts(self,pendant):
        """ 处理旧挂件的属性的放置 """
        if pendant:
            for singal in (self._separates, self._atts_new, self._atts_colour, self._atts_txt, self._atts_tuple, self._atts_spe):
                for key,frame in singal.items():
                    frame.pack_forget()

    def _delete_pendant(self):
        self._forget_oldatts(self._pendant)
        self._pendant = None

    def _place_newatts(self,pendant):
        """ 进行新挂件的属性的放置 & 更新为新挂件的可控属性 """
        #(放置属性标题标签-放置各个属性标签)*n
        if pendant:
            self._separates['unique'].pack(side='top',anchor='nw')
            self._atts_new = {key: SimFrame_txt(self) for key in pendant._atts_new}
            for key,frame in self._atts_new.items():
                frame.label['text'] = key.center(30)
                frame.string.set(pendant._atts_new[key])
                frame.pack(side='top',anchor='nw')

            self._separates['colour'].pack(side='top',anchor='nw')
            self._atts_colour = {key: SimFrame_colour(self) for key in pendant._atts_colour}
            for key,frame in self._atts_colour.items():
                frame.label['text'] = key.center(30)
                frame.string.set(pendant._atts_colour[key])
                frame.pack(side='top',anchor='nw')

            self._separates['txt'].pack(side='top',anchor='nw')
            self._atts_txt = {key: SimFrame_txt(self) for key in pendant._atts_txt}
            for key,frame in self._atts_txt.items():
                frame.label['text'] = key.center(30)
                frame.string.set(pendant._atts_txt[key])
                frame.pack(side='top',anchor='nw')

            self._separates['spe'].pack(side='top',anchor='nw')
            self._atts_spe = {key: SimFrame_menu(self) for key in pendant._atts_spe}
            for key,frame in self._atts_spe.items():
                frame.label['text'] = key.center(30)
                frame.string.set(pendant._atts_spe[key])
                frame.pack(side='top',anchor='nw')

            self._separates['tuple'].pack(side='top',anchor='nw')
            self._atts_tuple = {key: SimFrame_txt(self) for key in pendant._atts_tuple}
            for key,frame in self._atts_tuple.items():
                frame.label['text'] = key.center(30)
                frame.string.set(pendant._atts_tuple[key])
                frame.pack(side='top',anchor='nw')

    def _apply(self):
        """ 应用做出的修改 """
        if self._pendant:
            for key,frame in self._atts_new.items():
                # id,type 不允许修改
                if key == 'id' or key == 'type': continue
                self._pendant._atts_new[key] = frame.string.get()
            for key,frame in self._atts_txt.items():
                if frame.string.get() != '':
                    self._pendant[key] = frame.string.get()
            for key,frame in self._atts_colour.items():
                #只进行十六进制色值的修改
                if frame.string.get().startswith('#'):
                    self._pendant[key] = frame.string.get()
            for key,frame in self._atts_spe.items():
                self._pendant[key] = frame.string.get()
            self._pendant._atts_update()
        #应用修改后再重置下,观察有无错误
        self._back()

    def _back(self):
        """ 复位显示的各种挂件属性 """
        if self._pendant:
            for key,frame in self._atts_new.items():
                frame.string.set(self._pendant._atts_new[key])
            for key,frame in self._atts_txt.items():
                frame.string.set(self._pendant[key])
            for key,frame in self._atts_colour.items():
                frame.string.set(self._pendant[key])
                frame.colour = self._pendant[key]
                frame.label_execute['bg'] = frame.colour
            for key,frame in self._atts_spe.items():
                frame.string.set(self._pendant[key])
            for key,frame in self._atts_tuple.items():
                frame.string.set(self._pendant[key])

    def _AB_button_update(self,self_wid,self_hei):
        """ 更新 apply back 的位置 """
        wid_A,wid_B = 50,45
        hei_AB,pad = 30,10
        A_x,A_y = self_wid-wid_A-wid_B-pad*2, self_hei-hei_AB-pad
        B_x,B_y = A_x+wid_A+pad, A_y

        self._apply_button.place(x=A_x,y=A_y,width=wid_A,height=hei_AB,)
        self._back_button.place(x=B_x,y=B_y,width=wid_B,height=hei_AB)





class PowerFrame_WGTS(Frame):
    """ 罗列出可用的控件 """
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self,master, *args, **kwargs)
        Label(self, text = 'WidgetsFrame', bg = self.master.colors['WgtsFrame'], fg = 'gray').pack()

        self._add_PowerWidget(PowerLabel)
        self._add_PowerWidget(PowerButton)
        #self._add_PowerWidget(PowerCanvas)
        #self._add_PowerWidget(PowerMenu)
        self.config(*args, **kwargs)

    def _add_PowerWidget(self, PendantType: PowerWidget = None):
        """ 添加控件 """
        lsbt = ListButton(self, text = PendantType(self)._atts_new['type'])
        lsbt.PowerWidgetType = PendantType
        lsbt.pack()





class PowerFrame_SCRN(Frame):
    """ 可根据自身的宽高和主窗体的宽高等比例缩放 """
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.config(relief='so',borderwidth=1)
        self._wid_rate = 16
        """ 宽高比-宽 """
        self._hei_rate = 9
        """ 宽高比-高 """
        self._wid,self._hei = 0,0
        self._placeX,self._placeY = 0,0


        self.config(*args, **kwargs)

    def _update_size(self):
        """ 根据自身的宽高和主窗体的宽高等比例缩放的作用函数 """
        self.master.update()
        self._wid = int(self.master.winfo_width()*self.master.rate['ScrnFrame'])
        self._hei = int(self._wid/self._wid_rate*self._hei_rate)
        self._placeX = int(self.master.winfo_width() * self.master.rate['WgtsFrame'])
        self._placeY = int((self.master.winfo_height()-self._hei)/2)
        self.place(x=self._placeX,y=self._placeY,width=self._wid,height=self._hei)


def gcd(m: int, n: int) -> int:
    if m<n: m,n = n,m
    while m%n:
        r=m%n
        m=n
        n=r
    return n

def simplify_rate(width, height):
    """ 约分比例 """
    return width%gcd(width, height), height%gcd(width, height)

