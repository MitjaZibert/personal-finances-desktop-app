# Form implementation generated from reading ui file '\Users\mitja\Programiranje\PF2\ui_qt\ui_add_row.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from importlib.resources import path
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Win_Add_Row(object):
    def setupUi(self, Win_Add_Row):
        Win_Add_Row.setObjectName("Win_Add_Row")
        Win_Add_Row.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Win_Add_Row)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(parent=Win_Add_Row)
        self.label.setGeometry(QtCore.QRect(110, 50, 63, 20))
        self.label.setObjectName("label")

        self.retranslateUi(Win_Add_Row)
        self.buttonBox.accepted.connect(Win_Add_Row.accept) # type: ignore
        self.buttonBox.rejected.connect(Win_Add_Row.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Win_Add_Row)

    def retranslateUi(self, Win_Add_Row):
        _translate = QtCore.QCoreApplication.translate
        Win_Add_Row.setWindowTitle(_translate("Win_Add_Row", "Dialog"))
        self.label.setText(_translate("Win_Add_Row", "TextLabel"))

