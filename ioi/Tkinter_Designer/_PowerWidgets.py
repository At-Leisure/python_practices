from tkinter import Label,Button,Canvas,Menu, Widget
from abc import ABC


class PowerWidget(ABC):
    """ 控件基类,用于控件的认证 """ 

    self_type_name = 'PowerWidget'

    def __init__(self):
        self._atts_new = None#新增属性
        self._atts_txt = None#文本属性
        self._atts_spe = None#特值属性
        self._atts_colour = None#色值属性
        self._atts_tuple = None#元组属性
        self._set_atts()#初始化属性字典
        self._reset_atts()#自定义初始化字典-派生类需重定义此函数
        self._items_bind()#绑定事件

    def _items_bind(self):
        """ 事件绑定集合 """
        #绑定鼠标左键抬起事件为发出信息
        self.bind('<ButtonRelease-1>',self._send_ctrl_request)

    def _send_ctrl_request(self,event):
        """ 发出'接力棒' PowerWidget → PowerTk.manager → PowerTk.AttsFrame"""
        #更新信息后尝试向PowerTk.manager发送信息,若成功则在'路途'中产生消息
        self._atts_update()
        try:
            print('\n{'+self._atts_new['id']+'}', 'has sent a message .')
            #向PowerTk.manager发送信息
            self.master.master.manager._get_ctrl_request(self,event)
        except:
            #发送信息错误后的提示
            print('<Wrong> {'+self._atts_new['id']+'} sent message failed ✕')

    def _atts_update(self):
        """ 根据控件最新的状态更新 文本属性&特值属性&色值属性&元组属性\n
        更新信息不包括 新增属性"""
        for atts in (self._atts_tuple,self._atts_colour,self._atts_txt,self._atts_spe):
            for key in atts:
                atts[key] = self[key]

    def _set_atts(self):
        #id == str(event.widget) 控件的身份证号#name 属性的自定义名称
        self._atts_new = {'id': str(self),'type': '按钮 Button','name': str(self).split('!')[-1],}
        self._atts_tuple = {'font': ('default','default','default')}
        key_effect = ' '.join(['background highlightbackground']).split()
        self._atts_colour = {attibute: self[attibute] for attibute in key_effect}
        key_effect = ' '.join(['width height padx pady']).split()
        self._atts_txt = {attibute: self[attibute] for attibute in key_effect}
        key_effect = 'cursor relief'.split()
        self._atts_spe = {attibute: self[attibute] for attibute in key_effect}

    def _reset_atts(self): ...





class PowerLabel(PowerWidget, Label):
    """ 明确属性 & 绑定事件 \n
    左键选定 & 右键进行设置"""

    self_type_name = 'PowerLabel'

    def __init__(self, master, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        PowerWidget.__init__(self)
        self.config(text='Power Label',fg='white')
        self.config(*args, **kwargs)
    
    def _reset_atts(self):
        self._atts_new = {#id == str(event.widget) 控件的身份证号#name 属性的自定义名称
            'id': str(self),
            'type': '标签 Label ',
            'name': str(self).split('!')[-1],
        }
        self._atts_tuple = {
            'font': ('default','default','default')
        }
        key_effect = ' '.join(['background foreground activebackground activeforeground disabledforeground',
            'highlightbackground highlightcolor']
        ).split()
        self._atts_colour = {attibute: self[attibute] for attibute in key_effect}
        key_effect = ' '.join(['text width height padx pady borderwidth wraplength border bd',
            'highlightthickness underline image bitmap textvariable']
        ).split()
        self._atts_txt = {attibute: self[attibute] for attibute in key_effect}
        key_effect = 'anchor cursor compound justify relief state takefocus'.split()
        self._atts_spe = {attibute: self[attibute] for attibute in key_effect}







class PowerButton(PowerWidget, Button):
    """ 明确属性 & 绑定事件 \n
    左键选定 & 右键进行设置"""
        
    self_type_name = 'PowerButton'

    def __init__(self, master, *args, **kwargs):
        Button.__init__(self, master, *args, **kwargs)
        PowerWidget.__init__(self)
        self.config(text='Power Button',fg='white')
        self.config(*args, **kwargs)

    def _reset_atts(self):
        ...


