# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6.QtWidgets import QDialog

# App Specific libraries
import globals
from data_modules import DB_Util
from ui_qt.ui_add_row_allocation import Ui_Win_Add_Row_Allocation

# ===========================================================================================


# New window
class Win_Add_Row_Allocation(QDialog, Ui_Win_Add_Row_Allocation):
    def __init__(self, callback, parent=None):
        super(Win_Add_Row_Allocation, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        # set focus to Cat field
        self.buttonBox.setFocus()

        self.rowAdded = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        # Populate Currencies combo
        self.currList = []
        self.populateCurrencies()

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.addRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Populate Currencies combo
    # ++++
    def populateCurrencies(self):

        query = (
            "SELECT CURR_ID, CURR_CODE, CURR_RATE FROM REG_CURRENCY ORDER BY CURR_CODE"
        )
        data_curr = self.db.getData(query)

        for row in data_curr:
            currRow = [row[0], row[1], row[2]]
            self.currList.append(currRow)

        for curr in self.currList:
            self.comboBox_Currency.addItem(curr[1])

    # +++++++++++++++++++++++++++
    # Add Row
    # ++++
    def addRow(self):

        def getID(self):
            query = "SELECT MAX(ALLOC_ID) FROM MONEY_ALLOCATION"
            data = self.db.getData(query)
            id = data.fetchone()
            new_id = int(id[0])

            new_id += 1
            return new_id

        for data in self.currList:
            if data[1] == self.comboBox_Currency.currentText():
                currID = data[0]
                currRate = data[2]

        allocID = str(getID(self))
        alloc = str(self.lineEdit_Allocation.text())
        currID = str(currID)
        description = str(self.lineEdit_Description.text())
        amount = str(self.lineEdit_Amount.text())
        value = str(float(self.lineEdit_Amount.text()) / currRate)
        available = "Y"

        insert_stmt = (
            "INSERT INTO MONEY_ALLOCATION (ALLOC_ID, ALLOCATION, ALLOC_AMOUNT, CURR_ID, VALUE, ALLOC_DESC, AVAILABLE) VALUES ("
            + allocID
            + ", '"
            + alloc
            + "', "
            + amount
            + ", "
            + currID
            + ", "
            + value
            + ", '"
            + description
            + "', '"
            + available
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
