# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tasks_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TasksViewWidget(object):
    def setupUi(self, TasksViewWidget):
        TasksViewWidget.setObjectName("TasksViewWidget")
        TasksViewWidget.resize(1043, 346)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(TasksViewWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(TasksViewWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.member_box = QtWidgets.QComboBox(TasksViewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.member_box.sizePolicy().hasHeightForWidth())
        self.member_box.setSizePolicy(sizePolicy)
        self.member_box.setObjectName("member_box")
        self.horizontalLayout.addWidget(self.member_box)
        self.label_2 = QtWidgets.QLabel(TasksViewWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.priority_box = QtWidgets.QComboBox(TasksViewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.priority_box.sizePolicy().hasHeightForWidth())
        self.priority_box.setSizePolicy(sizePolicy)
        self.priority_box.setObjectName("priority_box")
        self.horizontalLayout.addWidget(self.priority_box)
        self.label_3 = QtWidgets.QLabel(TasksViewWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.status_box = QtWidgets.QComboBox(TasksViewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy)
        self.status_box.setObjectName("status_box")
        self.horizontalLayout.addWidget(self.status_box)
        self.add_button = QtWidgets.QPushButton(TasksViewWidget)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tasks_list = QtWidgets.QListWidget(TasksViewWidget)
        self.tasks_list.setObjectName("tasks_list")
        self.verticalLayout.addWidget(self.tasks_list)
        self.add_task = QtWidgets.QPushButton(TasksViewWidget)
        self.add_task.setObjectName("add_task")
        self.verticalLayout.addWidget(self.add_task)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.side_info = QtWidgets.QFrame(TasksViewWidget)
        self.side_info.setMinimumSize(QtCore.QSize(317, 0))
        self.side_info.setMaximumSize(QtCore.QSize(317, 16777215))
        self.side_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_info.setObjectName("side_info")
        self.horizontalLayout_2.addWidget(self.side_info)

        self.retranslateUi(TasksViewWidget)
        QtCore.QMetaObject.connectSlotsByName(TasksViewWidget)

    def retranslateUi(self, TasksViewWidget):
        _translate = QtCore.QCoreApplication.translate
        TasksViewWidget.setWindowTitle(_translate("TasksViewWidget", "Form"))
        self.label.setText(_translate("TasksViewWidget", "Исполнитель"))
        self.label_2.setText(_translate("TasksViewWidget", "Приоритет"))
        self.label_3.setText(_translate("TasksViewWidget", "Состояние"))
        self.add_button.setText(_translate("TasksViewWidget", "Добавить"))
        self.add_task.setText(_translate("TasksViewWidget", "Добавить задачу"))