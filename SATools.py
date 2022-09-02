from tkinter.messagebox import YES
from turtle import title
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog

from git.repo import Repo

import os,shutil



rootD = "E:\git\smic"
wsid = "QDF1616"


p = os.path.join(rootD,wsid)
eqp = os.path.join(rootD,wsid,"TDGOX03")

repo = Repo(p)

files = []

class mainText(QTextEdit):
    def __init__(self,parent=None):
        super(mainText,self).__init__(parent)
        self.setAcceptDrops(True)

    def dropEvent(self, e):
        filePathList = e.mimeData().text()
        filePaths = filePathList.split('\n') #拖拽多文件只取第一个地址
        for f in filePaths:
            filePath = f.replace('file:///', '', 1) #去除文件地址前缀的特定字符
            if os.path.isfile(filePath):
                self.append(filePath)
                shutil.copy2(filePath,eqp)
            # self.appendPlainText(filePath)


class mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        

        self.btn = QPushButton(self)
        self.btn.setText("保存")
        self.btn.move(10, 80)
        self.btn.clicked.connect(self.openfiles)
        

        # btn1 = QPushButton(window)
        # btn1.setText("状态")
        # btn1.move(105, 80)
        # btn1.clicked.connect(ststfiles)

        self.btn2 = QPushButton(self)
        self.btn2.setText("上传")
        self.btn2.move(200, 80)
        self.btn2.clicked.connect(self.Upload)

        self.btn3 = QPushButton(self)
        self.btn3.setText("回退")
        self.btn3.move(105, 80)
        self.btn3.clicked.connect(self.Goback)

        self.text = mainText(self)
        self.text.move(10, 200)

        # # 实例化一个 Ui_MainWindow对象
        # self.ui=Ui_MainWindow()
       	# # setupUi函数
       	# # 这个函数很多地方说是初始化ui对象，我觉得直接翻译为“设置UI”
       	# # 这样表明ui对象的实例化和设置（或者说加载）是完全不相干的两步
        # self.ui.setupUi(self)
        # # 这里使用的是 self.show(),和之后的区分一下

        # self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.ui.treeWidget.customContextMenuRequested.connect(self.create_rightmenu)  # 连接到菜单显示函数

        # self.show()

    def openfiles(self):
        files = []
        filepaths, filetype = QFileDialog.getOpenFileNames(
            window,
            "保存",
            r"E:\eap",
            "(*.exe;*.ini;*.xml)"
        )
        for file in filepaths:
            files.append(file)
            self.text.appendPlainText(file)

    def ststfiles(self):    
        df = repo.index.diff(repo.head.commit)

        repo.head.log
        
        for diff_added in df.iter_change_type('M'):
            print(diff_added)
            # text.appendPlainText(diff_added)

    def Goback(self):
        repo.head.reset(working_tree=True)
        repo.git.clean(f="--force")
        # repo.index.reset(working_tree=True)

    def Upload(self):
        self.upload = AnotherWindow()
        self.upload.show()

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("请输入commit信息")
        layout = QVBoxLayout()
        # layout2= QHBoxLayout()
        # qw = QWidget()
        # qw.setLayout(layout2)
        self.label = QLabel("Another Window")
        self.text = QTextEdit()
        self.btn1 = QPushButton("确认")
        self.btn2 = QPushButton("取消")
        self.btn1.clicked.connect(self.commit)
        self.btn2.clicked.connect(self.cancel)
        # layout.addWidget(self.label)

        layout.addWidget(self.text)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        self.setLayout(layout)

    def commit(self):
        if repo.is_dirty():
            t = self.text.toPlainText()
            repo.git.add(".")
            repo.index.commit(message=t)
            repo.git.push()
            reply = QMessageBox.information(self, '','更新成功',QMessageBox.Yes,QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.close()


    def cancel(self):
        self.text.clear()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = mainwindow()
    window.resize(300, 500)
    window.move(300, 300)

    window.show()
    app.exec_()