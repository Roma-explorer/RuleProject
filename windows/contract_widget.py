# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contract_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ContractWidget(object):
    def setupUi(self, ContractWidget):
        ContractWidget.setObjectName("ContractWidget")
        ContractWidget.resize(400, 409)
        self.verticalLayout = QtWidgets.QVBoxLayout(ContractWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(ContractWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.contract_number = QtWidgets.QLineEdit(ContractWidget)
        self.contract_number.setObjectName("contract_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.contract_number)
        self.label_5 = QtWidgets.QLabel(ContractWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.cost_edit = QtWidgets.QLineEdit(ContractWidget)
        self.cost_edit.setObjectName("cost_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cost_edit)
        self.label_2 = QtWidgets.QLabel(ContractWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.sign_date = QtWidgets.QDateEdit(ContractWidget)
        self.sign_date.setCalendarPopup(True)
        self.sign_date.setDate(QtCore.QDate(2022, 1, 1))
        self.sign_date.setObjectName("sign_date")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sign_date)
        self.label_6 = QtWidgets.QLabel(ContractWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.duration_edit = QtWidgets.QLineEdit(ContractWidget)
        self.duration_edit.setObjectName("duration_edit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.duration_edit)
        self.label_7 = QtWidgets.QLabel(ContractWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.client_box = QtWidgets.QComboBox(ContractWidget)
        self.client_box.setEditable(True)
        self.client_box.setObjectName("client_box")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.client_box)
        self.label_12 = QtWidgets.QLabel(ContractWidget)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtWidgets.QLabel(ContractWidget)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.risks_edit = QtWidgets.QTextEdit(ContractWidget)
        self.risks_edit.setObjectName("risks_edit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.risks_edit)
        self.tech_task = QtWidgets.QPushButton(ContractWidget)
        self.tech_task.setObjectName("tech_task")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.tech_task)
        self.add_contract = QtWidgets.QPushButton(ContractWidget)
        self.add_contract.setObjectName("add_contract")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.add_contract)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(ContractWidget)
        QtCore.QMetaObject.connectSlotsByName(ContractWidget)

    def retranslateUi(self, ContractWidget):
        _translate = QtCore.QCoreApplication.translate
        ContractWidget.setWindowTitle(_translate("ContractWidget", "Dialog"))
        self.label_4.setText(_translate("ContractWidget", "Номер"))
        self.label_5.setText(_translate("ContractWidget", "Стоимость"))
        self.label_2.setText(_translate("ContractWidget", "Дата подписания"))
        self.label_6.setText(_translate("ContractWidget", "Длительность"))
        self.label_7.setText(_translate("ContractWidget", "Заказчик"))
        self.label_12.setText(_translate("ContractWidget", "Тех. задание"))
        self.label_13.setText(_translate("ContractWidget", "Риски"))
        self.tech_task.setText(_translate("ContractWidget", "Добавить техническое задание"))
        self.add_contract.setText(_translate("ContractWidget", "Добавить"))