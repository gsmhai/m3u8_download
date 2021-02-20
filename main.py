# -*- coding: utf-8 -*-
# version: 0.1
# source: https://github.com/gsmhai/m3u8_download
# author: gsmhai

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import m3u8_ui
import m3u8_downloader

DownThread = None
listViewMode = None


class Downloadthread(QThread):
    breakSignal = pyqtSignal()
    printSignal = pyqtSignal(str)
    initSignal = pyqtSignal(list)
    updateSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        init_downloader()
        m3u8_downloader.breakSignal = self.breakSignal
        m3u8_downloader.printSignal = self.printSignal
        m3u8_downloader.initSignal = self.initSignal
        m3u8_downloader.updateSignal = self.updateSignal
        m3u8_downloader.Download()


def setColortoRow(QItemModel, rowIndex, color):
    if QItemModel.rowCount() > rowIndex:
        for i in range(QItemModel.columnCount()):
            item = QItemModel.item(rowIndex, i)
            if item is not None:
                item.setBackground(color)

def ReleaseButton():
    ui.Download.setEnabled(True)

def PrintInfo(msg=""):
    ui.statusbar.showMessage(msg, 20000)


def InitPlayList(playlist):
    global listViewMode
    listViewMode.removeRows(0, listViewMode.rowCount())
    for index, item in enumerate(playlist):
        listViewMode.setItem(index, 0, QStandardItem('%d' % (index+1)))
        listViewMode.setItem(index, 1, QStandardItem(item))
        listViewMode.setItem(index, 2, QStandardItem('等待下载'))


def UpdatePlayList(task_info):
    global listViewMode
    row = task_info[0]
    listViewMode.setItem(row, 2, QStandardItem(task_info[1]))
    if task_info[1] in '完成':
        setColortoRow(listViewMode, row, QColor(192, 253, 123))


def click_success():
    global DownThread
    ui.Download.setEnabled(False)
    DownThread = Downloadthread()
    DownThread.breakSignal.connect(ReleaseButton)
    DownThread.printSignal.connect(PrintInfo)
    DownThread.initSignal.connect(InitPlayList)
    DownThread.updateSignal.connect(UpdatePlayList)
    DownThread.start()


def init_downloader():
    #m3u8_Downloader.workDirPath = "Z:/"
    m3u8_downloader.m3u8IndexFile = "Z:/index.m3u8"
    url = ui.m3u8_url.text()
    title = ui.save_file.text()
    if len(title) < 4:
        title = '电影_' + url.rsplit('.', 1)[0].rsplit('/', 1)[1] + '.mp4'
    m3u8_downloader.m3u8Url = url
    m3u8_downloader.title = title
    proxy = {'http': 'http://' + ui.proxy.text(), 'https': 'https://' + ui.proxy.text()}
    m3u8_downloader.proxy = proxy
    m3u8_downloader.UseProxy = ui.cbProxy.isChecked()
    m3u8_downloader.MainUI = ui


def InitMainWindow():
    global listViewMode
    ui.m3u8_url.setText("https://bilibili.xiang-kuyun.com/20210214/11576_c9f0a0ea/index.m3u8?sign=3e7bf3669d4d88a86e5c57d7e3d67387")
    ui.save_file.setText('碰撞地球')
    listViewMode = QStandardItemModel(0, 3)
    listViewMode.setHorizontalHeaderLabels([' # ', '视频流地址', '状态'])
    #for row in range(3):
    #        for column in range(3):
    #            item=QStandardItem('row %s,column %s'%(row,column))
    #            listViewMode.setItem(row,column,item)
    ui.tableView.setModel(listViewMode)
    ui.tableView.setColumnWidth(0, 40)
    ui.tableView.setColumnWidth(1, 600)

    stylesheet = "QHeaderView::section{background:#99CCFF;font: bold 11px;border-width: 2px;}"
    ui.tableView.horizontalHeader().setStyleSheet(stylesheet)

    #ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode())
    ui.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
    ui.tableView.verticalHeader().setVisible(False)
    ui.tableView.horizontalHeader().setHighlightSections(False)

    stylesheet = "QTableView{background-color:white;alternate-background-color: rgb(233, 248, 254)};}"
    ui.tableView.setStyleSheet(stylesheet)
    #ui.tableView.setColumnWidth(1,40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = m3u8_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    InitMainWindow()
    MainWindow.show()
    ui.Download.clicked.connect(click_success)
    sys.exit(app.exec_())
