from PyQt5 import QtGui
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from views.manage_enter import HolderWidget

if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = HolderWidget()
    widget.show()

    app.exec_()
