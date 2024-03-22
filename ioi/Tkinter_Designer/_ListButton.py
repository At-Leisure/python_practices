from tkinter import Button,ACTIVE

class ListButton(Button):
    """ 用于新增控件的按钮 """

    def __init__(self, master, *args, **kwargs):
        Button.__init__(self,master, *args, **kwargs)
        self.PowerWidgetType = None
        def _enter(event):
            self['font'] = ('宋体',14,'bold')
            self['fg'] = 'deepskyblue'
        def _leave(event):
            self['font'] = ('宋体',14)
            self['fg'] = 'skyblue'

        self.bind('<Enter>', _enter)
        self.bind('<Leave>', _leave)
        self.config(relief='flat', bg=self.master['bg'], activebackground=self.master['bg'],
            fg='skyblue',font=('宋体',14),width=15,activeforeground='deepskyblue',command=self._send_create_request
        )

        self.config(*args, **kwargs)

    def _send_create_request(self):
        if self.PowerWidgetType:
            pause = self.PowerWidgetType(self.master)
            print('\nPowerTk.WgtsFrame尝试发送'+pause._atts_new['type']+'创建请求')
            try:self.master.master.manager._receive_create_request(self.PowerWidgetType)
            except:print('<Wrong> PowerTk.WgtsFrame尝试发送'+pause._atts_new['type']+'创建请求出错')
            finally:pause.destroy()





if __name__ == '__main__':
    win = __import__('tkinter').Tk()
    win.geometry('500x500')
    ListButton(win,text='test',bg='skyblue').pack()
    Button(win,text=123,bg='skyblue',relief='g',borderwidth=1.1).pack()
    win.mainloop()