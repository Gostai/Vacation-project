# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changeDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(580, 163)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBoxEmployee = QtWidgets.QComboBox(Dialog)
        self.comboBoxEmployee.setBaseSize(QtCore.QSize(50, 0))
        self.comboBoxEmployee.setObjectName("comboBoxEmployee")
        self.horizontalLayout_2.addWidget(self.comboBoxEmployee)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBoxPart = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxPart.setObjectName("comboBoxPart")
        self.verticalLayout.addWidget(self.comboBoxPart)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dateEditStart = QtWidgets.QDateEdit(self.groupBox_2)
        self.dateEditStart.setCalendarPopup(True)
        self.dateEditStart.setObjectName("dateEditStart")
        self.verticalLayout_2.addWidget(self.dateEditStart)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalSliderLength = QtWidgets.QSlider(self.groupBox_3)
        self.horizontalSliderLength.setMinimum(1)
        self.horizontalSliderLength.setMaximum(60)
        self.horizontalSliderLength.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderLength.setObjectName("horizontalSliderLength")
        self.horizontalLayout_4.addWidget(self.horizontalSliderLength)
        self.lcdNumberLength = QtWidgets.QLCDNumber(self.groupBox_3)
        self.lcdNumberLength.setProperty("intValue", 1)
        self.lcdNumberLength.setObjectName("lcdNumberLength")
        self.horizontalLayout_4.addWidget(self.lcdNumberLength)
        self.horizontalLayout_3.addWidget(self.groupBox_3)
        self.groupBoxWay = QtWidgets.QGroupBox(Dialog)
        self.groupBoxWay.setCheckable(True)
        self.groupBoxWay.setChecked(False)
        self.groupBoxWay.setObjectName("groupBoxWay")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBoxWay)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalSliderWay = QtWidgets.QSlider(self.groupBoxWay)
        self.horizontalSliderWay.setMaximum(14)
        self.horizontalSliderWay.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderWay.setObjectName("horizontalSliderWay")
        self.horizontalLayout_5.addWidget(self.horizontalSliderWay)
        self.lcdNumberWay = QtWidgets.QLCDNumber(self.groupBoxWay)
        self.lcdNumberWay.setObjectName("lcdNumberWay")
        self.horizontalLayout_5.addWidget(self.lcdNumberWay)
        self.horizontalLayout_3.addWidget(self.groupBoxWay)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.pushButtonOk = QtWidgets.QPushButton(Dialog)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout_6.addWidget(self.pushButtonOk)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_6.addWidget(self.pushButtonCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение отпуска"))
        self.label.setText(_translate("Dialog", "Выберите сотрудника:"))
        self.groupBox.setTitle(_translate("Dialog", "Часть отпуска"))
        self.groupBox_2.setTitle(_translate("Dialog", "Дата начала"))
        self.groupBox_3.setTitle(_translate("Dialog", "Длительность"))
        self.groupBoxWay.setTitle(_translate("Dialog", "Время на дорогу"))
        self.pushButtonOk.setText(_translate("Dialog", "Ok"))
        self.pushButtonCancel.setText(_translate("Dialog", "Отмена"))

