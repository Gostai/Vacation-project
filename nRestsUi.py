# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nRestsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(246, 238)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.comboBoxEmployee = QtWidgets.QComboBox(Dialog)
        self.comboBoxEmployee.setObjectName("comboBoxEmployee")
        self.verticalLayout.addWidget(self.comboBoxEmployee)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.lcdNumberNRest = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumberNRest.setObjectName("lcdNumberNRest")
        self.verticalLayout.addWidget(self.lcdNumberNRest)
        self.horizontalSliderNumRests = QtWidgets.QSlider(Dialog)
        self.horizontalSliderNumRests.setMinimum(1)
        self.horizontalSliderNumRests.setMaximum(6)
        self.horizontalSliderNumRests.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderNumRests.setObjectName("horizontalSliderNumRests")
        self.verticalLayout.addWidget(self.horizontalSliderNumRests)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonOk = QtWidgets.QPushButton(Dialog)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Введите количестов частей"))
        self.label.setText(_translate("Dialog", "Выберите сотрудника:"))
        self.label_2.setText(_translate("Dialog", "Выберите количество частей:"))
        self.pushButtonOk.setText(_translate("Dialog", "Ок"))
        self.pushButtonCancel.setText(_translate("Dialog", "Отмена"))

