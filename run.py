# -*-coding = utf-8 -*-
# @Time : 2023/7/10 16:23
# @Author : 万锦
# @File : run.py
# @Softwore : PyCharm

from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import numpy as np
import  datetime
import qfluentwidgets
import  pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import requests
import random
import json
from requests import request
import re
import dialog_pyqt
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import time

ui, _ = loadUiType('test_pyqt5.ui')
ui_dialog,_ = loadUiType('dialog_pyqt.ui')

class Dlg_Widget(QDialog,ui_dialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)  # 构造界面



        self.handlebutton()


    def handleui(self):
        pass

    def handlebutton(self):
        self.PushButton.clicked.connect(self.avg)


    def avg(self):

        yuwen = float(self.LineEdit.text())
        shuxue = float(self.LineEdit_2.text())
        yinyu  = float(self.LineEdit_3.text())
        avg_subject = np.mean([yuwen, shuxue,yinyu])
        self.LineEdit_4.setText(str(avg_subject))





class Mainapp(QMainWindow, ui):

    signals = pyqtSignal()
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) # 构造界面
        self.city_dict = {"北京":"101010100","上海":"101020100","长沙":"101250101","南京":"101190101"}
        self.TableWidget_weather.setHorizontalHeaderLabels(["日期", "最高气温", "最低气温", "风向", "风力", "天气"])
        self.handleui()
        self.handlebutton()
        self.communication()
        self.dgl = Dlg_Widget()
        self.slider_set()


    def slider_set(self):
        self.Slider_2.setMaximum(100)
        self.Slider_2.setMinimum(0)
        self.Slider_2.setSingleStep(2)

    def communication(self):
        pass



    def handleui(self):
        self.label_3.setText("<a href='https://www.baidu.com'>百度一下</a>")
        self.LineEdit_7.setPlaceholderText("Normal回显模式")
        intvalidator = QIntValidator()
        intvalidator.setRange(0,9)
        self.LineEdit_11.setValidator(intvalidator)
        doublevalidator = QDoubleValidator()
        doublevalidator.setRange(0,9)
        doublevalidator.setDecimals(2)
        self.LineEdit_12.setValidator(doublevalidator)

        reg = QRegExp('[a-zA-Z0-9]+$')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.LineEdit_13.setValidator(validator)

        self.figure = plt.figure()
        # self.chart = QChart()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas)

        # self.verticalLayout_2.addWidget(self.toolbar)
        self.verticalLayout_2.addWidget(self.canvas)


        self.ComboBox_2.addItems(["北京","上海","长沙","南京"])
        self.ComboBox_2.setCurrentIndex(1)
        self.pre_weather()
        self.load_echarts()






    def handlebutton(self):
        self.label_3.linkHovered.connect(self.lable_linkHovered)
        self.label_3.linkActivated.connect(self.display_test)
        self.PushButton_3.clicked.connect(self.display_test)
        self.PushButton_4.clicked.connect(self.open_file)
        self.PushButton_5.clicked.connect(self.open_file)
        self.PushButton_6.clicked.connect(self.select_row)
        self.PushButton_8.clicked.connect(lambda: self.PushButton_7.setEnabled(False))
        self.PushButton_9.clicked.connect(lambda :self.PushButton_7.setEnabled(True))
        self.RadioButton.clicked.connect(self.first_radio)
        self.PushButton_10.clicked.connect(self.plot)
        self.PushButton_11.clicked.connect(lambda:self.dgl.show())
        self.PushButton_11.clicked.connect(self.test2)
        self.Slider_2.valueChanged.connect(self.slider_show)
        self.PushButton_26.clicked.connect(self.add_row)
        self.PushButton_40.clicked.connect(self.del_row)
        self.PushButton_41.clicked.connect(self.save_form)
        self.PushButton_14.clicked.connect(lambda: self.tabWidget.setCurrentIndex(6))
        self.ComboBox_2.currentTextChanged.connect(self.pre_weather)
        self.ComboBox_2.currentTextChanged.connect(self.changeWeather)
        self.PushButton_15.clicked.connect(self.add_city)
        self.PushButton_16.clicked.connect(lambda : self.tabWidget.setCurrentIndex(7))
        self.PushButton_32.clicked.connect(self.pic_echart)
        self.PushButton_17.clicked.connect(self.echarts_change)
        # self.PushButton_18.clicked.connect(self.changeWeather)

    #更新echarts绘图
    def echarts_change(self):
        if self.radar_view.page():
            jscode = "showPiChart(300,300,300,300,300,300)"
            self.radar_view.page().runJavaScript(jscode)



    #echart绘图
    def pic_echart(self):

        #清空图像
        if self.verticalLayout_11.count()>0:
            self.verticalLayout_11.removeItem(self.verticalLayout_11.itemAt(0))

        # self.statusBar().showMessage("图像加载中...")
        self.radar_view = QWebEngineView()

        self.radar_view.load(QUrl("file:///"+"chart.html"))  # 注意格式，绝对路径 radar_layout.addWidget(radar_view)

        # jscode = "showPiChart(1500,1500,1500,1500,1500,1500)"
        # self.radar_view.page().runJavaScript(jscode)

        self.verticalLayout_11.addWidget(self.radar_view)
        self.statusBar().showMessage("图像加载完毕")


    #添加城市
    def add_city(self):

        city = self.LineEdit_22.text()

        with open("./data/citycode.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        data_dict = {}
        for item in data:
            data_dict[item["city_name"]] = item["city_code"]
        if data_dict.get(city):
            self.ComboBox_2.addItem(city)
            self.city_dict[city] = data_dict[city]
            self.statusBar().showMessage("{}添加成功".format(city))
        else:
            QMessageBox.information(self,"提示","无该城市信息，无法添加该城市")


    # 天气预报
    def pre_weather(self):

        city_select = self.ComboBox_2.currentText()
        data = requests.get("http://t.weather.sojson.com/api/weather/city/{}".format(self.city_dict[city_select])).json()["data"]

        self.LineEdit_19.setText(data["wendu"])
        self.LineEdit_20.setText(data["shidu"])
        self.LineEdit_21.setText(data["quality"])


        result_data = []
        self.high = []
        self.low = []
        self.date_forecast = []
        for row,items in enumerate(data["forecast"]):
            tmp = [items["ymd"],items["high"],items["low"],items["fx"],items["fl"],items["type"]]
            self.date_forecast.append(items["ymd"])
            self.high.append(float(re.findall("高温.(\d+).",items["high"])[0]))
            self.low.append(float(re.findall("低温.(\d+).",items["low"])[0]))
            result_data.append(tmp)
        # print(result_data)
        # print(high,low)
        # print(len(date_forecast),date_forecast)

        self.TableWidget_weather.setRowCount(len(result_data))
        self.TableWidget_weather.setColumnCount(len(result_data[0]))
        self.TableWidget_weather.setHorizontalHeaderLabels(["日期", "最高气温", "最低气温", "风向", "风力", "天气"])
        self.TableWidget_weather.verticalHeader().setVisible(False)
        for row,items in enumerate(result_data):
            for column,item in enumerate(items):
                self.TableWidget_weather.setItem(row,column,QTableWidgetItem(item))

            # self.TableWidget_weather.setItem(row,0,QWidgetItem(str(items["ymd"])))
            # self.TableWidget_weather.setItem(row,1,QWidgetItem(items["high"]))
            # self.TableWidget_weather.setItem(row,2,QWidgetItem(items["low"]))
            # self.TableWidget_weather.setItem(row,3,QWidgetItem(items["fx"]))
            # self.TableWidget_weather.setItem(row,4,QWidgetItem(items["fl"]))
            # self.TableWidget_weather.setItem(row,5,QWidgetItem(items["type"]))

    #加载坐标轴
    def load_echarts(self):


        #清空布局，重新载入图片
        if self.verticalLayout_3.count() > 0:
            self.verticalLayout_3.removeItem(self.verticalLayout_3.itemAt(0))

        #echarts绘图
        self.weather = QWebEngineView()

        self.weather.load(QUrl("file:///" + "weather.html"))  # 注意格式，绝对路径 radar_layout.addWidget(radar_view)

        # jscode = "showPiChart(1500,1500,1500,1500,1500,1500)"
        # jscode = "weather({},{},{})".format(date_forecast,high,low)
        # jscode = '''
        # weather(['2023-07-15', '2023-07-16', '2023-07-17', '2023-07-18', '2023-07-19', '2023-07-20', '2023-07-21', '2023-07-22', '2023-07-23', '2023-07-24', '2023-07-25', '2023-07-26', '2023-07-27', '2023-07-28', '2023-07-29'],
        #       [35.0, 33.0, 32.0, 33.0, 33.0, 34.0, 33.0, 34.0, 37.0, 35.0, 34.0, 32.0, 31.0, 35.0, 31.0],
        #       [28.0, 28.0, 27.0, 27.0, 27.0, 28.0, 27.0, 27.0, 27.0, 28.0, 28.0, 28.0, 27.0, 28.0, 26.0])
        # '''

        self.verticalLayout_3.addWidget(self.weather)

        self.statusBar().showMessage("图像加载完毕")


    def changeWeather(self):

        self.label_19.setText("{}未来十五天气温走势图".format(self.ComboBox_2.currentText()))
        if self.weather.page():

            # forecast = ['2023-07-15', '2023-07-16', '2023-07-17', '2023-07-18', '2023-07-19', '2023-07-20', '2023-07-21', '2023-07-22', '2023-07-23', '2023-07-24', '2023-07-25', '2023-07-26', '2023-07-27', '2023-07-28', '2023-07-29']
            # high = [35.0, 33.0, 32.0, 33.0, 33.0, 34.0, 33.0, 34.0, 37.0, 35.0, 34.0, 32.0, 31.0, 35.0, 31.0]
            # low = [28.0, 28.0, 27.0, 27.0, 27.0, 28.0, 27.0, 27.0, 27.0, 28.0, 28.0, 28.0, 27.0, 28.0, 26.0]


            jscode = "weather({},{},{})".format(self.date_forecast,self.high,self.low)
            self.weather.page().runJavaScript(jscode)

        #QChart组件绘图
        # chart = QChart()
        # chart.setTitle("{}最高气温".format(city_select))
        # chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.legend().hide()
        #
        # line_series = QLineSeries()  # Using line charts for this example
        # line_series_2 = QLineSeries()  # Using line charts for this example
        # # x_values = [1, 2, 3, 4, 5, 6, 7]
        # # y_values = [1, 2, 4, 3, 1, 3, 5]
        # x_values = [i for i in range(1,16)]
        # y_values = high
        # # print(high)
        # # print(low)
        #
        # for value in range(0, len(x_values)):
        #     line_series.append(x_values[value], high[value])
        #     line_series_2.append(x_values[value], low[value])
        # chart.addSeries(line_series)  # Add line series to chart instance
        # chart.addSeries(line_series_2)  # Add line series to chart instance
        #
        #
        # axis_x = QValueAxis()
        # axis_x.setLabelFormat("%d")
        # chart.addAxis(axis_x, Qt.AlignBottom)
        # line_series.attachAxis(axis_x)
        # line_series_2.attachAxis(axis_x)
        #
        # axis_y = QValueAxis()
        # axis_y.setLabelFormat("%d")
        # chart.addAxis(axis_y, Qt.AlignLeft)
        # line_series.attachAxis(axis_y)
        # line_series_2.attachAxis(axis_y)
        #
        # chart_view = QChartView(chart)
        # chart_view.setRenderHint(QPainter.Antialiasing)
        #
        # self.verticalLayout_3.addWidget(chart_view)











    def slider_show(self):
        self.LineEdit_18.setText(str(self.Slider_2.value()))
    def test2(self):
        self.dgl.LineEdit.setText("95")
        self.dgl.LineEdit_2.setText("99")
        self.dgl.LineEdit_3.setText("97")

    def RadioButton_clicked(self,button):

        self.DisplayLabel_2.setText("欢迎{}".format(button.text()))

    def first_radio(self):
        if self.RadioButton.isChecked():
            self.RadioButton_clicked(self.RadioButton)

    # 图像绘制
    def plot(self):

        # random data
        data = [random.random() for i in range(10)]

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()



    def test1(self):
        self.PushButton_7.setEnabled(False)




    def lable_linkHovered(self):

        self.LineEdit_2.setText("鼠标滑过标签")

    def display_test(self):
        self.LineEdit_2.setText("测试文本")

    #从本地加载excel问阿金
    def open_file(self):

        filepath ,_  = QFileDialog.getOpenFileName(self)

        if filepath:
            df = pd.read_excel(filepath)

            # 设置行列，设置表头
            self.TableWidget.setRowCount(len(df))
            self.TableWidget.setColumnCount(len(df.columns.values))
            self.TableWidget.setHorizontalHeaderLabels(df.columns.values)
            # self.TableWidget.setVerticalHeaderLabels(df.index)
            # 表格加载内容
            for row, form in enumerate(df.values):
                for column, item in enumerate(form):
                    self.TableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    #选择行
    def select_row(self):

        data = self.TableWidget.selectedItems()
        if data:
            self.LineEdit_3.setText(data[0].text())
            self.LineEdit_4.setText(data[1].text())
            self.LineEdit_5.setText(data[2].text())
            self.LineEdit_6.setText(data[3].text())

    # 增加行
    def add_row(self):
        self.TableWidget.insertRow(self.TableWidget.rowCount())
        self.TableWidget.setItem(self.TableWidget.rowCount()-1,0,QTableWidgetItem(self.LineEdit_3.text()))
        # self.TableWidget.setItem(0,0,QTableWidgetItem(self.LineEdit_3.text()))
        self.TableWidget.setItem(self.TableWidget.rowCount()-1,1,QTableWidgetItem(self.LineEdit_4.text()))
        # self.TableWidget.setItem(0,1,QTableWidgetItem(self.LineEdit_4.text()))
        self.TableWidget.setItem(self.TableWidget.rowCount()-1,2,QTableWidgetItem(self.LineEdit_5.text()))
        # self.TableWidget.setItem(0,2,QTableWidgetItem(self.LineEdit_5.text()))
        self.TableWidget.setItem(self.TableWidget.rowCount()-1,3,QTableWidgetItem(self.LineEdit_6.text()))
        # self.TableWidget.setItem(0,3,QTableWidgetItem(self.LineEdit_6.text()))

    #删除行
    def del_row(self):
        row = self.TableWidget.currentRow()
        if row:
            self.TableWidget.removeRow(row)

    #保存数据
    def save_form(self):

        # print(self.TableWidget.currentItem())

        row = self.TableWidget.rowCount()
        column = self.TableWidget.columnCount()
        row_lst = []
        column_lst = []
        for i in range(row):
            for j in range(column):
                item = self.TableWidget.item(i, j).text()
                column_lst.append(item)
            row_lst.append(column_lst)
            column_lst = []

        data = pd.DataFrame(row_lst)

        filepath, _ = QFileDialog.getSaveFileName(self)

        if filepath:
            data.to_excel(filepath)




def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icons/应用图标.ico"))
    # app.setWindowIcon(QIcon("./icons/应用图标.jpg"))
    window = Mainapp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()






