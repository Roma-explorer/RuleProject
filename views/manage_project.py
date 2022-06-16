from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from db import session
from db.models import Status, Priority, Task, Employee, Mistake, Feature, Description, Reason
from views import consts
from views.utils import *

from windows.project_widget import Ui_SumProjectWidget
from windows.short_member import Ui_ShortMemberWidget
from windows.main_window import Ui_MainWindow
from windows.tasks_widget import Ui_TasksViewWidget
from windows.task_widget import Ui_TaskWidget
from windows.createtask_window import Ui_CreateTaskWindow


class MainWindow(qtw.QMainWindow):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project
        self.employee = consts.employee

        self.ui.project_name.setText(self.project.name)
        self.ui.emp_name.setText(self.employee.surname + ' ' + self.employee.name + ' ' + self.employee.lastname)

        self.ui.sum_project = SumProjectWidget(self.project)
        self.ui.stackedWidget.insertWidget(0, self.ui.sum_project)

        self.ui.sum_project = TasksViewWidget()
        self.ui.stackedWidget.insertWidget(1, self.ui.sum_project)

        # self.ui.tasks = TasksViewWidget()
        # self.ui.stackedWidget.insertWidget(1, self.ui.sum_project)
        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.welcome.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.tasks.clicked.connect(lambda x: self.ui.stackedWidget.setCurrentIndex(1))


class SumProjectWidget(qtw.QWidget):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_SumProjectWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project

        self.ui.description_editor.setPlainText(self.project.description)

        self.ui.mvlayout = qtw.QVBoxLayout()
        self.ui.tvlayout = qtw.QVBoxLayout()

        self.ui.mslayout = qtw.QVBoxLayout()
        self.ui.tslayout = qtw.QVBoxLayout()

        self.ui.mslayout.addWidget(qtw.QLabel(text='Автор проекта'))
        self.head = self.project.head
        self.whead = ShortMemberWidget(self.head)
        # self.author.member_clicked.connect(self.show_member)
        self.ui.mslayout.addWidget(self.whead)
        self.ui.mslayout.addWidget(qtw.QLabel(text='Заказчик'))
        self.client = self.project.contract.client
        self.wclient = ShortMemberWidget(self.client)
        # self.client.member_clicked.connect(self.show_member)
        self.ui.mslayout.addWidget(self.wclient)
        self.ui.mslayout.addWidget(qtw.QLabel(text='Команда'))

        for empproject in self.project.employees:
            self.wmember = ShortMemberWidget(empproject.employees)
            # self.member.member_clicked.connect(self.show_member)
            self.ui.mslayout.addWidget(self.wmember)

        for feature in self.project.features:
            for task in feature.tasks:
                self.ui.tslayout.addWidget(qtw.QLabel(text=task.name))
            for bug in feature.mistakes:
                self.ui.tslayout.addWidget(qtw.QLabel(text=bug.name))


        self.ui.members_group.setLayout(self.ui.mvlayout)
        self.ui.tasks_group.setLayout(self.ui.tvlayout)

        self.ui.members_content.setLayout(self.ui.mslayout)
        self.ui.tasks_content.setLayout(self.ui.tslayout)

    # def show_member(self):
    #     self.vlayout = qtw.QVBoxLayout()
    #     self.emp_widget = EmployeeWidget(side=True)
    #     self.vlayout.addWidget(self.emp_widget)
    #     # self.ui.side_info.setMinimumHeight(self.emp_widget.height())
    #     self.ui.side_info.setLayout(self.vlayout)


