from threading import Thread
from tkinter import Tk,Menu,Frame,Label
from time import sleep

#pyparsing import delimited_list
from ._PowerFrame import PowerFrame_ATTS,PowerFrame_WGTS,PowerFrame_SCRN






class PowerTk(Tk):
    """Tk类的派生类,PowerTk类的Manager类变量用于管理当前控件和联系三个框架\n
    放置控件时, 控件的master应该是以下三个之一, 否则此派生类没有被使用的必要\n
    方位 → 名称 → 类型 → 用处\n
    left → WidgtsFrame → Frame → 控件的框架\n
    middle → ScrnFrame → Frame → 视窗的框架\n
    right → AttibuteFrame → PowerFrame_ATTS → 属性的框架 """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #1.改标题+改尺寸
        #3.生成改观线程
        self.colors = {'WgtsFrame': '#1f2428', 'ScrnFrame': '#24292e'}
        self.title('PowerTk')
        self.geometry('400x300')
        self['bg'] = self.colors['ScrnFrame']
        #2.生成manager和3个框架
        self.rate = {'WgtsFrame': 0.15, 'ScrnFrame': 0.65}#框架长度比例 AttsFrame的长度 = 1-WgtsFrame-ScrnFrame
        self.manager = Manager(self)
        self.WgtsFrame = PowerFrame_WGTS(self, bg = self.colors['WgtsFrame'])
        self.MidFrame = Frame(self, bg = self.colors['ScrnFrame'])
        self.ScrnFrame = PowerFrame_SCRN(self, bg = self.colors['ScrnFrame'])
        self.AttsFrame = PowerFrame_ATTS(self, bg = self.colors['WgtsFrame'])
        Label(self.MidFrame, text = 'ScreenFrame', bg = self.colors['ScrnFrame'], fg = 'gray').pack()
        #放置框架们
        self._framesPlaceReset__()

        #self._frames_can_changed 如果为True,
        #则未命名线程可以创建并启动,从而框架们可以随主窗口大小进行适应性变化
        self._frames_can_changed = True
        if self._frames_can_changed:
            self._target_frequency = 10 #改观的频率 default=10
            self.thread = Thread(target = self._PlaceReset_run__, daemon = True)
            self.thread.start()

        #关闭线程循环,从而使线程自行结束
        def _thread_quit(): self._frames_can_changed = False
        #重定义窗口的关闭事件,使得窗口的关闭紧接着线程的结束并 [在其之后]
        self.protocol('WM_DELETE_WINDOW',_thread_quit)

    def _framesPlaceReset__(self):
        """ 使框架们可以随主窗口大小进行适应性变化 """
        self.update()
        #根据设定的长度比例来调整各个框架的长度
        len = [
            int(self.winfo_width() * self.rate['WgtsFrame']),
            int(self.winfo_width() * self.rate['ScrnFrame']),
        ]
        len.append(self.winfo_width() - len[0] - len[1])
        #框架的高度就是窗体的盖度
        hei = self.winfo_height()
        self.WgtsFrame.place(x = 0, y = 0, width = len[0], height = hei)
        self.MidFrame.place(x = len[0], y = 0, width = len[1], height= hei)
        self.ScrnFrame._update_size()
        self.AttsFrame.place(x = len[0] + len[1], y = 0, width = len[2], height = hei)
        self.AttsFrame._AB_button_update(len[2], hei)

    def _PlaceReset_run__(self):
        """ 线程执行的函数 """
        while self._frames_can_changed:
            sleep(1/self._target_frequency)
            self._framesPlaceReset__()
        #关闭线程后再退出窗体循环,避免产生窗体结束后继续更新窗体的错误
        print('\nPowerTk.thread was ended and PowerTk was destroyed ✓ ✓ ✓')
        #销毁此小部件和所有后代小部件.这将结束此Tcl解释器的应用.
        self.destroy()
        #退出 Tcl 解释器.所有小部件将被销毁
        #self.quit()









class Manager(object):
    """ 作为PowerTk类的Manager类变量,用于管理当前控件和联系三个框架\n
    transferBaton(...) 函数用于传递被点击后伪聚焦的 PowerWidget 控件"""

    def __init__(self, master: 'PowerTk'):
        self.master = master
        self.pendant = None
        self.funcid = None #绑定menu时返回的str,解绑时需要用到
        self.list = []
        self._creat_pendant_menu()
        
    def _creat_pendant_menu(self):
        self.menu = Menu(self.master, tearoff=False)
        self.menu.add_command(label='Move',command=self._cmd_move)
        self.menu.add_command(label='Stand',command=self._cmd_stand)
        self.menu.add_command(label='Delete',command=self._cmd_delete)
        self.menu.add_separator()
        self.menu.add_command(label='More...',command=self._cmd_more)

    def _cmd_move(self):...
    def _cmd_stand(self):...
    def _cmd_delete(self):
        self.pendant.destroy()
        del_index = 0
        del_penat = None
        for del_index in range(self.list.__len__()):
            if str(self.list[del_index]) == self.pendant._atts_new['id']:break
        del_penat = self.list[del_index]
        self.list.pop(del_index)
        del del_penat
        try:
            print(id(del_penat))
        except:
            print('place_forget ✓')
            print('last:',self.list .__len__())
            self.master.AttsFrame._delete_pendant()
    def _cmd_more(self):...
        
    def _eject_menu(self,event):self.menu.post(event.x_root, event.y_root)

    def _bind_new_(self):
        """ 为新的控件绑定 放置+改观 事件 """
        try:
            self.funcid = self.pendant.bind('<Button-3>',self._eject_menu)
            print('bind new successed ✓')
        except:
            print('bind new failed ✕')


    def _forget_old_(self):
        """ 使旧的控件忘记 放置+改观 事件 """
        if self.pendant:
            try:
                self.pendant.unbind('<Button-3>', funcid = self.funcid)
                print('forget old successed ✓')
            except:
                print('forget old failed ✕')



    def _receive_create_request(self, PendantType):
        pause = PendantType(self.master)
        print('PowerTk.manager成功收到'+pause._atts_new['type']+'创建请求 ✓')
        pause.destroy()
        self.list.append(PendantType(self.master.ScrnFrame,text='New '+PendantType.self_type_name,bg='#008080',fg='white'))
        self._update(self.list[-1])
        self.pendant.pack(anchor='center')
        self._put_ctrl_request(self.pendant,None)

    def _get_ctrl_request(self,pendant,event):
        """ 中转'接力棒' PowerWidget → PowerTk.manager → PowerTk.AttsFrame"""
        print('{PowerTk.maneger} received message from {'+str(pendant)+'} sccessed ✓')
        self._put_ctrl_request(pendant,event)

    def _put_ctrl_request(self,pendant,event):
        """ 中转'接力棒' PowerWidget → PowerTk.manager → PowerTk.AttsFrame"""
        print('{PowerTk.manager} has sent information .')
        try: self.master.AttsFrame._receive_ctrl_request(pendant,event)
        except:
            print('<Wrong> {PowerTk.manager} sent message failed ✕')
            #如果信息传递失败则拒绝更新当前pendant
            return
            
        # >>> 下一步处理不好会升起错误 <<<
        self._update(pendant)

    def _update(self,newpendant):
        self._forget_old_()
        self.pendant = newpendant
        self._bind_new_()