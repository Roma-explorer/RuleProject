# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortemployee_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShortEmployeeWidget(object):
    def setupUi(self, ShortEmployeeWidget):
        ShortEmployeeWidget.setObjectName("ShortEmployeeWidget")
        ShortEmployeeWidget.resize(464, 41)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ShortEmployeeWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name = QtWidgets.QLabel(ShortEmployeeWidget)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)
        self.position = QtWidgets.QLabel(ShortEmployeeWidget)
        self.position.setObjectName("position")
        self.horizontalLayout.addWidget(self.position)
        self.department = QtWidgets.QLabel(ShortEmployeeWidget)
        self.department.setObjectName("department")
        self.horizontalLayout.addWidget(self.department)
        self.add_button = QtWidgets.QPushButton(ShortEmployeeWidget)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)

        self.retranslateUi(ShortEmployeeWidget)
        QtCore.QMetaObject.connectSlotsByName(ShortEmployeeWidget)

    def retranslateUi(self, ShortEmployeeWidget):
        _translate = QtCore.QCoreApplication.translate
        ShortEmployeeWidget.setWindowTitle(_translate("ShortEmployeeWidget", "Form"))
        self.name.setText(_translate("ShortEmployeeWidget", "name"))
        self.position.setText(_translate("ShortEmployeeWidget", "position"))
        self.department.setText(_translate("ShortEmployeeWidget", "department"))
        self.add_button.setText(_translate("ShortEmployeeWidget", "Добавить"))
