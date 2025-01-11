# ===========================================================================================
# Code specific to TableView Regular_Incomes
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
from data_tables.table_regular_incomes_add_row_win import Win_Add_Row_Reg_Income


# =========================================================

# Code specific to tableView_Regular_Incomes
class TableRegularIncomes():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Regular_Incomes"]
        self.db = DB_Util()

        self.incomeCategoriesComboDict = []


    #+++++++++++++++++++++++++++
    # Execute DDL on DBS
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()



    # =========================================================
    # Main Window - Table Regular Incomes functionality
    #++++
    def tableRegularIncomesFunctionality(self):
        # Seetings on row change
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():  
            self.updateRegularIncomes()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)



    #+++++++++++++++++++++++++++
    # Enable Delete button if Regular Income is not used in other tables
    #++++5
    def rowChanged(self):
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        regIncIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        regIncID = regIncIDIndex.data()

        
        query = f"""SELECT COUNT(REGULAR_INCOME_ID) FROM INCOMES WHERE REGULAR_INCOME_ID = {regIncID}"""
        data = self.db.getData(query).fetchone()
        count = int(data[0])
    
        if count > 0:
            globals.mainWinClass.ui.pushButton_DeleteRegIncome.setEnabled(False)
        else:
            globals.mainWinClass.ui.pushButton_DeleteRegIncome.setEnabled(True)


    #+++++++++++++++++++++++++++
    # Update changes on Regular Incomes table - tableView_Regular_Incomes
    #++++
    def updateRegularIncomes(self):

        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        regIncIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        regIncID = regIncIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()
        
        # DML statement
        update_stmt = None
        
        #db_columns = ["regular_income_id", "inc_category_id", "regular_income", "amount"]

        # column  "regular_income", "amount"
        if updatedColumn in ["regular_income", "amount"]:
            update_stmt = f"""UPDATE REG_REGULAR_INCOMES SET {updatedColumn} = '{updatedItemValue}' WHERE REGULAR_INCOME_ID = {regIncID}"""
       
        # column "inc_category" is changed through combobox, but "inc_category_id" must be updated
        if updatedColumn in ["inc_category"]:
            updatedColumn = "inc_category_id"
            updatedColumnIndex = 1
            incomeCategoryIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), updatedColumnIndex)
            updatedItemValue = incomeCategoryIDIndex.data()
            update_stmt = f"""UPDATE REG_REGULAR_INCOMES SET {updatedColumn} = {updatedItemValue} WHERE REGULAR_INCOME_ID = {regIncID}"""
        
       
        # if DML statement is generated, do DB update
        if update_stmt:
            from data_tables.data_tables_core.populate_table import populateTable
            self._executeDDL(update_stmt)
            table = globals.tableDict["tableView_Incomes"]
            # refresh data in tableView_Incomes
            populateTable(table)

        self.tableData.tableObject.model().blockSignals(False)
       
    #+++++++++++++++++++++++++++
    # Insert new row into Regular Incomes table - tableView_Regular_Incomes
    #++++
    def insertRegularIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Reg_Income(callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Delete row from Regular Incomes table - tableView_Regular_Incomes
    #++++
    def deleteRegularIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Regular Income ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 0).data())
        # selected item - Category ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Description
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Regular_Incomes', rowData=rowData, callback=self.repopulateData)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)
        
        
    #+++++++++++++++++++++++++++
    # # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

            table = globals.tableDict["tableView_Regular_Incomes"]
            # refresh data in tableView_Regular_Incomes
            populateTable(table)

            # refresh data in tableView_Incomes
            table = globals.tableDict["tableView_Incomes"]
            populateTable(table)
    
    
    
    #+++++++++++++++++++++++++++
    # Create combobox
    #++++
    def comboBoxDelegate(self):
        comboColumnIndex = 2
        
        query = "SELECT inc_category_id, inc_category FROM REG_INCOME_CATEGORIES ORDER BY inc_category_id ASC"
        self.incomeCategoriesComboDict, comboList = ComboBoxDelegate.getComboBoxData(query)
        delegate = ComboBoxDelegate(comboList, self.handleComboBoxChange)
        self.tableData.tableObject.setItemDelegateForColumn(comboColumnIndex, delegate)

    #+++++++++++++++++++++++++++
    # This method will be called when the combobox signal is emitted
    #++++
    def handleComboBoxChange(self, text):
        # get key from selected combobox value (text)
        incomeCategoryID = next((key for key, val in self.incomeCategoriesComboDict.items() if val == text), None)
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        incomeCategoryIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 1)
        self.tableData.tableObject.model().setData(incomeCategoryIDIndex, incomeCategoryID, Qt.ItemDataRole.EditRole)

        self.tableData.tableObject.model().blockSignals(False)
      