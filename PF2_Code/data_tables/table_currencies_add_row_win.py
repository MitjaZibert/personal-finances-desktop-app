# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries
from datetime import date

# PyQt6 libraries
from PyQt6 import QtWidgets

# App Specific libraries
import globals
from data_modules import DB_Util
from ui_qt.ui_add_row_reg_currency import Ui_Win_Add_Row_Reg_Currency

# ===========================================================================================


# New window
class Win_Add_Row_Reg_Currency(QtWidgets.QDialog, Ui_Win_Add_Row_Reg_Currency):
    def __init__(self, callback, parent=None):
        super(Win_Add_Row_Reg_Currency, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        # set focus to Cat field
        self.buttonBox.setFocus()

        self.rowAdded = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.addRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Add Row
    # ++++
    def addRow(self):

        currCode = str(self.lineEdit_CurrCode.text())
        currName = str(self.lineEdit_CurrName.text())
        currRate = str(self.lineEdit_CurrRate.text())
        rateDate = str(date.today())
        isCrypto = self.checkBox_IS_Crypto.isChecked()

        currIsCrypto = "0"
        if isCrypto == True:
            currIsCrypto = "2"

        insert_stmt = (
            "INSERT INTO REG_CURRENCY (CURR_CODE, CURR_NAME, CURR_RATE, RATE_DATE, CRYPTO) VALUES ('"
            + currCode
            + "', '"
            + currName
            + "', "
            + currRate
            + ", '"
            + rateDate
            + "', "
            + currIsCrypto
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
