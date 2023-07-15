# -*-coding = utf-8 -*-
# @Time : 2023/7/15 19:12
# @Author : 万锦
# @File : runQinputDialog.py
# @Softwore : PyCharm

from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

ui,_ = loadUiType("./ui/对话框.ui")

class MainWindow(QMainWindow,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleui()
        self.handle_button()

    def handleui(self):
        pass
    def handle_button(self):
        self.PushButton.clicked.connect(self.runQinputDialog)

    def runQinputDialog(self):

        sender = self.sender()
        sex = ["男","女"]
        if sender == self.PushButton:
            #文本，返回两个参数，第一个参数为返回文本，第二个为布尔值
            text, ok = QInputDialog.getText(self, '修改姓名', '请输入姓名：')
            print(text)
            if ok:
                print(text)
            #整数
            text, ok = QInputDialog.getInt(self, '年龄', '请输入年龄：')
            #选择
            text, ok = QInputDialog.getItem(self, '性别', '请选择性别：',sex)
            #浮点数
            text, ok = QInputDialog.getDouble(self, '价格',"输入价格")


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setWindowTitle("test")
    mainwindow.setWindowIcon(QIcon("../Icons/应用图标.jpg"))
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
