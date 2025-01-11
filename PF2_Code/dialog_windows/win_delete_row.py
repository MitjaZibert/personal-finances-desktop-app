# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6 import QtWidgets

# App Specific libraries
from data_modules import DB_Util
from ui_qt.ui_delete_row import Ui_Win_Delete_Row

# ===========================================================================================


# New window
class Win_Delete_Row(QtWidgets.QDialog, Ui_Win_Delete_Row):
    def __init__(self, table, rowData, callback, parent=None):
        super(Win_Delete_Row, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        self.rowID = str(rowData[0])

        # Labels on Delete Row Window

        self.label_Value1.setText("")
        self.label_Value2.setText("")
        self.label_Value3.setText("")

        if len(rowData) >= 2:
            self.label_Value1.setText(str(rowData[1]))

        if len(rowData) >= 3:
            self.label_Value2.setText(str(rowData[2]))

        if len(rowData) >= 4:
            self.label_Value3.setText(str(rowData[3]))

        # set focus to Cat field
        self.buttonBox.setFocus()

        self.rowDeleted = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        self.table = table

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.deleteRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Delete Row
    # ++++
    def deleteRow(self):

        delete_stmt = None

        if self.table == "Allocation":
            delete_stmt = "DELETE FROM MONEY_ALLOCATION WHERE ALLOC_ID = " + str(
                self.rowID
            )

        if self.table == "Incomes":
            delete_stmt = "DELETE FROM INCOMES WHERE INCOME_ID = " + str(self.rowID)

        if self.table == "Expenses":
            delete_stmt = "DELETE FROM EXPENSES WHERE EXPENSE_ID = " + str(self.rowID)

        if self.table == "Cat_Incomes":
            delete_stmt = (
                "DELETE FROM REG_INCOME_CATEGORIES WHERE INC_CATEGORY_ID = "
                + str(self.rowID)
            )

        if self.table == "Cat_Expenses":
            delete_stmt = (
                "DELETE FROM REG_EXPENSE_CATEGORIES WHERE EXP_CATEGORY_ID = "
                + str(self.rowID)
            )

        if self.table == "Regular_Incomes":
            delete_stmt = (
                "DELETE FROM REG_REGULAR_INCOMES WHERE REGULAR_INCOME_ID = "
                + str(self.rowID)
            )

        if self.table == "Regular_Expenses":
            delete_stmt = (
                "DELETE FROM REG_REGULAR_EXPENSES WHERE REGULAR_EXPENSE_ID = "
                + str(self.rowID)
            )

        if self.table == "Currencies":
            delete_stmt = (
                "DELETE FROM REG_CURRENCY WHERE CURR_ID = "
                + str(self.rowID)
            )

        # if DML statement is generated, do DB update
        if delete_stmt:
            self.db.executeDDL(delete_stmt)
            self.db.saveData()
            self.rowDeleted = True

        self.closeWin()

    # +++++++++++++++++++++++++++
    # Close Window
    # ++++
    def closeWin(self):

        self.callback(self.rowDeleted)
        self.close()


# *********************************************************************************************
# *********************************************************************************************
# NOTES
# *********************************************************************************************
