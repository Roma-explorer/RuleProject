import re
from datetime import datetime, date

from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from views import consts
from windows.employee_widget import Ui_EmployeeWidget
from windows.address_widget import Ui_AddressWidget
from windows.adddepartment_widget import Ui_AddDepartment

from db import session
from db.models import Address, Country, City, Region, Street, Employee, Position, EmployeeContract, Sex, Department

from views.utils import get_or_create, not_all_filled


class AddressWidget(qtw.QWidget):
    address_called = qtc.pyqtSignal()
    send_address = qtc.pyqtSignal(Address)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_AddressWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.address_called.connect(self.return_address)

    def return_address(self):

        country = self.ui.country_box.currentText()
        city = self.ui.city_box.currentText()
        region = self.ui.region_box.currentText()
        street = self.ui.street_box.currentText()
        house = self.ui.house_edit.text()

        if '' in [country, city, region, street, house]:
            not_all_filled()
        else:
            country, created = get_or_create(session, Country, name=country)
            if created:
                session.add(country)
                session.commit()
            region, created = get_or_create(session, Region, name=region, country_id=country.id)
            if created:
                session.add(region)
                session.commit()
            city, created = get_or_create(session, City, name=city, region_id=country.id)
            if created:
                session.add(city)
                session.commit()
            street, created = get_or_create(session, Street, name=street, city_id=city.id)
            if created:
                session.add(street)
                session.commit()
            address = Address(country_id=country.id, city_id=city.id, region_id=region.id,
                              street_id=street.id, house_number=int(house))
            session.add(address)
            session.commit()
            self.send_address.emit(address)


class EmployeeWidget(qtw.QWidget):
    employee_added = qtc.pyqtSignal(Employee)

    def __init__(self, side=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_EmployeeWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        # self.ui.sex_box.addItems([Sex.male.value, Sex.female.value])

        self.positions = [pos[0] for pos in session.query(Position.name).distinct()]
        self.ui.position.addItems(self.positions)

        self.departments = [dep[0] for dep in session.query(Department.name).distinct()]
        self.ui.department.addItems(self.departments)

        if side:
            self.ui.submitButton.hide()
            self.setWindowModality(qtc.Qt.ApplicationModal)

        self.ui.submitButton.clicked.connect(self.create_employee)

    def create_employee(self):
        self.name = self.ui.name.text()
        self.lastname = self.ui.lastname.text()
        self.surname = self.ui.surname.text()
        self.phone = self.ui.phone.text()
        self.email = self.ui.email.text()
        # self.sex = self.ui.sex_box.currentText()

        email_pattern = re.compile(
            "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
        if not email_pattern.match(self.email):
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Warning, text='Это не email')
            message.show()
            return

        self.birth_date = self.ui.date.date().toPyDate()
        self.position = self.ui.position.currentText()
        self.department = self.ui.department.currentText()
        self.worktype = self.ui.worktype.text()
        self.amount_hours = self.ui.amount_hours.text()
        self.start_period = self.ui.start_period.time().toPyTime()
        self.end_period = self.ui.end_period.time().toPyTime()
        self.sign_date = self.ui.sign_date.date().toPyDate()
        self.probation_date = self.ui.probation_date.date().toPyDate()

        if "" in [self.name, self.lastname, self.phone, self.email, self.position, self.department, self.amount_hours,
                  self.worktype]:
            not_all_filled()

        self.position, created = get_or_create(session, Position, name=self.position)

        if self.department not in self.departments:
            self.wdepartment = AddDepartmentWidget(name=self.department)
            self.wdepartment.return_department.connect(self.add_department)
            self.wdepartment.show()
        else:
            self.department = session.query(Department).filter_by(name=self.department).all()[0]
            self.save_employee()

    def save_employee(self):
        # sex = 'male' if self.sex == 'Мужской' else 'female'
        employee = Employee(name=self.name, lastname=self.lastname, surname=self.surname,
                            birth_date=self.birth_date, email=self.email, phone=self.phone,
                            department_id=self.department.id, position_id=self.position.id)
        session.add(employee)
        session.commit()
        consts.employee = employee
        consts.user.employee_id = employee.id
        session.add(consts.user)
        contract = EmployeeContract(position_id=self.position.id, num_hours=self.amount_hours,
                                    probation_time=self.probation_date, sign_date=self.sign_date,
                                    work_time=datetime.combine(date.today(), self.end_period)
                                              - datetime.combine(date.today(), self.start_period),
                                    employee_id=employee.id, work_type=self.worktype)
        session.add(contract)
        session.commit()
        self.employee_added.emit(employee)

    def add_department(self, *department):
        self.department = department[0]
        self.save_employee()


class AddDepartmentWidget(qtw.QWidget):
    return_department = qtc.pyqtSignal(Department)

    def __init__(self, name='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_AddDepartment()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.name.setText(name)

        self.ui.vlayout = qtw.QVBoxLayout()
        self.waddress = AddressWidget()
        self.waddress.send_address.connect(self.add_address)
        self.ui.vlayout.addWidget(self.waddress)
        self.ui.address_frame.setLayout(self.ui.vlayout)
        self.ui.submit_button.clicked.connect(self.add_department)

    def add_address(self, *address):
        self.address = address[0]

    def add_department(self):
        name = self.ui.name.text()

        if name == '':
            not_all_filled()
        elif name in session.query(Department.name).all():
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Warning, text='Такой департамент уже существует')
            message.show()
        else:
            self.waddress.address_called.emit()
            department = Department(name=name, address_id=self.address.id)
            session.add(department)
            session.commit()
            self.return_department.emit(department)
            self.close()
