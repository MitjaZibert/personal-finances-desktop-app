# Form implementation generated from reading ui file '\Users\mitja\Programiranje\PF2\ui_qt\ui_delete_row.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from importlib.resources import path
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Win_Delete_Row(object):
    def setupUi(self, Win_Delete_Row):
        Win_Delete_Row.setObjectName("Win_Delete_Row")
        Win_Delete_Row.resize(523, 251)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Win_Delete_Row)
        self.buttonBox.setGeometry(QtCore.QRect(150, 200, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelConfirmation = QtWidgets.QLabel(parent=Win_Delete_Row)
        self.labelConfirmation.setGeometry(QtCore.QRect(30, 30, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelConfirmation.setFont(font)
        self.labelConfirmation.setObjectName("labelConfirmation")
        self.label_Value1 = QtWidgets.QLabel(parent=Win_Delete_Row)
        self.label_Value1.setGeometry(QtCore.QRect(50, 80, 441, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_Value1.setFont(font)
        self.label_Value1.setObjectName("label_Value1")
        self.label_Value2 = QtWidgets.QLabel(parent=Win_Delete_Row)
        self.label_Value2.setGeometry(QtCore.QRect(50, 110, 441, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_Value2.setFont(font)
        self.label_Value2.setObjectName("label_Value2")
        self.label_Value3 = QtWidgets.QLabel(parent=Win_Delete_Row)
        self.label_Value3.setGeometry(QtCore.QRect(50, 140, 441, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_Value3.setFont(font)
        self.label_Value3.setObjectName("label_Value3")

        self.retranslateUi(Win_Delete_Row)
        self.buttonBox.accepted.connect(Win_Delete_Row.accept) # type: ignore
        self.buttonBox.rejected.connect(Win_Delete_Row.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Win_Delete_Row)

    def retranslateUi(self, Win_Delete_Row):
        _translate = QtCore.QCoreApplication.translate
        Win_Delete_Row.setWindowTitle(_translate("Win_Delete_Row", "Dialog"))
        self.labelConfirmation.setText(_translate("Win_Delete_Row", "Do you really want to delete the following row:"))
        self.label_Value1.setText(_translate("Win_Delete_Row", "Val1"))
        self.label_Value2.setText(_translate("Win_Delete_Row", "Val2"))
        self.label_Value3.setText(_translate("Win_Delete_Row", "Val3"))

