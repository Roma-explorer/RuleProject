from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from windows.login_window import Ui_LoginDialog
from windows.register_window import Ui_RegisterDialog
from windows.welcome_projectslist import Ui_ProjectListWidget

from db import session
from db.models import User, Employee, Project

from views.utils import not_all_filled
from views import consts
from views.create_project import CreateProjectWidget
from views.manage_project import MainWindow
from views.shared_widgets import EmployeeWidget

user = None


class ClickableLabel(qtw.QLabel):
    clicked = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()


class HolderWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resize(358, 257)

        self.stackwidget = qtw.QStackedWidget()

        self.login_window = LoginDialog()
        self.login_window.register_clicked.connect(self.gotoregister)
        self.login_window.logged_in.connect(self.navigate_employee)
        self.stackwidget.addWidget(self.login_window)

        self.register_window = RegisterDialog()
        self.register_window.login_clicked.connect(self.gotologin)
        self.register_window.registered.connect(self.gotocreateemp)
        self.stackwidget.addWidget(self.register_window)

        self.create_project = CreateProjectWidget()
        self.stackwidget.addWidget(self.create_project)

        self.emp_widget = EmployeeWidget()
        self.emp_widget.employee_added.connect(self.navigate_employee)
        self.stackwidget.addWidget(self.emp_widget)
        self.stackwidget.setCurrentIndex(0)

        self.vlayout = qtw.QVBoxLayout(self)
        self.vlayout.addWidget(self.stackwidget)
        self.setLayout(self.vlayout)

    def navigate_employee(self, *employee):
        employee = employee[0]
        self.resize(333, 435)

        self.projects_list = WelcomeProjectListWidget(employee)
        self.projects_list.create_project.connect(self.gotomain)
        self.stackwidget.addWidget(self.projects_list)
        self.stackwidget.setCurrentIndex(4)

    def gotoregister(self):
        print("Went to register")
        self.resize(383, 299)
        self.stackwidget.setCurrentIndex(1)

    def gotocreateemp(self):
        print("Went to create Emp")
        self.resize(317, 440)
        self.stackwidget.setCurrentIndex(3)

    def gotologin(self):
        print("Went to log in")
        self.resize(358, 257)
        self.stackwidget.setCurrentIndex(0)

    def gotomain(self):
        self.main_window = MainWindow(consts.project)
        self.main_window.show()
        self.hide()


class LoginDialog(qtw.QDialog):

    register_clicked = qtc.pyqtSignal()
    logged_in = qtc.pyqtSignal(Employee)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        # self.ui.lunregistred = ClickableLabel(self.ui.lunregistred)
        self.ui.lunregistred.mousePressEvent = self.emit_register  # self.gotoregister
        # self.ui.lunregistred.mouseReleaseEvent = self.send_register  # self.gotoregister
        self.ui.submitButton.clicked.connect(self.log_in)
        # self.ui.lunregistred.clicked.connect(self.gotoregister)
        # self.ui.stacklayout = qtw.QStackedLayout(self)
        # self.ui.stacklayout.addChildLayout(self.ui.gridLayout)

    def emit_register(self, event):
        print("Send register")
        self.register_clicked.emit()

    def log_in(self):
        login = self.ui.loginBox.text()
        password = self.ui.passwordBox.text()
        user = session.query(User).filter_by(name=login).filter_by(password=password).all()
        if not user:
            error_message = qtw.QMessageBox(icon=qtw.QMessageBox.Critical, text='Такого пользователя не существует')
            error_message.show()
            return
        else:
            employee = user[0].employee
            consts.user = user
            consts.employee = employee
            self.logged_in.emit(employee)


class RegisterDialog(qtw.QDialog):

    login_clicked = qtc.pyqtSignal()
    registered = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_RegisterDialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.lenter.mousePressEvent = self.emit_login  # self.gotologin
        self.ui.submitButton.clicked.connect(self.register)
        # self.ui.stacklayout = qtw.QStackedLayout(self)
        # self.ui.stacklayout.addChildLayout(self.ui.gridLayout_2)

    def register(self):
        name = self.ui.loginBox.text()
        password = self.ui.passwordBox.text()
        sec_password = self.ui.checkpasswordBox.text()

        if '' in [name, password, sec_password]:
            not_all_filled()
        elif password != sec_password:
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Warning, text='Пароли не совпадают')
            message.show()
        elif session.query(User).filter_by(name=name).filter_by(password=password).all():
            message = qtw.QMessageBox(icon=qtw.QMessageBox.Warning, text='Такой пароль уже существует. Введите другой')
            message.show()
        else:
            user = User(name=name, password=password)
            session.add(user)
            session.commit()
            consts.user = user
            self.registered.emit()

    def emit_login(self, event):
        print("Login clicked")
        self.login_clicked.emit()

    def gotologin(self, event):
        self.login_dialog = LoginDialog()
        self.login_dialog.resize(358, 257)
        self.stackwidget = qtw.QStackedWidget()
        self.stackwidget.addWidget(self.login_dialog)
        # self.stackwidget.addWidget(self)
        # self.vlayout = qtw.QVBoxLayout(self)
        # self.vlayout.addLayout(self.ui.gridLayout_2)
        self.ui.gridLayout_2.addWidget(self.stackwidget)
        self.setLayout(self.vlayout)
        self.stackwidget.show()
        self.stackwidget.setCurrentIndex(1)


class WelcomeProjectListWidget(qtw.QWidget):

    create_project = qtc.pyqtSignal()

    def __init__(self, employee, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ProjectListWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.employee = employee

        if self.employee:
            for project in self.employee.projects:
                pr = ProjectItemWidget(project.projects)
                pr.project_clicked.connect(self.open_project)
                item = qtw.QListWidgetItem()
                widgetLayout = qtw.QHBoxLayout()
                widgetLayout.addStretch()
                widgetLayout.setSizeConstraint(qtw.QLayout.SetMaximumSize)
                pr.setLayout(widgetLayout)
                hint = pr.sizeHint()
                hint.setHeight(pr.size().height() + 15)
                item.setSizeHint(hint)

                self.ui.projects_list.addItem(item)
                self.ui.projects_list.setItemWidget(item, pr)

        self.ui.add_button.clicked.connect(self.open_create_project)

    def open_create_project(self):
        self.CreateProject = CreateProjectWidget()
        self.CreateProject.project_created.connect(self.project_created)
        self.CreateProject.show()

    def project_created(self, *project):
        consts.project = project
        self.create_project.emit()

    def open_project(self, *project):
        project = project[0]
        self.main_window = MainWindow(project)
        self.main_window.show()
        self.hide()


class ProjectItemWidget(qtw.QWidget):

    project_clicked = qtc.pyqtSignal(Project)

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = project

        self.resize(200, 20)
        lname = qtw.QLabel(text=project.name)
        self.hlayout = qtw.QHBoxLayout(self)
        self.hlayout.addWidget(lname)
        self.setLayout(self.hlayout)

        self.mouseDoubleClickEvent = self.project_click

    def project_click(self, event):
        self.project_clicked.emit(self.project)

