# ===========================================================================================
# Code specific to TableView Allocation
# 
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries


# PyQt Windows libraries
from PyQt6.QtCore import Qt

# App Specific libraries
import globals
from data_modules import DB_Util
from data_tables.data_tables_core.combo_box_delegate import ComboBoxDelegate
from dialog_windows.win_delete_row import Win_Delete_Row
from data_tables.table_allocation_add_row_win import Win_Add_Row_Allocation
import data_modules.data_calculations as data_calculations

# =========================================================

# Code specific to tableView_Allocation
class TableAllocation():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Allocation"]
        self.db = DB_Util()
        self.currenciesComboDict = {}


    #+++++++++++++++++++++++++++
    # Execute DDL on DBS
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()

    # =========================================================
    # Main Window - Table Allocation functionality
    #++++
    def tableAllocationFunctionality(self):

        # Seetings on row chnage
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():        
            self.updateAllocation()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)


    #+++++++++++++++++++++++++++
    # Enable Delete button if Allocation Amount <> 0
    #++++
    def rowChanged(self):

        self._enableDeleteButton()

    #+++++++++++++++++++++++++++
    # Enable Delete button if Allocation Amount <> 0
    #++++
    def _enableDeleteButton(self):

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        amountIndex = self.tableData.tableObject.model().index(itemIndex.row(), 3)
        amount = amountIndex.data()

        avlIndex = self.tableData.tableObject.model().index(itemIndex.row(), 7)
        checkState = avlIndex.data(Qt.ItemDataRole.CheckStateRole)
        
        if float(amount) == 0.0 and checkState == Qt.CheckState.Unchecked:
            globals.mainWinClass.ui.pushButton_DeleteAllocation.setEnabled(True)
        else:
            globals.mainWinClass.ui.pushButton_DeleteAllocation.setEnabled(False)


    #+++++++++++++++++++++++++++
    # Update changes on Allocation table - tableView_Allocation
    #++++
    def updateAllocation(self):
        # if DML statement is generated, do DB update
        def _updateDB(update_stmt):
            if update_stmt:
                self._executeDDL(update_stmt)
                self._enableDeleteButton()
                data_calculations.recalculateAmounts()


        # If currency is changed recalculate allocation amount
        def _recaclculateCurrency(itemValue):
            # Get Currency rate
            currCodeIndex = self.tableData.tableObject.model().index(itemIndex.row(), 4)
            currCode = currCodeIndex.data()

            query = f"""SELECT CURR_RATE FROM REG_CURRENCY WHERE CURR_CODE = '{currCode}'"""
            data_curr = self.db.getData(query)
            
            for row in data_curr:
                currRate = row[0]

            # Recalculated value based on currency rate
            recalculatedValue = float(itemValue) / float(currRate)

            return recalculatedValue
        
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        allocIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        allocID = allocIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()
        
        # DML statement
        update_stmt = None
        
        #db_columns = ["alloc_id", "allocation", "alloc_amount", "curr_code", "value", "alloc_desc", "available"]
                               
        # column "allocation" and "alloc_desc"
        if updatedColumn in ["allocation", "alloc_desc"]:
            update_stmt = f"""UPDATE MONEY_ALLOCATION SET {updatedColumn} = '{updatedItemValue}' WHERE ALLOC_ID = {allocID}"""
            _updateDB(update_stmt)

        # column "alloc_amount"
        if updatedColumn == "alloc_amount":
            # Recalculated value based on currency rate
            updatedValue = _recaclculateCurrency(updatedItemValue)
            update_stmt = f"""UPDATE MONEY_ALLOCATION SET ALLOC_AMOUNT = {updatedItemValue} , VALUE = {updatedValue} WHERE ALLOC_ID = {allocID}"""
            _updateDB(update_stmt)

            # Update Value column in the table
            valueIndex = self.tableData.tableObject.model().index(itemIndex.row(), 5)            
            self.tableData.tableObject.model().setData(valueIndex, updatedValue, Qt.ItemDataRole.EditRole)
            
        # column "curr_code"
        if updatedColumn in ["curr_code"]:
            updatedColumn = "curr_id"
            updatedColumnIndex = 1
            currIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), updatedColumnIndex)
            updatedItemValue = currIDIndex.data()
            update_stmt = f"""UPDATE MONEY_ALLOCATION SET {updatedColumn} = {updatedItemValue} WHERE ALLOC_ID = {allocID}"""
            _updateDB(update_stmt)

            # Recalculated value based on currency rate
             # changed item row ID
            amountIndex = self.tableData.tableObject.model().index(itemIndex.row(), 3)
            amount = amountIndex.data()
        
            recalculatedValue = _recaclculateCurrency(amount)
            update_stmt = f"""UPDATE MONEY_ALLOCATION SET VALUE = {recalculatedValue} WHERE ALLOC_ID = {allocID}"""
            _updateDB(update_stmt)

            # Update Value column in the table
            valueIndex = self.tableData.tableObject.model().index(itemIndex.row(), 5)            
            self.tableData.tableObject.model().setData(valueIndex, recalculatedValue, Qt.ItemDataRole.EditRole)
      
        # column "available"
        if updatedColumn == "available":
            availableIndex = self.tableData.tableObject.model().index(itemIndex.row(), 7)
            checkState = availableIndex.data(Qt.ItemDataRole.CheckStateRole)
            
            if checkState == Qt.CheckState.Checked:
                updatedItemValue = 2
            else:
                updatedItemValue = 0
                
            update_stmt = f"""UPDATE MONEY_ALLOCATION SET {updatedColumn} = '{updatedItemValue}' WHERE ALLOC_ID = {allocID}"""
            _updateDB(update_stmt)
        

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Insert new row into Allocation table - tableView_Allocation
    #++++
    def insertAllocation(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Allocation(callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
        
        
    #+++++++++++++++++++++++++++
    # Delete row from Allocation table - tableView_Allocation
    #++++
    def deleteAllocation(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Allocation ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 0).data())
        # selected item - Allocation
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Description
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 6).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Allocation', rowData=rowData, callback=self.repopulateData)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)
        
        
    #+++++++++++++++++++++++++++
    # # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

            table = globals.tableDict["tableView_Allocation"]
            # refresh data in tableView_Allocation
            populateTable(table)
            
            data_calculations.recalculateAmounts()

    

    #+++++++++++++++++++++++++++
    # Create combobox
    #++++
    def comboBoxDelegate(self):
        comboColumnIndex = 4
        
        query = "SELECT CURR_ID, CURR_CODE FROM REG_CURRENCY ORDER BY CURR_CODE ASC"
        self.currenciesComboDict, comboList = ComboBoxDelegate.getComboBoxData(query)
        delegate = ComboBoxDelegate(comboList, self.handleComboBoxChange)
        self.tableData.tableObject.setItemDelegateForColumn(comboColumnIndex, delegate)

    #+++++++++++++++++++++++++++
    # This method will be called when the combobox signal is emitted
    #++++
    def handleComboBoxChange(self, text):
        # get key from selected combobox value (text)
        currencyID = next((key for key, val in self.currenciesComboDict.items() if val == text), None)
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        currecyIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 1)
        self.tableData.tableObject.model().setData(currecyIDIndex, currencyID, Qt.ItemDataRole.EditRole)

        self.tableData.tableObject.model().blockSignals(False)
     