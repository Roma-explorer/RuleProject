# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TaskWidget(object):
    def setupUi(self, TaskWidget):
        TaskWidget.setObjectName("TaskWidget")
        TaskWidget.resize(722, 71)
        self.gridLayout = QtWidgets.QGridLayout(TaskWidget)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.status_box = QtWidgets.QComboBox(TaskWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy)
        self.status_box.setObjectName("status_box")
        self.gridLayout.addWidget(self.status_box, 1, 1, 1, 1)
        self.time = QtWidgets.QLabel(TaskWidget)
        self.time.setObjectName("time")
        self.gridLayout.addWidget(self.time, 1, 3, 1, 1)
        self.task_name = QtWidgets.QLabel(TaskWidget)
        self.task_name.setObjectName("task_name")
        self.gridLayout.addWidget(self.task_name, 0, 0, 1, 3)
        self.priority_box = QtWidgets.QComboBox(TaskWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.priority_box.sizePolicy().hasHeightForWidth())
        self.priority_box.setSizePolicy(sizePolicy)
        self.priority_box.setObjectName("priority_box")
        self.gridLayout.addWidget(self.priority_box, 1, 0, 1, 1)
        self.executor = QtWidgets.QLabel(TaskWidget)
        self.executor.setObjectName("executor")
        self.gridLayout.addWidget(self.executor, 1, 2, 1, 1)
        self.dedicatedhours_box = QtWidgets.QSpinBox(TaskWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dedicatedhours_box.sizePolicy().hasHeightForWidth())
        self.dedicatedhours_box.setSizePolicy(sizePolicy)
        self.dedicatedhours_box.setMinimumSize(QtCore.QSize(40, 0))
        self.dedicatedhours_box.setWrapping(False)
        self.dedicatedhours_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dedicatedhours_box.setAccelerated(False)
        self.dedicatedhours_box.setProperty("showGroupSeparator", False)
        self.dedicatedhours_box.setMinimum(0)
        self.dedicatedhours_box.setMaximum(1000)
        self.dedicatedhours_box.setProperty("value", 0)
        self.dedicatedhours_box.setObjectName("dedicatedhours_box")
        self.gridLayout.addWidget(self.dedicatedhours_box, 1, 4, 1, 1)

        self.retranslateUi(TaskWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskWidget)

    def retranslateUi(self, TaskWidget):
        _translate = QtCore.QCoreApplication.translate
        TaskWidget.setWindowTitle(_translate("TaskWidget", "Form"))
        self.time.setText(_translate("TaskWidget", "TextLabel"))
        self.task_name.setText(_translate("TaskWidget", "TextLabel"))
        self.executor.setText(_translate("TaskWidget", "TextLabel"))
