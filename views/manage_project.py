from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from windows.project_widget import Ui_SumProjectWidget
from windows.short_member import Ui_ShortMemberWidget
from windows.main_window import Ui_MainWindow

from manage_enter import EmployeeWidget


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.sum_project = SumProjectWidget()
        self.ui.stackedWidget.insertWidget(0, self.ui.sum_project)
        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.welcome.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(0))


class SumProjectWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_SumProjectWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.mvlayout = qtw.QVBoxLayout()
        self.ui.tvlayout = qtw.QVBoxLayout()

        self.ui.mslayout = qtw.QVBoxLayout()
        self.ui.tslayout = qtw.QVBoxLayout()

        self.ui.mslayout.addWidget(qtw.QLabel(text='Автор проекта'))
        self.author = ShortMemberWidget()
        self.author.member_clicked.connect(self.show_member)
        self.ui.mslayout.addWidget(self.author)
        self.ui.mslayout.addWidget(qtw.QLabel(text='Заказчик'))
        self.client = ShortMemberWidget()
        self.client.member_clicked.connect(self.show_member)
        self.ui.mslayout.addWidget(self.client)
        self.ui.mslayout.addWidget(qtw.QLabel(text='Команда'))

        for i in range(5):
            self.member = ShortMemberWidget()
            self.member.member_clicked.connect(self.show_member)
            self.ui.mslayout.addWidget(self.member)
            self.ui.tslayout.addWidget(qtw.QLabel(text=f'task {i}'))

        self.ui.members_group.setLayout(self.ui.mvlayout)
        self.ui.tasks_group.setLayout(self.ui.tvlayout)

        self.ui.members_content.setLayout(self.ui.mslayout)
        self.ui.tasks_content.setLayout(self.ui.tslayout)

    def show_member(self):
        self.vlayout = qtw.QVBoxLayout()
        self.emp_widget = EmployeeWidget(side=True)
        self.vlayout.addWidget(self.emp_widget)
        # self.ui.side_info.setMinimumHeight(self.emp_widget.height())
        self.ui.side_info.setLayout(self.vlayout)


class ShortMemberWidget(qtw.QWidget):

    member_clicked = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ShortMemberWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.name.mousePressEvent = self.name_clicked

    def name_clicked(self, event):
        print("Member clicked")
        self.member_clicked.emit()


if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = MainWindow()
    widget.show()

    app.exec_()