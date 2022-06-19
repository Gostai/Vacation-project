# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dellRestsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(257, 114)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBoxEmployee = QtWidgets.QComboBox(Dialog)
        self.comboBoxEmployee.setObjectName("comboBoxEmployee")
        self.verticalLayout.addWidget(self.comboBoxEmployee)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonDell = QtWidgets.QPushButton(Dialog)
        self.pushButtonDell.setObjectName("pushButtonDell")
        self.horizontalLayout.addWidget(self.pushButtonDell)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Удалить отпуска сотрудника"))
        self.label.setText(_translate("Dialog", "Выберите сотрудника:"))
        self.pushButtonDell.setText(_translate("Dialog", "Удалить"))
        self.pushButtonCancel.setText(_translate("Dialog", "Отмена"))

