from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from db import session
from db.models import Contract, Client, TechTask, Requirement, Project, EmployeeProject
from views import consts
from views.manage_project import MainWindow
from views.shared_widgets import AddressWidget
from windows.projectcreate_widget import Ui_CreateProjectWidget
from windows.contract_widget import Ui_ContractWidget
from windows.techtask_window import Ui_TeckTaskDialog
from windows.requirement_widget import Ui_ReqWidget
from windows.client_widget import Ui_ClientWidget

from views.utils import *


class CreateProjectWidget(qtw.QWidget):

    project_created = qtc.pyqtSignal(Project)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_CreateProjectWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.contract_add.clicked.connect(self.open_contractwidget)
        self.ui.submitButton.clicked.connect(self.add_project)

    def open_contractwidget(self):
        self.add_contract_dialog = AddContractDialog()
        self.add_contract_dialog.contract_created.connect(self.add_contract)
        self.add_contract_dialog.show()

    def add_contract(self, *contract):
        self.contract = contract[0]
        self.ui.contract_add.setText('Добавлено')

    def add_project(self):
        name = self.ui.name.text()
        start_date = self.ui.start_date.date().toPyDate()
        end_date = self.ui.end_date.date().toPyDate()
        description = self.ui.description.toPlainText()

        if self.ui.contract_add.text() == 'Добавить контракт':
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Critical, text='Нужно добавить контракт')
            message.show()
            return
        elif name == '':
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Critical, text='Нужно ввести название проекта')
            message.show()
            return
        else:
            project = Project(name=name, description=description, date_start=start_date, date_end=end_date,
                              contract_id=self.contract.number, head_id=consts.employee.id)
            session.add(project)
            session.commit()
            consts.project = project

            empproject = EmployeeProject(project_id=project.id, employee_id=consts.employee.id)
            session.add(empproject)
            session.commit()

            main_window = MainWindow(project)
            main_window.show()
            self.close()


class AddContractDialog(qtw.QWidget):

    contract_created = qtc.pyqtSignal(Contract)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ContractWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.clients = [client.name for client in session.query(Client).all()]
        self.ui.client_box.addItems(self.clients)

        self.ui.tech_task.clicked.connect(self.open_techtaskdialog)
        self.ui.add_contract.clicked.connect(self.add_contract)

    def open_techtaskdialog(self):
        self.techtask_dialog = TechTaskDialog()
        self.techtask_dialog.techtask_created.connect(self.add_techtask)
        self.techtask_dialog.show()

    def add_techtask(self, tech_task):
        self.techtask = tech_task
        self.ui.tech_task.setText('Добавлено')

    def add_contract(self):
        if self.ui.tech_task.text() == 'Добавить техническое задание':
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Critical, text='Добавьте техническое задание')
            message.show()
            return
        else:
            self.number = self.ui.contract_number.text()
            self.cost = self.ui.cost_edit.text()
            self.sign_date = self.ui.sign_date.date().toPyDate()
            self.duration = self.ui.duration_edit.text()
            self.client = self.ui.client_box.currentText()
            self.risks = self.ui.risks_edit.toPlainText()
            if '' in [self.number, self.cost, self.sign_date, self.duration, self.client, self.risks]:
                not_all_filled()
                return
            else:
                if self.client not in self.clients:
                    self.client_window = ClientWidget()
                    self.client_window.client_created.connect(self.add_client)
                    self.client_window.show()
                else:
                    self.client = session.query(Client).filter_by(name=self.client).all()[0]
                    self.save_contract()

    def save_contract(self):
        contract = Contract(number=int(self.number), cost=float(self.cost), sign_date=self.sign_date,
                            duration=self.duration, risks=self.risks, tech_task_id=self.techtask.id,
                            client_id=self.client.id)
        session.add(contract)
        session.commit()
        self.contract_created.emit(contract)
        self.close()

    def add_client(self, *client):
        self.client = client[0]
        self.save_contract()


class ClientWidget(qtw.QWidget):

    client_created = qtc.pyqtSignal(Client)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ClientWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.vlayout = qtw.QVBoxLayout()
        self.waddress = AddressWidget()
        self.waddress.send_address.connect(self.add_address)
        self.ui.vlayout.addWidget(self.waddress)
        self.ui.address_frame.setLayout(self.ui.vlayout)

        self.ui.submit_button.clicked.connect(self.add_client)

    def add_client(self):
        company_name = self.ui.compname.text()
        account = self.ui.account.text()
        inn = self.ui.inn.text()
        ogrn = self.ui.ogrn.text()
        phone = self.ui.phone.text()
        email = self.ui.email.text()

        if '' in [company_name, account, inn, ogrn, phone, email]:
            not_all_filled()
            return
        else:
            self.waddress.address_called.emit()
            client = Client(name=company_name, account=account, inn=inn, ogrn=ogrn,
                            phone=phone, email=email, address_id=self.address.id)
            session.add(client)
            session.commit()

            self.client_created.emit(client)
            self.close()

    def add_address(self, *address):
        self.address = address[0]


class TechTaskDialog(qtw.QDialog):

    techtask_created = qtc.pyqtSignal(TechTask)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_TeckTaskDialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.scrollreq = qtw.QWidget()
        self.layout = qtw.QVBoxLayout()
        self.scrollreq.setLayout(self.layout)
        self.ui.req_scroll.setWidget(self.scrollreq)
        self.ui.add_req.clicked.connect(self.add_requirement)

        self.ui.submitButton.clicked.connect(self.add_techtask)

    def add_requirement(self):
        req_widget = RequirementWidget()
        self.layout.addWidget(req_widget)

    def add_techtask(self):
        number = self.ui.num_edit.text()
        description = self.ui.description_edit.toPlainText()
        purpose = self.ui.purpose_edit.toPlainText()
        work_order = self.ui.workorder_edit.toPlainText()
        controls = self.ui.control_edit.toPlainText()

        if description == '':
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Critical)
            message.show()
            return
        else:
            reqs = self.add_reqs(self.layout)
            tech_task = TechTask(number=number, description=description, purpose=purpose,
                                 work_order=work_order, control_procedures=controls)
            session.add(tech_task)
            session.commit()
            for req in reqs:
                req.tech_task_id = tech_task.id

            session.add_all(reqs)
            session.commit()

            self.techtask_created.emit(tech_task)
            self.close()

    def add_reqs(self, layout: qtw.QVBoxLayout()):
        index = layout.count()
        reqs = []
        index -= 1
        while index >= 0:
            req_info: RequirementWidget = layout.itemAt(index).widget()
            gost = req_info.ui.gost.text()
            if gost:
                req_skill = Requirement(gost=gost, content=req_info.ui.content.toPlainText())
                reqs.append(req_skill)
            index -= 1
         # session.add_all(reqs)
        return reqs


class RequirementWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ReqWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.remreq_button.clicked.connect(self.close)


if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = CreateProjectWidget()
    widget.show()

    app.exec_()
