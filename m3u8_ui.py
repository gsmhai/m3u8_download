# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'm3u8_downloader.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.m3u8_url = QtWidgets.QLineEdit(self.centralwidget)
        self.m3u8_url.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m3u8_url.sizePolicy().hasHeightForWidth())
        self.m3u8_url.setSizePolicy(sizePolicy)
        self.m3u8_url.setObjectName("m3u8_url")
        self.gridLayout.addWidget(self.m3u8_url, 0, 1, 1, 5)
        self.Download = QtWidgets.QPushButton(self.centralwidget)
        self.Download.setObjectName("Download")
        self.gridLayout.addWidget(self.Download, 0, 6, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.save_file = QtWidgets.QLineEdit(self.centralwidget)
        self.save_file.setObjectName("save_file")
        self.gridLayout.addWidget(self.save_file, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.proxy = QtWidgets.QLineEdit(self.centralwidget)
        self.proxy.setObjectName("proxy")
        self.gridLayout.addWidget(self.proxy, 1, 3, 1, 1)
        self.cbProxy = QtWidgets.QCheckBox(self.centralwidget)
        self.cbProxy.setObjectName("cbProxy")
        self.gridLayout.addWidget(self.cbProxy, 1, 4, 1, 1)
        self.cbDecrypt = QtWidgets.QCheckBox(self.centralwidget)
        self.cbDecrypt.setChecked(True)
        self.cbDecrypt.setObjectName("cbDecrypt")
        self.gridLayout.addWidget(self.cbDecrypt, 1, 5, 1, 1)
        self.cbCombine = QtWidgets.QCheckBox(self.centralwidget)
        self.cbCombine.setChecked(True)
        self.cbCombine.setObjectName("cbCombine")
        self.gridLayout.addWidget(self.cbCombine, 1, 6, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 637, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "M3U8 Downloader"))
        self.label.setText(_translate("MainWindow", "M3U8 Url"))
        self.Download.setText(_translate("MainWindow", "Download"))
        self.label_2.setText(_translate("MainWindow", "File Name"))
        self.label_3.setText(_translate("MainWindow", "Proxy"))
        self.proxy.setText(_translate("MainWindow", "10.217.10.40:80"))
        self.cbProxy.setText(_translate("MainWindow", "UseProxy"))
        self.cbDecrypt.setText(_translate("MainWindow", "Auto Decrypt"))
        self.cbCombine.setText(_translate("MainWindow", "Auto Merge"))