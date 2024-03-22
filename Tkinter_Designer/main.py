from ._all_tkinter_tools import *


def main():

    win = PowerTk()
    win.geometry('1000x700+400+100')
    win['bg'] = win.colors['WgtsFrame']
    win.mainloop()
