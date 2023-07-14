# -*-coding = utf-8 -*-
# @Time : 2023/7/12 11:47

from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from test001 import Ui_MainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


class Mainapp(QMainWindow, Ui_MainWindow):

    signals = pyqtSignal()
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) # 构造界面
        self.ComboBox.addItems(["a","b","c"])
        self.ComboBox.currentIndexChanged.connect(self.test1)
        self.chart = QWebEngineView()
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.chart)


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