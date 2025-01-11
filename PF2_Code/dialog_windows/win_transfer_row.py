# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6 import QtWidgets

# App Specific libraries
from data_modules import DB_Util
from ui_qt.ui_transfer_row import Ui_Win_Transfer_Row

# ===========================================================================================


# New window
class Win_Transfer_Row(QtWidgets.QDialog, Ui_Win_Transfer_Row):
    def __init__(self, table, rowData, callback, parent=None):
        super(Win_Transfer_Row, self).__init__(parent)

        # Setup Window
        self.setupUi(self)

        self.rowID = str(rowData[0])

        # Labels on Transfer Row Window

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

        self.rowTransferred = False

        # callback method
        self.callback = callback

        self.db = DB_Util()

        self.table = table

        # +++++++ Buttons ++++++++

        # (button) Save
        self.buttonBox.accepted.connect(self.transferRow)

        # (button) Close
        self.buttonBox.rejected.connect(self.closeWin)

    # +++++++++++++++++++++++++++
    # Delete Row
    # ++++
    def transferRow(self):

        transfer_stmt = None

        if self.table == "Incomes":

            query = (
                "select NEXT_INCOMES_SUM_ID from (select lead(INCOMES_SUM_ID) over (order by INCOMES_SUM_ID) as NEXT_INCOMES_SUM_ID, INCOMES_SUM_ID from INCOMES_SUM) as I where INCOMES_SUM_ID = (SELECT INCOMES_SUM_ID FROM INCOMES WHERE INCOME_ID = "
                + str(self.rowID)
                + ")"
            )
            data = self.db.getData(query).fetchone()

            nextMonthID = data[0]

            transfer_stmt = (
                "UPDATE INCOMES SET INCOMES_SUM_ID = "
                + str(nextMonthID)
                + " WHERE INCOME_ID = "
                + str(self.rowID)
            )

        if self.table == "Expenses":
            query = (
                "select NEXT_EXPENSES_SUM_ID from (select lead(EXPENSES_SUM_ID) over (order by EXPENSES_SUM_ID) as NEXT_EXPENSES_SUM_ID, EXPENSES_SUM_ID from EXPENSES_SUM) as E where E.EXPENSES_SUM_ID = (SELECT EXPENSES_SUM_ID FROM EXPENSES WHERE EXPENSE_ID = "
                + str(self.rowID)
                + ")"
            )
            data = self.db.getData(query).fetchone()

            nextMonthID = data[0]

            transfer_stmt = (
                "UPDATE EXPENSES SET EXPENSES_SUM_ID = "
                + str(nextMonthID)
                + " WHERE EXPENSE_ID =  "
                + str(self.rowID)
            )

        # if DML statement is generated, do DB update
        if transfer_stmt:
            self.db.executeDDL(transfer_stmt)
            self.db.saveData()
            self.rowTransferred = True

        self.closeWin()

    # +++++++++++++++++++++++++++
    # Close Window
    # ++++
    def closeWin(self):

        self.callback(self.rowTransferred)
        self.close()


# *********************************************************************************************
# *********************************************************************************************
# NOTES
# *********************************************************************************************
