# -*-coding = utf-8 -*-
# @Time : 2023/7/9 17:00
# @Author : 万锦
# @File : test.py
# @Softwore : PyCharm
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import  datetime
import qfluentwidgets
from 计算器 import Ui_MainWindow


################################################################
# ui, _ = loadUiType('计算器.ui')




class Mainapp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) # 构造界面
        self.handleui()
        self.handlebutton()

    def handleui(self):
        pass

    def handlebutton(self):
        pass


    def n0(self):
        return 0
    def n1(self):
        return 1
    def n2(self):
        return 2
    def n3(self):
        return 3
    def n4(self):
        return 4
    def n5(self):
        return 5
    def n6(self):
        return 6
    def n7(self):
        return 7
    def n8(self):
        return 8
    def n9(self):
        return 9




def main():
    app = QApplication([])

    window = Mainapp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()