from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from windows.employee_widget import Ui_EmployeeWidget
from windows.login_window import Ui_LoginDialog
from windows.register_window import Ui_RegisterDialog

from db import s


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
        self.stackwidget.addWidget(self.login_window)
        self.register_window = RegisterDialog()
        self.register_window.login_clicked.connect(self.gotologin)
        self.register_window.registered.connect(self.gotocreateemp)
        self.stackwidget.addWidget(self.register_window)
        self.emp_widget = EmployeeWidget()
        self.stackwidget.addWidget(self.emp_widget)
        self.stackwidget.setCurrentIndex(0)

        self.vlayout = qtw.QVBoxLayout(self)
        self.vlayout.addWidget(self.stackwidget)
        self.setLayout(self.vlayout)

    def gotoregister(self):
        print("Went to register")
        self.resize(383, 299)
        self.stackwidget.setCurrentIndex(1)

    def gotocreateemp(self):
        print("Went to create Emp")
        self.resize(317, 440)
        self.stackwidget.setCurrentIndex(2)

    def gotologin(self):
        print("Went to log in")
        self.resize(358, 257)
        self.stackwidget.setCurrentIndex(0)


class LoginDialog(qtw.QDialog):

    register_clicked = qtc.pyqtSignal()
    logged_in = qtc.pyqtSignal()

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
        user = query(User).
        self.logged_in.emit()

    def gotoregister(self, event):
        self.register_dialog = RegisterDialog()
        self.register_dialog.resize(383, 299)
        self.stackwidget = qtw.QStackedWidget()
        self.stackwidget.addWidget(self.register_dialog)
        # self.stackwidget.addWidget(self)
        # self.vlayout = qtw.QVBoxLayout(self)
        # self.vlayout.addLayout(self.ui.gridLayout)
        self.ui.gridLayout.addWidget(self.stackwidget)
        # self.setLayout(self.vlayout)
        self.stackwidget.show()
        self.stackwidget.setCurrentIndex(2)


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


class EmployeeWidget(qtw.QWidget):
    def __init__(self, side=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_EmployeeWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        if side:
            self.ui.submitButton.hide()
            self.setWindowModality(qtc.Qt.ApplicationModal)
