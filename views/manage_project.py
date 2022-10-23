from datetime import date, timedelta
from functools import partial

from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from db import session
from db.models import Status, Priority, Task, Employee, Mistake, Feature, Description, Reason, Project, EmployeeProject, \
    EmployeeProjectFeature, Base, Position, Department
from views import consts
from views.shared_widgets import EmployeeWidget
from views.side_widgets import SideTaskWidget, SideClientWidget
from views.utils import *

from windows.project_widget import Ui_SumProjectWidget
from windows.short_member import Ui_ShortMemberWidget
from windows.main_window import Ui_MainWindow
from windows.tasks_widget import Ui_TasksViewWidget
from windows.task_widget import Ui_TaskWidget
from windows.createtask_window import Ui_CreateTaskWindow
from windows.membersview_widget import Ui_MembersViewWidget
from windows.shortemployee_widget import Ui_ShortEmployeeWidget


class MainWindow(qtw.QMainWindow):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project
        self.employee = consts.employee

        self.setWindowTitle(self.project.name)

        self.ui.project_name.setText(self.project.name)
        self.ui.emp_name.setText(self.employee.surname + ' ' + self.employee.name + ' ' + self.employee.lastname)

        self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
        self.show_sumup()

        self.ui.welcome.clicked.connect(self.show_sumup)
        self.ui.tasks.clicked.connect(self.show_tasksview)
        self.ui.team.clicked.connect(self.show_membersview)

    def show_sumup(self):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())

        self.ui.sum_project = SumProjectWidget(self.project)
        self.ui.stackedWidget.addWidget(self.ui.sum_project)
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_tasksview(self):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())

        self.ui.tasks_view = TasksViewWidget(self.project)
        self.ui.stackedWidget.addWidget(self.ui.tasks_view)
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_membersview(self):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())

        self.ui.members_view = MembersViewWidget(self.project)
        self.ui.stackedWidget.addWidget(self.ui.members_view)
        self.ui.stackedWidget.setCurrentIndex(0)


class SumProjectWidget(qtw.QWidget):
    def __init__(self, project: Project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_SumProjectWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project

        self.ui.description_editor.setPlainText(self.project.description)
        self.ui.startdate.setDate(self.project.date_start)
        self.ui.enddate.setDate(self.project.date_end)
        self.ui.client.hide()
        self.ui.client = ClickableLabel(text=self.project.contract.client.name)
        self.ui.gridLayout_2.addWidget(self.ui.client, 1, 1, 1, 2)
        self.ui.client.clicked.connect(self.show_client)

        self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())

        self.ui.mvlayout = qtw.QVBoxLayout()
        self.ui.tvlayout = qtw.QVBoxLayout()

        self.ui.mslayout = qtw.QVBoxLayout()
        self.ui.tslayout = qtw.QVBoxLayout()

        self.ui.mslayout.addWidget(qtw.QLabel(text='Автор проекта'))
        self.head = self.project.head
        self.whead = ShortMemberWidget(self.head)
        self.whead.member_clicked.connect(self.show_member)
        self.ui.mslayout.addWidget(self.whead)
        self.ui.mslayout.addWidget(qtw.QLabel(text='Команда'))

        for empproject in self.project.employees:
            self.wmember = ShortMemberWidget(empproject.employees)
            self.wmember.member_clicked.connect(self.show_member)
            self.ui.mslayout.addWidget(self.wmember)

        for feature in self.project.features:
            for task in feature.tasks:
                task_widget = ClickableLabel(text=task.name)
                task_widget.clicked.connect(partial(self.show_task, task))
                self.ui.tslayout.addWidget(task_widget)
            for bug in feature.mistakes:
                bug_widget = ClickableLabel(text=bug.name)
                bug_widget.clicked.connect(partial(self.show_task, bug))
                self.ui.tslayout.addWidget(bug_widget)

        self.ui.members_group.setLayout(self.ui.mvlayout)
        self.ui.tasks_group.setLayout(self.ui.tvlayout)

        self.ui.members_content.setLayout(self.ui.mslayout)
        self.ui.tasks_content.setLayout(self.ui.tslayout)

        self.ui.task_add.clicked.connect(self.add_task)
        self.ui.member_add.clicked.connect(self.add_member)

    def add_task(self):
        self.task_add_widget = CreateTask(self.project)
        self.task_add_widget.task_created.connect(self.add_task_to_tasks)
        self.task_add_widget.show()

    def add_task_to_tasks(self, *task):
        task = task[0]
        task_widget = ClickableLabel(text=task.name)
        task_widget.clicked.connect(partial(self.show_task, task))
        self.ui.tslayout.addWidget(task_widget)

    def add_member(self):
        self.memberadd_window = SelectEmployeeWindow(self.project)
        self.memberadd_window.employee_selected.connect(self.add_member_to_members)
        self.memberadd_window.show()

    def add_member_to_members(self, employee):
        self.wmember = ShortMemberWidget(employee)
        self.wmember.member_clicked.connect(self.show_member)
        self.ui.mslayout.addWidget(self.wmember)

    def show_member(self, *employee):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
        self.emp_widget = EmployeeWidget(employee[0])
        self.ui.stackedWidget.addWidget(self.emp_widget)

    def show_task(self, *task):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
        self.side_task = SideTaskWidget(task[0])
        self.ui.stackedWidget.addWidget(self.side_task)

    def show_client(self):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
        self.side_client = SideClientWidget(self.project.contract)
        self.ui.stackedWidget.addWidget(self.side_client)



