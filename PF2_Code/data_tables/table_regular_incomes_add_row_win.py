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
from ui_qt.ui_add_row_reg_income import Ui_Win_Add_Row_Reg_Income

# ===========================================================================================


# New window
class Win_Add_Row_Reg_Income(QtWidgets.QDialog, Ui_Win_Add_Row_Reg_Income):
    def __init__(self, callback, parent=None):
        super(Win_Add_Row_Reg_Income, self).__init__(parent)

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
    # Populate Income Categories Combobox
    # ++++
    def populateCombobox(self):

        query = "SELECT INC_CATEGORY_ID, INC_CATEGORY FROM REG_INCOME_CATEGORIES ORDER BY INC_CATEGORY_ID"
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
        reg_inc_desc = str(self.lineEdit_Description.text())
        reg_inc_amount = self.lineEdit_Amount.text()

        insert_stmt = (
            "INSERT INTO REG_REGULAR_INCOMES (INC_CATEGORY_ID, REGULAR_INCOME, AMOUNT) VALUES ('"
            + catID
            + "', '"
            + reg_inc_desc
            + "', '"
            + reg_inc_amount
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
