# Form implementation generated from reading ui file '\Users\mitja\Programiranje\PF2\ui_qt\ui_add_row_expense.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from importlib.resources import path
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Win_Add_Row_Expense(object):
    def setupUi(self, Win_Add_Row_Expense):
        Win_Add_Row_Expense.setObjectName("Win_Add_Row_Expense")
        Win_Add_Row_Expense.resize(603, 302)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Win_Add_Row_Expense)
        self.buttonBox.setGeometry(QtCore.QRect(240, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(parent=Win_Add_Row_Expense)
        self.label.setGeometry(QtCore.QRect(30, 20, 511, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox_Category = QtWidgets.QComboBox(parent=Win_Add_Row_Expense)
        self.comboBox_Category.setGeometry(QtCore.QRect(150, 70, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_Category.setFont(font)
        self.comboBox_Category.setObjectName("comboBox_Category")
        self.label_2 = QtWidgets.QLabel(parent=Win_Add_Row_Expense)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Win_Add_Row_Expense)
        self.label_3.setGeometry(QtCore.QRect(30, 109, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=Win_Add_Row_Expense)
        self.label_4.setGeometry(QtCore.QRect(20, 189, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=Win_Add_Row_Expense)
        self.label_5.setGeometry(QtCore.QRect(20, 150, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.lineEdit_Expense = QtWidgets.QLineEdit(parent=Win_Add_Row_Expense)
        self.lineEdit_Expense.setGeometry(QtCore.QRect(150, 110, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Expense.setFont(font)
        self.lineEdit_Expense.setObjectName("lineEdit_Expense")
        self.lineEdit_Description = QtWidgets.QLineEdit(parent=Win_Add_Row_Expense)
        self.lineEdit_Description.setGeometry(QtCore.QRect(150, 150, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Description.setFont(font)
        self.lineEdit_Description.setObjectName("lineEdit_Description")
        self.lineEdit_Amount = QtWidgets.QLineEdit(parent=Win_Add_Row_Expense)
        self.lineEdit_Amount.setGeometry(QtCore.QRect(150, 190, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Amount.setFont(font)
        self.lineEdit_Amount.setObjectName("lineEdit_Amount")

        self.retranslateUi(Win_Add_Row_Expense)
        self.buttonBox.accepted.connect(Win_Add_Row_Expense.accept) # type: ignore
        self.buttonBox.rejected.connect(Win_Add_Row_Expense.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Win_Add_Row_Expense)

    def retranslateUi(self, Win_Add_Row_Expense):
        _translate = QtCore.QCoreApplication.translate
        Win_Add_Row_Expense.setWindowTitle(_translate("Win_Add_Row_Expense", "Dialog"))
        self.label.setText(_translate("Win_Add_Row_Expense", "New Expense Row for YEAR / MONTH"))
        self.label_2.setText(_translate("Win_Add_Row_Expense", "Category:"))
        self.label_3.setText(_translate("Win_Add_Row_Expense", "Expense:"))
        self.label_4.setText(_translate("Win_Add_Row_Expense", "Amount:"))
        self.label_5.setText(_translate("Win_Add_Row_Expense", "Note:"))