class ShortMemberWidget(qtw.QWidget):

    member_clicked = qtc.pyqtSignal(Employee)

    def __init__(self, member, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ShortMemberWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.member = member

        self.ui.name.setText(" ".join([member.lastname, member.surname]))
        self.ui.mail.setText(member.email)

        self.ui.name.mousePressEvent = self.name_clicked
        self.mouseDoubleClickEvent = self.name_clicked

    def name_clicked(self, event):
        print("Member clicked")
        self.member_clicked.emit(self.member)


class TasksViewWidget(qtw.QWidget):
    def __init__(self, project: Project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_TasksViewWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project

        self.ui.status_box.addItems(['Все'] + [s.value for s in Status])
        self.ui.priority_box.addItems(['Все'] + [s.value for s in Priority])

        members = []
        for member in self.project.employees:
            emp = member.employees
            name = " ".join([emp.lastname, emp.name])
            members.append(name)

        self.ui.member_box.addItems(['Все'] + members)

        self.ui.tasks_list.setColumnCount(1)
        self.ui.tasks_list.setHeaderHidden(True)
        self.filter_features()

        self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())

        self.ui.status_box.currentTextChanged.connect(self.filter_features)
        self.ui.priority_box.currentTextChanged.connect(self.filter_features)
        self.ui.member_box.currentTextChanged.connect(self.filter_features)

        self.ui.add_button.clicked.connect(self.create_task)

    def filter_features(self):
        self.features_views = []
        self.ui.tasks_list.clear()
        features = self.project.features
        for feature in features:
            tasks = self.filter_tasks(feature)
            if tasks:
                feature_view = TaskWidget(feature)
                feature_view.task_changed.connect(self.filter_features)
                feature_view.task_clicked.connect(self.show_task)
                self.features_views.append(feature_view)
                feature_root = qtw.QTreeWidgetItem(self.ui.tasks_list)
                self.ui.tasks_list.setItemWidget(feature_root, 0, feature_view)
                self.show_tasks(tasks, feature_root, self.ui.tasks_list)
                self.ui.tasks_list.addTopLevelItem(feature_root)

    def show_tasks(self, tasks, feature_root, wlist):
        for task in tasks:
            self.add_task(task, feature_root, wlist)

    def filter_tasks(self, feature):
        member = self.ui.member_box.currentText()

        if member == 'Все':
            tasks = session.query(Task).filter_by(feature_id=feature.id)
            bugs = session.query(Mistake).filter_by(feature_id=feature.id)
        else:
            lastname, name = member.split(' ')
            member_id = session.query(Employee.id).filter_by(name=name).filter_by(lastname=lastname)
            tasks = session.query(Task).filter_by(feature_id=feature.id).filter_by(employee_id=member_id)
            bugs = session.query(Mistake).filter_by(feature_id=feature.id).filter_by(employee_id=member_id)

        status = self.ui.status_box.currentText()
        if status != 'Все':
            status = Status(status)
            tasks = tasks.filter_by(status=status)
            bugs = bugs.filter_by(status=status)

        priority = self.ui.priority_box.currentText()
        if priority != 'Все':
            priority = Priority(priority)
            tasks = tasks.filter_by(priority=priority)
            bugs = bugs.filter_by(priority=priority)

        all_tasks = list(tasks.all()) + list(bugs.all())
        return all_tasks

    def add_task(self, task, feature_root, *wlist):
        if not wlist:
            wlist = self.ui.tasks_list
        else:
            wlist = wlist[0]

        task_widget = TaskWidget(task)
        task_widget.task_changed.connect(self.filter_features)
        task_widget.task_clicked.connect(self.show_task)
        task_item = qtw.QTreeWidgetItem(feature_root)
        self.ui.tasks_list.setItemWidget(task_item, 0, task_widget)
        feature_root.addChild(task_item)

    def create_task(self):
        self.createtask_window = CreateTask(self.project)
        self.createtask_window.task_created.connect(self.add_new_task)
        self.createtask_window.show()

    def add_new_task(self, *task):
        if type(task[0]) == Feature:
            feature = task[0]
            feature_view = TaskWidget(feature)
            feature_view.task_changed.connect(self.filter_features)
            feature_view.task_clicked.connect(self.show_task)
            feature_root = qtw.QTreeWidgetItem(self.ui.tasks_list)
            self.ui.tasks_list.setItemWidget(feature_root, 0, feature_view)
            self.ui.tasks_list.addTopLevelItem(feature_root)
            self.features_views.append(feature_view)
        else:
            task = task[0]
            for index, feature_view in enumerate(self.features_views):
                if feature_view.task == task.feature:
                    self.add_task(task, self.ui.tasks_list.topLevelItem(index), self.ui.tasks_list)

    def show_task(self, *task):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
        self.side_task = SideTaskWidget(task[0])
        self.ui.stackedWidget.addWidget(self.side_task)


class TaskWidget(qtw.QWidget):

    task_changed = qtc.pyqtSignal(Base)
    task_clicked = qtc.pyqtSignal(Base)

    def __init__(self, task, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_TaskWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.task = task

        self.ui.status_box.addItems([s.value for s in Status])
        self.ui.priority_box.addItems([p.value for p in Priority])

        if type(task) != Feature:
            emp = task.employee
        else:
            emp = task.emprojfeatures[0].employee_projects.employees
        self.ui.executor.setText(" ".join([emp.lastname, emp.name]))

        self.ui.status_box.setCurrentText(task.status.value)
        self.ui.priority_box.setCurrentText(task.priority.value)
        self.ui.task_name.setText(task.name)
        self.ui.time.setText(str(task.planned_hours) + 'ч')
        self.ui.dedicatedhours_box.setValue(self.task.dedicated_hours)

        self.ui.status_box.currentTextChanged.connect(self.status_save)
        self.ui.priority_box.currentTextChanged.connect(self.priority_save)
        self.ui.dedicatedhours_box.valueChanged.connect(self.dedicated_hours_save)

        self.mouseDoubleClickEvent = self.task_pressed

    def status_save(self):
        valid = self.check_status()
        if valid:
            self.task.status = Status(self.ui.status_box.currentText())
            session.add(self.task)
            session.commit()
            self.task_changed.emit(self.task)
        else:
            self.ui.status_box.setCurrentText(self.task.status.value)

    def check_status(self):
        if type(self.task) == Feature and self.ui.status_box.currentText() == Status.closed.value:
            bugs = session.query(Mistake.status).filter_by(feature_id=self.task.id).all()
            tasks = session.query(Task.status).filter_by(feature_id=self.task.id).all()
            if any([task.status.value != Status.closed.value for task in bugs + tasks]):
                message = qtw.QMessageBox(icon=qtw.QMessageBox.Warning,
                                          text='Прежде чем завершить функционал завершите все задачи')
                message.exec_()
                return False
        return True

    def priority_save(self):
        self.task.priority = Priority(self.ui.priority_box.currentText())
        session.add(self.task)
        session.commit()
        self.task_changed.emit(self.task)

    def dedicated_hours_save(self):
        self.task.dedicated_hours = self.ui.dedicatedhours_box.value()
        session.add(self.task)
        session.commit()
        self.task_changed.emit(self.task)

    def task_pressed(self, env):
        self.task_clicked.emit(self.task)


class CreateTask(qtw.QWidget):
    task_created = qtc.pyqtSignal(Base)

    def __init__(self, project: Project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_CreateTaskWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project

        self.setWindowTitle("Создание задачи")

        self.ui.date_start.setDate(date.today())
        self.ui.date_end.setDate(date.today() + timedelta(days=1))
        self.ui.type_box.currentTextChanged.connect(self.type_modify)
        self.ui.type_box.setCurrentText("Баг")
        self.ui.type_box.setCurrentText("Функционал")

        self.ui.priority_box.addItems([p.value for p in Priority])
        self.ui.status_box.addItems([s.value for s in Status])

        self.members = []
        for member in consts.project.employees:
            emp = member.employees
            self.members.append(emp)
            name = ' '.join([emp.surname, emp.name])
            self.ui.member_box.addItem(name)

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
            if self.ui.feature_box.count() == 0:
                self.ui.feature_box.addItems([f[0] for f in session.query(Feature.name).all()])

    def add_task(self):
        self.name = self.ui.name.text()
        self.date_start = self.ui.date_start.date().toPyDate()
        self.date_end = self.ui.date_end.date().toPyDate()
        self.type = self.ui.type_box.currentText()
        self.priority = self.ui.priority_box.currentText()
        self.status = self.ui.status_box.currentText()
        self.planned_hours = self.ui.planned_hours.value()
        self.description = self.ui.description.toPlainText()
        self.member = self.ui.member_box.currentIndex()
        self.member = self.members[self.member]

        if '' in [self.name, self.description, self.status, self.member] or self.planned_hours == 0:
            not_all_filled()
            return
        else:
            self.description = Description(text=self.description)
            session.add(self.description)
            session.commit()
            if self.type == 'Задача':
                self.feature = self.ui.feature_box.currentText()
                self.feature = session.query(Feature).filter_by(name=self.feature).first()
                self.task = Task(name=self.name, date_start=self.date_start, date_end=self.date_end, dedicated_hours=0,
                                 description_id=self.description.id, status=Status(self.status),
                                 planned_hours=self.planned_hours, employee_id=self.member.id,
                                 priority=Priority(self.priority), feature_id=self.feature.id)
                session.add(self.task)
                session.commit()
                self.task_created.emit(self.task)
            elif self.type == 'Баг':
                self.feature = self.ui.feature_box.currentText()
                self.feature = session.query(Feature).filter_by(name=self.feature).first()
                self.reason = self.ui.reason.toPlainText()
                self.reason = Reason(text=self.reason)
                session.add(self.reason)
                session.commit()
                self.bug = Mistake(name=self.name, date_start=self.date_start, date_end=self.date_end, dedicated_hours=0,
                                   description_id=self.description.id, status=Status(self.status),
                                   planned_hours=self.planned_hours, employee_id=self.member.id,
                                   priority=Priority(self.priority), feature_id=self.feature.id,
                                   reason_id=self.reason.id)
                session.add(self.bug)
                session.commit()
                self.task_created.emit(self.bug)
            elif self.type == 'Функционал':
                empproj = session.query(EmployeeProject).filter_by(employee_id=self.member.id).filter_by(
                    project_id=self.project.id).all()[0]
                self.feature = Feature(name=self.name, date_start=self.date_start, date_end=self.date_end,
                                       description_id=self.description.id, status=Status(self.status),
                                       planned_hours=self.planned_hours, priority=Priority(self.priority),
                                       project_id=self.project.id, dedicated_hours=0)
                session.add(self.feature)
                session.commit()
                empprojfeature = EmployeeProjectFeature(feature_id=self.feature.id, employeeproj_id=empproj.id)
                session.add(empprojfeature)
                session.commit()
                self.task_created.emit(self.feature)
            self.close()


class MembersViewWidget(qtw.QWidget):
    def __init__(self, project: Project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MembersViewWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.project = project

        self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())

        self.positions = [pos[0] for pos in session.query(Position.name).distinct()]
        self.ui.position_box.addItems(['Все'] + self.positions)

        self.departments = [dep[0] for dep in session.query(Department.name).distinct()]
        self.ui.department_box.addItems(['Все'] + self.departments)

        self.filter_members()

        self.ui.position_box.currentTextChanged.connect(self.filter_members)
        self.ui.department_box.currentTextChanged.connect(self.filter_members)
        self.ui.add_button.clicked.connect(self.create_member)

    def create_member(self):
        self.select_member = SelectEmployeeWindow(self.project)
        self.select_member.employee_selected.connect(self.add_member)
        self.select_member.show()

    def filter_members(self):
        self.ui.members_list.clear()
        position = self.ui.position_box.currentText()
        department = self.ui.department_box.currentText()

        members = session.query(Employee).filter(Employee.id.
                                                 in_(session.query(EmployeeProject.employee_id)
                                                     .filter_by(project_id=self.project.id).distinct()))

        if position != 'Все':
            position = session.query(Position).filter_by(name=position).first()
            members = members.filter_by(position_id=position.id)

        if department != 'Все':
            department = session.query(Department).filter_by(name=department).first()
            members = members.filter_by(department_id=department.id)

        for member in members.all():
            self.add_member(member)

    def add_member(self, member):
        sew = ShortEmployeeWidget(member, info=True)
        sew.widget_clicked.connect(self.show_member)
        item = qtw.QListWidgetItem()
        widgetLayout = qtw.QHBoxLayout()
        widgetLayout.addStretch()
        widgetLayout.setSizeConstraint(qtw.QLayout.SetMaximumSize)
        sew.setLayout(widgetLayout)
        hint = sew.sizeHint()
        hint.setHeight(sew.size().height())
        item.setSizeHint(hint)

        self.ui.members_list.addItem(item)
        self.ui.members_list.setItemWidget(item, sew)

    def show_member(self, *employee):
        if self.ui.stackedWidget.currentWidget():
            self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.currentWidget())
        self.emp_widget = EmployeeWidget(employee[0])
        self.ui.stackedWidget.addWidget(self.emp_widget)


class SelectEmployeeWindow(qtw.QDialog):

    employee_selected = qtc.pyqtSignal(Employee)

    def __init__(self, project: Project, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Добавление сотрудника")
        self.project = project

        self.vlayout = qtw.QVBoxLayout()
        self.setLayout(self.vlayout)
        self.members_list = qtw.QListWidget()
        self.vlayout.addWidget(self.members_list)
        self.resize(444, 249)

        employees = session.query(Employee).filter(Employee.id.not_in(session.query(EmployeeProject.employee_id)
                                                                      .filter_by(project_id=project.id))).all()

        for employee in employees:
            self.add_employee_to_list(employee)

    def add_employee_to_list(self, employee):
        sew = ShortEmployeeWidget(employee)
        sew.empadd_clicked.connect(self.add_employee_to_project)
        item = qtw.QListWidgetItem()
        widgetLayout = qtw.QHBoxLayout()
        widgetLayout.addStretch()
        widgetLayout.setSizeConstraint(qtw.QLayout.SetMaximumSize)
        sew.setLayout(widgetLayout)
        hint = sew.sizeHint()
        hint.setHeight(sew.size().height())
        item.setSizeHint(hint)

        self.members_list.addItem(item)
        self.members_list.setItemWidget(item, sew)

    def add_employee_to_project(self, *employee):
        employee = employee[0]

        emproject = EmployeeProject(employee_id=employee.id, project_id=self.project.id)
        session.add(emproject)
        session.commit()
        self.employee_selected.emit(employee)


class ShortEmployeeWidget(qtw.QWidget):

    empadd_clicked = qtc.pyqtSignal(Employee)
    widget_clicked = qtc.pyqtSignal(Employee)

    def __init__(self, employee, info=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_ShortEmployeeWidget()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.employee = employee

        self.ui.name.mousePressEvent = self.emp_clicked
        self.mouseDoubleClickEvent = self.emp_clicked

        self.ui.name.setText(' '.join([employee.surname, employee.name]))
        self.ui.position.setText(employee.position.name)
        self.ui.department.setText(employee.department.name)

        self.ui.add_button.clicked.connect(self.employee_select)

        if info:
            self.ui.add_button.hide()

    def emp_clicked(self, event):
        print("Member clicked")
        self.widget_clicked.emit(self.employee)

    def employee_select(self):
        self.empadd_clicked.emit(self.employee)
        self.close()


class ClickableLabel(qtw.QLabel):
    clicked = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()


if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = MainWindow()
    widget.show()

    app.exec_()
