# -*-coding = utf-8 -*-
# @Time : 2023/7/10 11:20
# @Author : 万锦
# @File : tmp.py
# @Softwore : PyCharm


# a = "1+3+4"
# b = eval(a)
#
# c = a.join(("+"))
# d = c.join((str(b)))
#
# e = eval(d)
#
# print(a,b)
# print(c)

#
# import pandas as pd
#
# df = pd.read_excel("E:/pyqt/Rainoff_predict/data/test.xlsx")
# print(df)
# print(df.columns.values)
# print(len(df))
# print(df.values)
# import numpy as np
#
# a= 10
# b =20
#
# print(np.mean([a,b]))
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
#
#
# class QmyWidget(QWidget):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)  # 调用父类的构造函数，创建QWidget窗体
#         self.setupUi()
#
#     def setupUi(self):
#         """页面初始化"""
#         # 设置窗体大小及标题
#         self.resize(500, 400)
#         self.setWindowTitle("QComboBox组件示例")
#         # 创建布局
#         self.layout = QVBoxLayout()
#
#         # QComboBox组件定义
#         self.combo = QComboBox(self)
#         # QComboBox组件设置
#         self.itmes = ["one", "two", "three", "four"]
#         self.combo.addItem("zero")   # 设置单个项目
#         self.combo.addItems(self.itmes)   # 设置多个项目
#         # QComboBox关联信号
#         self.combo.activated.connect(self.on_combo_activated)
#
#         # 将组件添加到布局中
#         self.layout.addWidget(self.combo)
#         # 为窗体添加布局
#         self.setLayout(self.layout)
#
#     def on_combo_activated(self, index):
#         """combo组件槽函数"""
#         print("combo下拉列表被切换啦:{}！".format(index))
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myMain = QmyWidget()
#     myMain.show()
#     sys.exit(app.exec_())


# import json
# with open("./data/citycode.json","r",encoding="utf-8") as f:
#     data = json.load(f)
# data_dict = {}
# for item in data:
#     data_dict[item["city_name"]] = item["city_code"]
# with open("./data/city.csv", "w",encoding="utf8") as f:
#     json.dump(data_dict, f)
# # print(data_dict)

# import requests
#
# cityCode = "101161101"
# json_data = requests.get("http://t.weather.sojson.com/api/weather/city/{}".format(cityCode))
#
# print(json_data.json()["data"]["forecast"][0])
# for row,items in enumerate(json_data.json()["data"]["forecast"]):
#     print(row,items["ymd"],type(items["ymd"]))
#     print(row,items["high"],type(items["high"]))
#     print(row,items["low"],type(items["low"]))
#     print(row,items["fx"],type(items["fx"]))
#     print(row,items["fl"],type(items["fl"]))
#     print(row,items["type"],type(items["type"]))

# teststr = "低温 15℃"
# import re
#
# print(re.findall("低温.(\d+).",teststr))
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget,QPushButton
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # 创建QWebEngineView组件
#         self.web_view = QWebEngineView()
#         self.setCentralWidget(self.web_view)
#
#         # 加载ECharts图表的HTML文件
#         html_file = "file:///"+"html/radar.html"
#         self.web_view.load(QUrl(html_file))
#
#
#         # 添加一个按钮并连接交互函数
#         self.widget = QWidget()
#         self.layout = QVBoxLayout(self.widget)
#         self.button = QPushButton('Update Chart')
#         # self.button.clicked.connect(on_button_click)
#         self.layout.addWidget(self.web_view)
#         self.layout.addWidget(self.button)
#         self.setCentralWidget(self.widget)
#
# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()
import sys
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECharts with PyQt")
        self.setGeometry(100, 100, 800, 600)

        # 创建控件
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["X", "Y"])
        self.table_widget.setRowCount(5)

        self.button = QPushButton("Plot", self)
        self.button.clicked.connect(self.plot_chart)

        self.web_view = QWebEngineView(self)
        self.web_view.load(QUrl.fromLocalFile("chart.html"))  # 加载ECharts的HTML文件

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.button)
        layout.addWidget(self.web_view)

        # 创建主部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 创建JavaScript桥接
        self.js_bridge = JavaScriptBridge(self)
        self.js_bridge.dataUpdated.connect(self.update_table_data)

        # 在Web视图中注册桥接对象
        web_channel = QWebChannel(self)
        web_channel.registerObject("bridge", self.js_bridge)
        self.web_view.page().setWebChannel(web_channel)

    def plot_chart(self):
        # 获取表格数据
        data = []
        for row in range(self.table_widget.rowCount()):
            x_item = self.table_widget.item(row, 0)
            y_item = self.table_widget.item(row, 1)
            if x_item is not None and y_item is not None:
                x = float(x_item.text())
                y = float(y_item.text())
                data.append([x, y])

        # 将数据传递给JavaScript
        self.js_bridge.set_chart_data(data)

    @pyqtSlot(str)
    def update_table_data(self, data_str):
        # 更新表格数据
        data = eval(data_str)  # 将字符串转换为列表
        self.table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            x_item = QTableWidgetItem(str(item[0]))
            y_item = QTableWidgetItem(str(item[1]))
            self.table_widget.setItem(row, 0, x_item)
            self.table_widget.setItem(row, 1, y_item)


class JavaScriptBridge(QObject):
    dataUpdated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart_data = []

    @pyqtSlot(result=str)
    def get_chart_data(self):
        return str(self.chart_data)

    @pyqtSlot(str)
    def set_chart_data(self, data_str):
        self.chart_data = eval(data_str)  # 将字符串转换为列表
        self.dataUpdated.emit(str(data_str))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
