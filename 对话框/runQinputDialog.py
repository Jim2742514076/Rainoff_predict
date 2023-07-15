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
        self.load_txt()

    def handle_button(self):
        self.PushButton.clicked.connect(self.runQinputDialog)
        self.PushButton_2.clicked.connect(self.runQfontDialog)
        self.PushButton_3.clicked.connect(self.runQcolorDialog)
        self.PushButton_4.clicked.connect(self.runQfileDialog)
        self.PushButton_5.clicked.connect(self.runQprogressDialog)



    def load_txt(self):
        with open("test.txt","r",encoding="utf-8") as f:
            txt = f.read()
        self.TextEdit.setText(txt)

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

    def runQfontDialog(self):
        font,ok = QFontDialog.getFont()
        self.TextEdit.setCurrentFont(font)

    #一个返回值
    def runQcolorDialog(self):
        col = QColorDialog.getColor()
        self.TextEdit.setTextBackgroundColor(col)

    def runQfileDialog(self):

        #第三个参数进行文件格式进行限制
        file = QFileDialog.getOpenFileName(self,"打开文件","./",("文本(*.txt)"))
        print(file)
        file_save = QFileDialog.getSaveFileName(self,"保存文件","./",("文本(*.txt)"))
        print(file_save)

    #进度条对话框
    def runQprogressDialog(self):
        num = 100000
        progress = QProgressDialog(self)
        progress.setWindowTitle("请稍等")
        progress.setLabelText("正在操作...")
        progress.setCancelButtonText("取消")
        progress.setMinimumDuration(5)
        progress.setWindowModality(Qt.WindowModal)
        progress.setRange(0, num)
        for i in range(num):
            progress.setValue(i)
            if progress.wasCanceled():
                QMessageBox.warning(self, "提示", "操作失败")
                break
        else:
            progress.setValue(num)
            QMessageBox.information(self, "提示", "操作成功")





def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setWindowTitle("test")
    mainwindow.setWindowIcon(QIcon("../Icons/应用图标.jpg"))
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