class ShortMemberWidget(qtw.QWidget):

    # member_clicked = qtc.pyqtSignal()

    def __init__(self, member, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ShortMemberWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.name = member.name
        self.ui.email = member.email

        # self.ui.name.mousePressEvent = self.name_clicked

    def name_clicked(self, event):
        print("Member clicked")
        self.member_clicked.emit()


class TasksViewWidget(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_TasksViewWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.status_box.addItems(['Все'] + [s.value for s in Status])
        self.ui.priority_box.addItems(['Все'] + [s.value for s in Priority])

        members = []
        for member in consts.project.employees:
            members.append(member.employees)

        self.ui.member_box.addItems(['Все'] + members)

    def show_candidates(self, tasks, wlist):
        for task in tasks:
            self.add_candidate(task, wlist)

    def filter_candidates(self):
        self.ui.tasks_list.clear()
        member = self.ui.member_box.currentText()

        if member == 'Все':
            tasks = session.query(Task)
            bugs = session.query(Mistake)
        else:
            member_id = session.query(Employee.id).filter_by(name=member)
            tasks = session.query(Task).filter_by(employee_id=member_id)
            bugs = session.query(Mistake).filter_by(employee_id=member_id)

        status = self.ui.status_box.currentText()
        if status != 'Все':
            status = Status(status)
            tasks = tasks.filter_by(status=status)
            bugs = tasks.filter_by(status=status)

        priority = self.ui.priority_box.currrentText()
        if priority != 'Все':
            priority = Priority(status)
            tasks = tasks.filter_by(status=priority)
            bugs = tasks.filter_by(status=priority)

        all_tasks = list(tasks.all()) + list(bugs.all())
        self.show_candidates(all_tasks, self.ui.tasks_list)

    def add_candidate(self, candidate, *wlist):
        if not wlist:
            wlist = self.ui.tasks_list
        else:
            wlist = wlist[0]

        tw = TaskWidget(candidate)
        item = qtw.QListWidgetItem()
        widgetLayout = qtw.QHBoxLayout()
        widgetLayout.addStretch()
        widgetLayout.setSizeConstraint(qtw.QLayout.SetMaximumSize)
        tw.setLayout(widgetLayout)
        tw.is_accepted.connect(self.show_accepted)
        hint = tw.sizeHint()
        hint.setHeight(tw.size().height())
        item.setSizeHint(hint)

        wlist.addItem(item)
        wlist.setItemWidget(item, tw)


class TaskWidget(qtw.QWidget):
    def __init__(self, task, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_TaskWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.ui.status_box.addItems([s.value for s in Status])
        self.ui.priority_box.addItems([s.value for s in Priority])

        self.ui.status_box.setCurrentText(task.status.value)
        self.ui.priority_box.setCurrentText(task.priority.value)
        self.ui.task_name.setText(task.name)
        self.ui.executor.setText(task.employee.name)
        self.ui.time.setText(task.planned_hours)


class CreateTask(qtw.QWidget):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_CreateTaskWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project

        self.ui.priority_box.addItems([s.value for s in Priority])

        members = []
        for member in consts.project.employees:
            emp = member.employees
            name = ' '.join([emp.surname, emp.name])
            members.append(name)

        self.ui.member_box.addItems(members)

        self.ui.type_box.currentTextChanged.connect(self.type_modify)
        self.ui.submitButton.clicked.connect(self.add_task)

    def type_modify(self):
        if self.ui.type_box.currentText() != 'Баг':
            self.ui.lreason.hide()
            self.ui.reason.hide()
        else:
            self.ui.lreason.show()
            self.ui.reason.show()

        if self.ui.type_box.currentText() == 'Функционал':
            self.ui.ladd_to.hide()
            self.ui.feature_box.hide()
        else:
            self.ui.ladd_to.show()
            self.ui.feature_box.show()
            self.ui.feature_box.addItems([f for f in session.query(Feature.name).all()])

    def add_task(self):
        self.name = self.ui.name.text()
        self.date_start = self.ui.date_start.date().toPyDate()
        self.date_end = self.ui.date_end.date().toPyDate()
        self.type = self.ui.type_box.currentText()
        self.priority = self.ui.priority_box.currentText()
        self.status = self.ui.status_box.currentText()
        self.planned_hours = self.ui.planned_hours.value()
        self.description = self.ui.description.toPlainText()
        self.member = self.ui.member_box.currentText()
        surname, name = self.member.split(' ')
        self.member = session.query(Employee).filter_by(surname=surname).filter_by(name=name).all()[0]

        if '' in [self.name, self.description, self.status, self.member]:
            not_all_filled()
            return
        else:
            self.description = Description(text=self.description)
            session.add(self.description)
            session.commit()
            if self.type == 'Задача':
                self.feature = self.ui.feature_box.currentText()
                self.feature = session.query(Feature).filter_by(name=self.feature)
                self.task = Task(name=self.name, date_start=self.date_start, date_end=self.date_end,
                                 description_id=self.description.id, status=Status(self.status),
                                 planned_hours=self.planned_hours, employee_id=self.member.id,
                                 priority=Priority(self.priority), feature_id=self.feature.id)
                session.add(self.task)
                session.commit()
            elif self.type == 'Баг':
                self.feature = self.ui.feature_box.currentText()
                self.feature = session.query(Feature).filter_by(name=self.feature)
                self.reason = self.ui.reason.toPlainText()
                self.reason = Reason(text=self.reason)
                self.bug = Mistake(name=self.name, date_start=self.date_start, date_end=self.date_end,
                                   description_id=self.description.id, status=Status(self.status),
                                   planned_hours=self.planned_hours, employee_id=self.member.id,
                                   priority=Priority(self.priority), feature_id=self.feature.id,
                                   reason_id=self.reason.id)
                session.add(self.bug)
                session.commit()
            elif self.type == 'Функционал':
                self.feature = Feature(name=self.name, date_start=self.date_start, date_end=self.date_end,
                                       description_id=self.description.id, status=Status(self.status),
                                       planned_hours=self.planned_hours, employee_id=self.member.id,
                                       priority=Priority(self.priority), project_id=self.project.id)
                session.add(self.feature)
                session.commit()
            self.close()


if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = MainWindow()
    widget.show()

    app.exec_()
