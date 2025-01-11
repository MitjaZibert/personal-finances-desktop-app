# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6 import QtWidgets

# App Specific libraries
import globals
from data_modules import DB_Util
from ui_qt.ui_add_row_reg_expense import Ui_Win_Add_Row_Reg_Expense

# ===========================================================================================


# New window
class Win_Add_Row_Reg_Expense(QtWidgets.QDialog, Ui_Win_Add_Row_Reg_Expense):
    def __init__(self, callback, parent=None):
        super(Win_Add_Row_Reg_Expense, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        # set focus to Cat field
        self.buttonBox.setFocus()

        self.rowAdded = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        self.catList = []
        self.populateCombobox()

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.addRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Populate Expense Categories Combobox
    # ++++
    def populateCombobox(self):

        query = "SELECT EXP_CATEGORY_ID, EXP_CATEGORY FROM REG_EXPENSE_CATEGORIES ORDER BY EXP_CATEGORY_ID"
        cur = self.db.getData(query)

        self.catList = []
        for data in cur:
            catDict = {data[0]: str(data[1])}
            self.catList.append(catDict)

        for cat in self.catList:
            for key, val in cat.items():
                self.comboBoxCategory.addItem(val)

    # +++++++++++++++++++++++++++
    # Add Row
    # ++++
    def addRow(self):

        def getCatID(self):
            for cat in self.catList:
                for key, val in cat.items():
                    if val == self.comboBoxCategory.currentText():
                        expCatID = key

            return expCatID

        catID = str(getCatID(self))
        reg_exp_desc = str(self.lineEdit_Description.text())
        reg_exp_amount = self.lineEdit_Amount.text()
        reg_exp_months = self.lineEdit_Months.text()

        insert_stmt = (
            "INSERT INTO REG_REGULAR_EXPENSES (EXP_CATEGORY_ID, REGULAR_EXPENSE, AMOUNT, MONTHS) VALUES ('"
            + catID
            + "', '"
            + reg_exp_desc
            + "', '"
            + reg_exp_amount
            + "', '"
            + reg_exp_months
            + "')"
        )

        # if DML statement is generated, do DB update
        if insert_stmt:
            self.db.executeDDL(insert_stmt)
            self.db.saveData()
            self.rowAdded = True

        self.closeWin()

    # +++++++++++++++++++++++++++
    # Close Window
    # ++++
    def closeWin(self):

        self.callback(self.rowAdded)
        self.close()


# *********************************************************************************************
# *********************************************************************************************
# NOTES
# *********************************************************************************************
