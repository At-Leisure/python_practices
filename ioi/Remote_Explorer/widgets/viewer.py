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


# 项目根路径
root_dir = pathlib.Path(r'./ioi/Remote_Explorer')


class OSType(enum.Enum):
    """ 枚举操作系统 """
    Windows, Linux, Unix = range(3)


class DirType(enum.Enum):
    """ 目录枚举 """
    Folder, File = range(2)  # 顺序不可变


def os_type() -> OSType:
    """ 返回当前操作系统的类型 """
    os_ = platform.platform()
    if os_.startswith('Windows'):
        return OSType.Windows
    if os_.startswith('Linux'):
        return OSType.Linux
    if os_.startswith('Unix'):
        return OSType.Unix


class Viewer(QWidget):
    """ 主要视图 """

    def __init__(self, os_type: OSType = None, init_dir: str = None, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        # 动态加载ui文件
        self.current_dir_ = os.getcwd() if init_dir is None else init_dir  # 当前指向的路径
        self.ui = uic.loadUi(root_dir / 'ui/view.ui', self)  # 动态加载ui文件

        self.right_scroll_widget: QWidget
        self.right_scroll: QScrollArea
        self.lot: QVBoxLayout = self.right_scroll_widget.layout()

        self.left_tree: QTreeWidget
        self.left_tree.setHeaderHidden(True)  # 隐藏顶部标号
        self.left_tree.setIndentation(20)  # 设置上下级之间的间隔

        # 设置垂直滚动条的每次滚动步长为30
        # vertical_scrollbar = self.right_scroll.verticalScrollBar()
        # vertical_scrollbar.setSingleStep(30)

        # === TEST ===#
        self.refresh_tree_from(
            self.left_tree, self.make_tree_dict())  # 调用递归函数生成树形结构

        names = ['folder', 'file.txt', 'main.py', 'theme', 'file', 'utils']
        types = [DirType.Folder, DirType.File, DirType.File,
                 DirType.Folder, DirType.File, DirType.Folder]
        self.refresh_scroll_from(names, types)

    def refresh_tree_from(self, root, dict_: dict):
        """ 根据字符串字典刷新内容，使用有序字典可以保证排序不变 
        ## Parameter
        `root` - 此次递归的根节点
        `dict_` - 此次递归的字典"""
        for name, next_dict in dict_.items():
            next_dict: dict
            child = QTreeWidgetItem(root)
            child.setText(0, name)
            if len(next_dict):
                self.refresh_tree_from(child, next_dict)

            # 展开不空的结点
            child.setExpanded(True)

    def make_tree_dict(self) -> dict:
        """ 返回当前路径的字典树 """
        def isHidenFile(filePath):  # 判断Windows下目录是否具备隐藏属性
            if os_type() is OSType.Windows:
                import win32file
                import win32con
                fileAttr = win32file.GetFileAttributes(filePath)
                if fileAttr & win32con.FILE_ATTRIBUTE_HIDDEN:
                    return True
                return False
            return False

        """ total_dict = {}
        now_dict = total_dict
        now_dir = ''
        for step,dir_ in enumerate(self.current_dir_.replace('\\', '/').split('/')):
            if step != 0:  # 第一轮跳过
                now_dict = now_dict[dir_]  # 更新当前字典
            now_dir += (dir_ + '/')  # 更新当前的路径
            # 当前目录下所有子目录
            dir_names = [name for name in os.listdir(now_dir)]
            # 只取文件夹
            folder_names = [
                name for name in dir_names if os.path.isdir(now_dir+'/'+name)]
            # 只取非隐藏文件夹
            folder_names = [
                name for name in folder_names if not isHidenFile(now_dir+'/'+name)]
            # 在上一级字典添加子字典
            for name in folder_names:
                now_dict[name] = dict() """
        total_dict = {}
        root_dict = total_dict
        now_dict = None
        now_dir = ''
        for step, dir_ in enumerate(self.current_dir_.replace('\\', '/').split('/')):
            # 如果上一级字典不存在此键，就创建一个
            now_dir += (dir_ + '/')  # 更新当前的路径
            # 当前目录下所有子目录
            dir_names = [name for name in os.listdir(now_dir)]
            # 只取文件夹
            folder_names = [
                name for name in dir_names if os.path.isdir(now_dir+'/'+name)]
            # 只取非隐藏文件夹
            folder_names = [
                name for name in folder_names if not isHidenFile(now_dir+'/'+name)]
            # 在本级字典添加子字典
            now_dict = {name: {} for name in folder_names}
            # 在上一级字典添加本机字典
            root_dict[dir_] = now_dict
            # 更新上一级字典的指向
            root_dict = now_dict

        return total_dict

    def refresh_scroll_from(self, names: tuple[str], types: tuple[DirType]):
        """ 根据字符串元组刷新内容
        ## Parameter
        `names` - 文件名称列表
        `types` - 文件类型列表"""
        assert len(names) == len(types), '名称列表和类型列表长度需要相等'
        assert all(isinstance(type_, DirType)
                   for type_ in types), '类型列表的元素只能是DirType类型'
        # 删除先前的控件
        while self.lot.count():
            widget = self.lot.takeAt(0).widget()  # 获取第一个控件
            self.lot.removeWidget(widget)  # 从布局中移除控件
            widget.deleteLater()  # 手动释放内存

        # 获得序列
        zipped = zip(names, types)
        sorted_zip = sorted(zipped, key=lambda x: (x[1].value, x[0]))
        # 排序新来的控件
        for name, type_ in sorted_zip:
            icon = QIcon(self._select_icon(name, type_))  # 选择图标
            button = QPushButton(self.right_scroll_widget,
                                 icon=icon, text=name)
            button.setMinimumHeight(50)
            button.setMaximumHeight(50)
            button.setProperty('isfiles', True)
            self.lot.addWidget(button)
        # 在底部添加弹簧，防止控件在少量时分散
        self.lot.addItem(QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def _select_icon(self, dir_name: str, dir_type) -> str:
        """ 根据文件后缀返回对应的图标的链接， 
        **函数名前缀有下划线时应视为该类的私有方法**"""
        path = root_dir / 'svg'
        if dir_type is DirType.File:  # 文件
            suffix = dir_name.split('.')[-1]
            if suffix == 'py':
                path = path / 'file_type_python.svg'
            elif suffix == 'txt':
                path = path / 'file_type_text.svg'
            else:
                path = path / 'default_file.svg'
        else:  # 文件夹
            if dir_name == 'theme':
                path = path / 'folder_type_theme.svg'
            elif dir_name == 'utils':
                path = path / 'folder_type_tools.svg'
            else:
                path = path / 'default_folder.svg'
        return str(path)


# import subprocess
# # 执行外部命令并捕获标准输出
# command = 'dir /B /A-D'  # 替换为你要执行的命令
# result = subprocess.run(command, shell=True, capture_output=True, text=True)
# # 输出标准输出结果
# print(result.stdout)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = Viewer()
    v.show()
    sys.exit(app.exec_())
