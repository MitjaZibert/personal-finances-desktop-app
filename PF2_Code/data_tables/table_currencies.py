# ===========================================================================================
# Code specific to TableView Incomes Categories
#
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries


# PyQt Windows libraries
from PyQt6 import QtCore

# App Specific libraries
import globals
from data_modules import DB_Util
from dialog_windows.win_delete_row import Win_Delete_Row
from data_tables.table_currencies_add_row_win import Win_Add_Row_Reg_Currency

# =========================================================


# Code specific to tableView_Currency
class TableCurrency:
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Currency"]
        self.db = DB_Util()

    # +++++++++++++++++++++++++++
    # Execute DDL on DBS
    # ++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()

    # =========================================================
    # Main Window - Table Currencies functionality
    #++++
    def tableCurrenciesFunctionality(self):
        # Seetings on row chanage
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():        
            self.updateRegCurrency()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)

    # +++++++++++++++++++++++++++
    # Enable Delete button if Currency is not used in other tables
    # ++++
    def rowChanged(self):

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        # changed item row ID
        currencyIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        currencyID = currencyIDIndex.data()

        query = f"""SELECT COUNT(ALLOC_ID) FROM MONEY_ALLOCATION WHERE CURR_ID  = {currencyID}"""
        data = self.db.getData(query).fetchone()
        count = int(data[0])

        if count > 0:
            globals.mainWinClass.ui.pushButton_DeleteCurrency.setEnabled(False)
        else:
            globals.mainWinClass.ui.pushButton_DeleteCurrency.setEnabled(True)

    # +++++++++++++++++++++++++++
    # Update changes on Reg_Currency table - tableView_Currency
    # ++++
    def updateRegCurrency(self):

        self.tableData.tableObject.model().blockSignals(True)

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        # changed item row ID
        currencyIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        currencyID = currencyIDIndex.data()

        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]

        # Updated value
        updatedItemValue = itemIndex.data()

        # DML statement
        update_stmt = None

        # db_columns = "curr_id", "curr_code", "curr_name", "curr_rate", "rate_date", "crypto"

        # column "curr_code", "curr_name", "curr_rate", "rate_date"
        if updatedColumn in ["curr_code", "curr_name", "curr_rate", "rate_date"]:
            update_stmt = f"""UPDATE REG_CURRENCY SET {updatedColumn} = '{updatedItemValue}' WHERE CURR_ID = {currencyID}"""

        # column "crypto"
        if updatedColumn == "crypto":
            itemIndex = self.tableData.tableObject.model().index(itemIndex.row(), 5)
            checkState = itemIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)

            updatedItemValue = 0
            if checkState == QtCore.Qt.CheckState.Checked:
                updatedItemValue = 2

            update_stmt = f"""UPDATE REG_CURRENCY SET CRYPTO = {updatedItemValue} WHERE CURR_ID = {currencyID}"""

        # if DML statement is generated, do DB update
        if update_stmt:
            self._executeDDL(update_stmt)

        self.tableData.tableObject.model().blockSignals(False)

    # +++++++++++++++++++++++++++
    # Insert new row into Reg_Currency table - tableView_Currency
    # ++++
    def insertRegCurrency(self):

        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Reg_Currency(callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)

    # +++++++++++++++++++++++++++
    # Delete row from Reg_Currency table - tableView_Currency
    # ++++
    def deleteRegCurrency(self):

        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        # selected item - CURR_ID
        rowData.append(
            self.tableData.tableObject.model().index(itemIndex.row(), 0).data()
        )
        # selected item - CURR_CODE
        rowData.append(
            self.tableData.tableObject.model().index(itemIndex.row(), 1).data()
        )
        # selected item - CURR_NAME
        rowData.append(
            self.tableData.tableObject.model().index(itemIndex.row(), 2).data()
        )

        self.winDeleteRow = Win_Delete_Row(
            table="Currencies", rowData=rowData, callback=self.repopulateData
        )
        self.winDeleteRow.show()

        self.tableData.tableObject.model().blockSignals(False)

    # +++++++++++++++++++++++++++
    # # Repopulate data as a callback
    # ++++

    def repopulateData(self, repopulate=True):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

            table = globals.tableDict["tableView_Currency"]
            # refresh data in tableView_Currency
            populateTable(table)
