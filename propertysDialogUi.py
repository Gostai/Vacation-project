# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'propertysDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 307)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalSliderPercent = QtWidgets.QSlider(Dialog)
        self.horizontalSliderPercent.setMaximum(100)
        self.horizontalSliderPercent.setSliderPosition(20)
        self.horizontalSliderPercent.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderPercent.setObjectName("horizontalSliderPercent")
        self.horizontalLayout.addWidget(self.horizontalSliderPercent)
        self.lcdNumberPercent = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumberPercent.setObjectName("lcdNumberPercent")
        self.horizontalLayout.addWidget(self.lcdNumberPercent)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalSliderManagerPercent = QtWidgets.QSlider(Dialog)
        self.horizontalSliderManagerPercent.setMaximum(100)
        self.horizontalSliderManagerPercent.setSliderPosition(8)
        self.horizontalSliderManagerPercent.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderManagerPercent.setObjectName("horizontalSliderManagerPercent")
        self.horizontalLayout_2.addWidget(self.horizontalSliderManagerPercent)
        self.lcdNumberManagerPercent = QtWidgets.QLCDNumber(Dialog)
        self.lcdNumberManagerPercent.setObjectName("lcdNumberManagerPercent")
        self.horizontalLayout_2.addWidget(self.lcdNumberManagerPercent)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.checkBoxNCMatrix = QtWidgets.QCheckBox(Dialog)
        self.checkBoxNCMatrix.setObjectName("checkBoxNCMatrix")
        self.verticalLayout_3.addWidget(self.checkBoxNCMatrix)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.doubleSpinBoxGamma = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBoxGamma.setDecimals(5)
        self.doubleSpinBoxGamma.setMaximum(1.0)
        self.doubleSpinBoxGamma.setSingleStep(1e-05)
        self.doubleSpinBoxGamma.setProperty("value", 0.0005)
        self.doubleSpinBoxGamma.setObjectName("doubleSpinBoxGamma")
        self.verticalLayout_3.addWidget(self.doubleSpinBoxGamma)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxPercentInMonth = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxPercentInMonth.setObjectName("checkBoxPercentInMonth")
        self.verticalLayout.addWidget(self.checkBoxPercentInMonth)
        self.checkBoxPercent = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxPercent.setObjectName("checkBoxPercent")
        self.verticalLayout.addWidget(self.checkBoxPercent)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxPercentManagerInMonth = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxPercentManagerInMonth.setObjectName("checkBoxPercentManagerInMonth")
        self.verticalLayout_2.addWidget(self.checkBoxPercentManagerInMonth)
        self.checkBoxPercentManager = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxPercentManager.setObjectName("checkBoxPercentManager")
        self.verticalLayout_2.addWidget(self.checkBoxPercentManager)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButtonOk = QtWidgets.QPushButton(Dialog)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout_3.addWidget(self.pushButtonOk)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_3.addWidget(self.pushButtonCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "??????????????????"))
        self.label.setText(_translate("Dialog", "?????????????? ?????????????????????? ?? ?????????????? ????????????????????????"))
        self.label_2.setText(_translate("Dialog", "?????????????? ?????????????????????????? ?? ?????????????? ????????????????????????"))
        self.checkBoxNCMatrix.setText(_translate("Dialog", "???????????????????????? ?????????????? ??????????????????????????"))
        self.label_3.setText(_translate("Dialog", "???????????????? ?????????????????? ?????????? ????????????????????????"))
        self.groupBox.setTitle(_translate("Dialog", "????????????????????"))
        self.checkBoxPercentInMonth.setText(_translate("Dialog", "?????????????????? ?????????????? ???????????????????? ?? ??????????"))
        self.checkBoxPercent.setText(_translate("Dialog", "?????????????????? ?????????? ?????????????? ?????? ???????????????????? ???????????????????? ???????????????????????? "))
        self.groupBox_2.setTitle(_translate("Dialog", "????????????????????????"))
        self.checkBoxPercentManagerInMonth.setText(_translate("Dialog", "?????????????????? ?????????????? ?????????????????????????? ???????????????????? ?? ??????????"))
        self.checkBoxPercentManager.setText(_translate("Dialog", "?????????????????? ?????????? ?????????????? ?????? ???????????????????? ???????????????????? ???????????????????????? "))
        self.pushButtonOk.setText(_translate("Dialog", "Ok"))
        self.pushButtonCancel.setText(_translate("Dialog", "????????????"))

