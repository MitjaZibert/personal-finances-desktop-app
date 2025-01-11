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
from ui_qt.ui_add_row_cat_incomes import Ui_Win_Add_Row_Cat_Incomes

# ===========================================================================================


# New window
class Win_Add_Row_Cat_Incomes(QtWidgets.QDialog, Ui_Win_Add_Row_Cat_Incomes):
    def __init__(self, callback, parent=None):
        super(Win_Add_Row_Cat_Incomes, self).__init__(parent)

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

        cat = str(self.lineEdit_Category.text())
        cat_desc = str(self.lineEdit_Description.text())

        insert_stmt = (
            "INSERT INTO REG_INCOME_CATEGORIES (INC_CATEGORY, INC_CAT_DESC) VALUES ('"
            + cat
            + "', '"
            + cat_desc
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
