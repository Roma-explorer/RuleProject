# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'address_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddressWidget(object):
    def setupUi(self, AddressWidget):
        AddressWidget.setObjectName("AddressWidget")
        AddressWidget.resize(260, 155)
        self.formLayout = QtWidgets.QFormLayout(AddressWidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(AddressWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.country_box = QtWidgets.QComboBox(AddressWidget)
        self.country_box.setEditable(True)
        self.country_box.setObjectName("country_box")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.country_box)
        self.label_2 = QtWidgets.QLabel(AddressWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.region_box = QtWidgets.QComboBox(AddressWidget)
        self.region_box.setEditable(True)
        self.region_box.setObjectName("region_box")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.region_box)
        self.label_4 = QtWidgets.QLabel(AddressWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.city_box = QtWidgets.QComboBox(AddressWidget)
        self.city_box.setEditable(True)
        self.city_box.setObjectName("city_box")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.city_box)
        self.label_5 = QtWidgets.QLabel(AddressWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.street_box = QtWidgets.QComboBox(AddressWidget)
        self.street_box.setEditable(True)
        self.street_box.setObjectName("street_box")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.street_box)
        self.lphone = QtWidgets.QLabel(AddressWidget)
        self.lphone.setObjectName("lphone")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lphone)
        self.house_edit = QtWidgets.QLineEdit(AddressWidget)
        self.house_edit.setObjectName("house_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.house_edit)

        self.retranslateUi(AddressWidget)
        QtCore.QMetaObject.connectSlotsByName(AddressWidget)

    def retranslateUi(self, AddressWidget):
        _translate = QtCore.QCoreApplication.translate
        AddressWidget.setWindowTitle(_translate("AddressWidget", "Form"))
        self.label.setText(_translate("AddressWidget", "Страна"))
        self.label_2.setText(_translate("AddressWidget", "Регион"))
        self.label_4.setText(_translate("AddressWidget", "Город"))
        self.label_5.setText(_translate("AddressWidget", "Улица"))
        self.lphone.setText(_translate("AddressWidget", "Номер дома"))