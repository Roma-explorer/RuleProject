# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'short_member.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShortMemberWidget(object):
    def setupUi(self, ShortMemberWidget):
        ShortMemberWidget.setObjectName("ShortMemberWidget")
        ShortMemberWidget.resize(343, 74)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShortMemberWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtWidgets.QLabel(ShortMemberWidget)
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.mail = QtWidgets.QLabel(ShortMemberWidget)
        self.mail.setObjectName("mail")
        self.verticalLayout.addWidget(self.mail)

        self.retranslateUi(ShortMemberWidget)
        QtCore.QMetaObject.connectSlotsByName(ShortMemberWidget)

    def retranslateUi(self, ShortMemberWidget):
        _translate = QtCore.QCoreApplication.translate
        ShortMemberWidget.setWindowTitle(_translate("ShortMemberWidget", "Form"))
        self.name.setText(_translate("ShortMemberWidget", "TextLabel"))
        self.mail.setText(_translate("ShortMemberWidget", "TextLabel"))
