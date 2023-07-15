# -*-coding = utf-8 -*-
# @Time : 2023/7/12 11:47

from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from test001 import Ui_MainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import codecs

ui,_ = loadUiType("test001.ui")
class Mainapp(QMainWindow, ui):

    signals = pyqtSignal()
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) # 构造界面
        self.ComboBox.addItems(["a","b","c"])
        self.ComboBox.currentIndexChanged.connect(self.test1)
        self.add_echarts()
        self.button_connect()

    def button_connect(self):
        self.pushButton.clicked.connect(self.showPi)

    def add_echarts(self):
        self.chart = QWebEngineView()
        self.chart.load(QUrl("file:///"+"html/chart.html"))
        self.verticalLayout.addWidget(self.chart)

    def showPi(self):
        """
        显示饼形图
        """
        food = 500
        rent = 500
        electricity = 500
        traffic = 500
        relationship = 500
        taobao = 500
        # 将微调框的数值赋值给变量
        jscode = "showPiChart({}, {}, {}, {}, {}, {});".format(food, traffic, relationship, rent, electricity, taobao)
        self.chart.page().runJavaScript(jscode)
        # 加载运行JavaScript



    def test1(self):
        self.LineEdit.setText(self.ComboBox.text())


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icons/应用图标.ico"))
    window = Mainapp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()