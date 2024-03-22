# 0
import sys
import os
import platform
import enum
from collections import OrderedDict  # 有序字典
import pathlib  # Path类：pathlib模块中的核心类，用于表示和操作文件路径

# 1
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

# 2

from .widgets import Viewer


def main():
    app = QApplication(sys.argv)
    v = Viewer()
    v.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
