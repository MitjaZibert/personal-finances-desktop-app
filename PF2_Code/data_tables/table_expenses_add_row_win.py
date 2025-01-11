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
from ui_qt.ui_add_row_expense import Ui_Win_Add_Row_Expense
from util import getMonthName

# ===========================================================================================


# New window
class Win_Add_Row_Expense(QtWidgets.QDialog, Ui_Win_Add_Row_Expense):
    def __init__(self, expenseYear, expenseMonth, callback, parent=None):
        super(Win_Add_Row_Expense, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        # set focus to Cat field
        self.buttonBox.setFocus()

        self.rowAdded = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        self.expenseYear = expenseYear
        self.expenseMonth = expenseMonth

        monthName = getMonthName(self.expenseMonth)
        expenseLabel = (
            "New Expense Row for " + str(monthName) + " " + str(expenseYear) + ":"
        )
        self.label.setText(expenseLabel)
        self.expenseSumID = self.getExpenseSumID()

        # Populate Categories combo
        self.catList = []
        self.populateCategories()

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.addRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Get ExpenseSumID
    # ++++
    def getExpenseSumID(self):

        query = (
            "SELECT EXPENSES_SUM_ID FROM EXPENSES_SUM WHERE YEAR = "
            + str(self.expenseYear)
            + " AND MONTH = "
            + str(self.expenseMonth)
        )
        data = self.db.getData(query)
        value = data.fetchone()
        expenseSumID = value[0]

        return expenseSumID

    # +++++++++++++++++++++++++++
    # Populate Categories combo
    # ++++
    def populateCategories(self):

        query = "SELECT EXP_CATEGORY_ID, EXP_CATEGORY FROM REG_EXPENSE_CATEGORIES ORDER BY EXP_CATEGORY_ID"
        data_cat = self.db.getData(query)

        for row in data_cat:
            catRow = [row[0], row[1]]
            self.catList.append(catRow)

        for curr in self.catList:
            self.comboBox_Category.addItem(curr[1])

    # +++++++++++++++++++++++++++
    # Add Row
    # ++++
    def addRow(self):

        for data in self.catList:
            if data[1] == self.comboBox_Category.currentText():
                catID = data[0]

        expense = str(self.lineEdit_Expense.text())
        notes = str(self.lineEdit_Description.text())
        amount = str(self.lineEdit_Amount.text())

        insert_stmt = (
            "INSERT INTO EXPENSES (EXPENSES_SUM_ID, EXP_CATEGORY_ID, EXPENSE, NOTES, AMOUNT_ALL, AMOUNT_OPEN) VALUES ("
            + str(self.expenseSumID)
            + ", "
            + str(catID)
            + ", '"
            + expense
            + "', '"
            + notes
            + "', "
            + str(amount)
            + " , "
            + str(amount)
            + ")"
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
