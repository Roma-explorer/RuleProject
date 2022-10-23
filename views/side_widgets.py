from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from db.models import Status, Priority, Task, Contract, Mistake, Feature
from views import consts

from windows.side_task import Ui_SideTaskWidget
from windows.side_client import Ui_SideClientWidget


class SideTaskWidget(qtw.QWidget):

    def __init__(self, task: Task or Mistake or Feature, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_SideTaskWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.task = task

        self.ui.priority_box.addItems([p.value for p in Priority])
        self.ui.status_box.addItems([s.value for s in Status])

        self.members = []
        for member in consts.project.employees:
            emp = member.employees
            self.members.append(emp)
            name = ' '.join([emp.surname, emp.name])
            self.ui.member_box.addItem(name)

        self.type_modify()
        self.populate_widget()

    def type_modify(self):
        if type(self.task) == Mistake:
            self.ui.ltype.setText('Баг')
            self.ui.feature_box.setCurrentText(self.task.feature.name)
        elif type(self.task) == Feature:
            self.ui.ltype.setText('Функционал')
            self.ui.lreason.hide()
            self.ui.reason.hide()
            self.ui.ladd_to.hide()
            self.ui.feature_box.hide()
        elif type(self.task) == Task:
            self.ui.ltype.setText("Задача")
            self.ui.feature_box.setCurrentText(self.task.feature.name)
            self.ui.lreason.hide()
            self.ui.reason.hide()

    def populate_widget(self):
        self.ui.name.setText(self.task.name)
        self.ui.description.setPlainText(self.task.description.text)
        self.ui.date_start.setDate(self.task.date_start)
        self.ui.date_end.setDate(self.task.date_end)
        self.ui.planned_hours.setValue(self.task.planned_hours)
        self.ui.dedicated_hours.setValue(self.task.dedicated_hours)
        self.ui.priority_box.setCurrentText(self.task.priority.value)
        self.ui.status_box.setCurrentText(self.task.status.value)

        if type(self.task) != Feature:
            executor = self.task.employee
            self.ui.member_box.setCurrentText(' '.join([executor.surname, executor.name]))
        else:
            executor = self.task.emprojfeatures[0].employee_projects.employees
            self.ui.member_box.setCurrentText(' '.join([executor.surname, executor.name]))

        if type(self.task) == Mistake:
            self.ui.reason.setPlainText(self.task.reason.text)


class SideClientWidget(qtw.QWidget):

    def __init__(self, contract: Contract, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_SideClientWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.contract = contract
        self.client = contract.client

        self.populate_widget()

    def populate_widget(self):
        self.ui.compname.setText(self.client.name)
        self.ui.account.setText(self.client.account)
        self.ui.inn.setText(self.client.inn)
        self.ui.ogrn.setText(self.client.ogrn)
        self.ui.email.setText(self.client.email)
        self.ui.phone.setText(self.client.phone)

        self.ui.contract_number.setText(str(self.contract.number))
        self.ui.cost_edit.setText(str(self.contract.cost))
        self.ui.sign_date.setDate(self.contract.sign_date)
