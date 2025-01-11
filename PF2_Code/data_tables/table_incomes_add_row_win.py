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
from ui_qt.ui_add_row_income import Ui_Win_Add_Row_Income
from util import getMonthName

# ===========================================================================================


# New window
class Win_Add_Row_Income(QtWidgets.QDialog, Ui_Win_Add_Row_Income):
    def __init__(self, incomeYear, incomeMonth, callback, parent=None):
        super(Win_Add_Row_Income, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        # set focus to Cat field
        self.buttonBox.setFocus()

        self.rowAdded = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        self.incomeYear = incomeYear
        self.incomeMonth = incomeMonth

        monthName = getMonthName(self.incomeMonth)
        incomeLabel = (
            "New Income Row for " + str(monthName) + " " + str(incomeYear) + ":"
        )
        self.label.setText(incomeLabel)
        self.incomeSumID = self.getIncomesSumID()

        # Populate Categories combo
        self.catList = []
        self.populateCategories()

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.addRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Get IncomesSumID
    # ++++
    def getIncomesSumID(self):

        query = (
            "SELECT INCOMES_SUM_ID FROM INCOMES_SUM WHERE YEAR = "
            + str(self.incomeYear)
            + " AND MONTH = "
            + str(self.incomeMonth)
        )
        data = self.db.getData(query)
        value = data.fetchone()
        incomeSumID = value[0]

        return incomeSumID

    # +++++++++++++++++++++++++++
    # Populate Categories combo
    # ++++
    def populateCategories(self):

        query = "SELECT INC_CATEGORY_ID, INC_CATEGORY FROM REG_INCOME_CATEGORIES ORDER BY INC_CATEGORY_ID"
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

        income = str(self.lineEdit_Income.text())
        notes = str(self.lineEdit_Description.text())
        amount = str(self.lineEdit_Amount.text())

        insert_stmt = (
            "INSERT INTO INCOMES (INCOMES_SUM_ID, INC_CATEGORY_ID, INCOME, NOTES, AMOUNT_ALL, AMOUNT_OPEN) VALUES ("
            + str(self.incomeSumID)
            + ", "
            + str(catID)
            + ", '"
            + income
            + "', '"
            + notes
            + "', "
            + amount
            + " , "
            + amount
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
