# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AdUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(898, 479)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("vacation.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxYear = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxYear.setObjectName("comboBoxYear")
        self.horizontalLayout.addWidget(self.comboBoxYear)
        self.labelBanner = QtWidgets.QLabel(self.centralwidget)
        self.labelBanner.setObjectName("labelBanner")
        self.horizontalLayout.addWidget(self.labelBanner)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableWidget.setFont(font)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(19)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout.addWidget(self.tableWidget)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setBaseSize(QtCore.QSize(50, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelName = QtWidgets.QLabel(self.groupBox_2)
        self.labelName.setBaseSize(QtCore.QSize(50, 0))
        self.labelName.setObjectName("labelName")
        self.verticalLayout_2.addWidget(self.labelName)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBoxNumParts = QtWidgets.QGroupBox(self.groupBox)
        self.groupBoxNumParts.setObjectName("groupBoxNumParts")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxNumParts)
        self.gridLayout.setObjectName("gridLayout")
        self.lcdNumberNP = QtWidgets.QLCDNumber(self.groupBoxNumParts)
        self.lcdNumberNP.setProperty("intValue", 1)
        self.lcdNumberNP.setObjectName("lcdNumberNP")
        self.gridLayout.addWidget(self.lcdNumberNP, 0, 1, 1, 1)
        self.horizontalSliderNumParts = QtWidgets.QSlider(self.groupBoxNumParts)
        self.horizontalSliderNumParts.setBaseSize(QtCore.QSize(40, 0))
        self.horizontalSliderNumParts.setMinimum(1)
        self.horizontalSliderNumParts.setMaximum(6)
        self.horizontalSliderNumParts.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderNumParts.setObjectName("horizontalSliderNumParts")
        self.gridLayout.addWidget(self.horizontalSliderNumParts, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBoxNumParts)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox_3)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_3.addWidget(self.dateEdit)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalSliderRestLength = QtWidgets.QSlider(self.groupBox_5)
        self.horizontalSliderRestLength.setMinimum(1)
        self.horizontalSliderRestLength.setMaximum(60)
        self.horizontalSliderRestLength.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderRestLength.setObjectName("horizontalSliderRestLength")
        self.horizontalLayout_5.addWidget(self.horizontalSliderRestLength)
        self.lcdNumberLength = QtWidgets.QLCDNumber(self.groupBox_5)
        self.lcdNumberLength.setProperty("intValue", 1)
        self.lcdNumberLength.setObjectName("lcdNumberLength")
        self.horizontalLayout_5.addWidget(self.lcdNumberLength)
        self.horizontalLayout_2.addWidget(self.groupBox_5)
        self.groupBoxWay = QtWidgets.QGroupBox(self.groupBox)
        self.groupBoxWay.setCheckable(True)
        self.groupBoxWay.setChecked(False)
        self.groupBoxWay.setObjectName("groupBoxWay")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBoxWay)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalSliderRestWayLength = QtWidgets.QSlider(self.groupBoxWay)
        self.horizontalSliderRestWayLength.setMaximum(20)
        self.horizontalSliderRestWayLength.setSingleStep(2)
        self.horizontalSliderRestWayLength.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderRestWayLength.setObjectName("horizontalSliderRestWayLength")
        self.horizontalLayout_3.addWidget(self.horizontalSliderRestWayLength)
        self.lcdNumberWay = QtWidgets.QLCDNumber(self.groupBoxWay)
        self.lcdNumberWay.setObjectName("lcdNumberWay")
        self.horizontalLayout_3.addWidget(self.lcdNumberWay)
        self.horizontalLayout_2.addWidget(self.groupBoxWay)
        self.pushButtonSetRest = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonSetRest.setObjectName("pushButtonSetRest")
        self.horizontalLayout_2.addWidget(self.pushButtonSetRest)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menuBar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menuBar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionChangeOneRest = QtWidgets.QAction(MainWindow)
        self.actionChangeOneRest.setObjectName("actionChangeOneRest")
        self.actionChangeOneNumRests = QtWidgets.QAction(MainWindow)
        self.actionChangeOneNumRests.setObjectName("actionChangeOneNumRests")
        self.actionDelOneRest = QtWidgets.QAction(MainWindow)
        self.actionDelOneRest.setObjectName("actionDelOneRest")
        self.actionDelAll = QtWidgets.QAction(MainWindow)
        self.actionDelAll.setObjectName("actionDelAll")
        self.actionListsAndRatings = QtWidgets.QAction(MainWindow)
        self.actionListsAndRatings.setObjectName("actionListsAndRatings")
        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")
        self.actionSaveGraph = QtWidgets.QAction(MainWindow)
        self.actionSaveGraph.setObjectName("actionSaveGraph")
        self.actionSaveExcelView = QtWidgets.QAction(MainWindow)
        self.actionSaveExcelView.setObjectName("actionSaveExcelView")
        self.actionPreShowGraph = QtWidgets.QAction(MainWindow)
        self.actionPreShowGraph.setObjectName("actionPreShowGraph")
        self.actionSaveDencity = QtWidgets.QAction(MainWindow)
        self.actionSaveDencity.setObjectName("actionSaveDencity")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNotCrossingMatrix = QtWidgets.QAction(MainWindow)
        self.actionNotCrossingMatrix.setObjectName("actionNotCrossingMatrix")
        self.menu.addAction(self.actionExit)
        self.menu_2.addAction(self.actionChangeOneRest)
        self.menu_2.addAction(self.actionChangeOneNumRests)
        self.menu_2.addAction(self.actionDelOneRest)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.actionDelAll)
        self.menu_2.addAction(self.actionListsAndRatings)
        self.menu_2.addAction(self.actionNotCrossingMatrix)
        self.menu_2.addAction(self.actionOptions)
        self.menu_3.addAction(self.actionPreShowGraph)
        self.menu_3.addAction(self.actionSaveGraph)
        self.menu_3.addAction(self.actionSaveExcelView)
        self.menu_3.addAction(self.actionSaveDencity)
        self.menu_4.addAction(self.actionAbout)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu_3.menuAction())
        self.menuBar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "???????????????????????? ????????????????"))
        self.labelBanner.setText(_translate("MainWindow", "?????????? ?????????????? ???? 2020 ??????"))
        self.groupBox.setTitle(_translate("MainWindow", "?????????? ??????????????"))
        self.groupBox_2.setTitle(_translate("MainWindow", "??????????????????:"))
        self.labelName.setText(_translate("MainWindow", "???????????? ??.??."))
        self.groupBoxNumParts.setTitle(_translate("MainWindow", "???????????????????? ????????????:"))
        self.groupBox_3.setTitle(_translate("MainWindow", "???????? ????????????"))
        self.groupBox_5.setTitle(_translate("MainWindow", "???????????????????????? ??????????:"))
        self.groupBoxWay.setTitle(_translate("MainWindow", "?????????? ???? ????????????: 0"))
        self.pushButtonSetRest.setText(_translate("MainWindow", "??????????????????"))
        self.menu.setTitle(_translate("MainWindow", "????????"))
        self.menu_2.setTitle(_translate("MainWindow", "????????????????????????????"))
        self.menu_3.setTitle(_translate("MainWindow", "????????????????"))
        self.menu_4.setTitle(_translate("MainWindow", "????????????"))
        self.actionExit.setText(_translate("MainWindow", "??????????"))
        self.actionChangeOneRest.setText(_translate("MainWindow", "???????????????? ???????????? ????????????????????"))
        self.actionChangeOneNumRests.setText(_translate("MainWindow", "???????????????? ???????????????????? ????????????????"))
        self.actionDelOneRest.setText(_translate("MainWindow", "?????????????? ???????????? ????????????????????"))
        self.actionDelAll.setText(_translate("MainWindow", "???????????????? ?????? ??????????????"))
        self.actionListsAndRatings.setText(_translate("MainWindow", "???????????? ?? ????????????????"))
        self.actionOptions.setText(_translate("MainWindow", "??????????????????"))
        self.actionSaveGraph.setText(_translate("MainWindow", "?????????????????? ????????????"))
        self.actionSaveExcelView.setText(_translate("MainWindow", "?????????????????? ??????????????????????????"))
        self.actionPreShowGraph.setText(_translate("MainWindow", "?????????????????????????????? ????????????????"))
        self.actionSaveDencity.setText(_translate("MainWindow", "?????????????????? ?????????????????? ????????"))
        self.actionAbout.setText(_translate("MainWindow", "?? ??????????????????"))
        self.actionNotCrossingMatrix.setText(_translate("MainWindow", "?????????????? ??????????????????????????"))

