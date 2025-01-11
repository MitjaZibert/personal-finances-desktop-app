# ===========================================================================================
# Code specific to TableView Regular_Expenses
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
from data_tables.table_regular_expenses_add_row_win import Win_Add_Row_Reg_Expense

# =========================================================

# Code specific to tableView_Regular_Expenses
class TableRegularExpenses():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Regular_Expenses"]
        self.db = DB_Util()
        self.expenseCategoriesComboDict = []


    #+++++++++++++++++++++++++++
    # Execute DDL on DBS
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()


    # =========================================================
    # Main Window - Table Regular Expenses functionality
    #++++
    def tableRegularExpensesFunctionality(self):

        # Seetings on row change
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():  
            self.updateRegularExpenses()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)

    #+++++++++++++++++++++++++++
    # Enable Delete button if Regular Expenses is not used in other tables
    #++++5
    def rowChanged(self):
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        regExpIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        regExpID = regExpIDIndex.data()

        
        query = f"""SELECT COUNT(REGULAR_EXPENSE_ID) FROM EXPENSES WHERE REGULAR_EXPENSE_ID = {regExpID}"""
        data = self.db.getData(query).fetchone()
        count = int(data[0])
    
        if count > 0:
            globals.mainWinClass.ui.pushButton_DeleteRegExpense.setEnabled(False)
        else:
            globals.mainWinClass.ui.pushButton_DeleteRegExpense.setEnabled(True)


    #+++++++++++++++++++++++++++
    # Update changes on Regular Expenses table - tableView_Regular_Expenses
    #++++
    def updateRegularExpenses(self):

        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        regExpIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        regExpID = regExpIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()
        
        # DML statement
        update_stmt = None
        
        #db_columns = ["regular_expense_id", "exp_category_id", "regular_expense", "amount", "months"]
                               
        # column "regular_expense", "amount", "months"
        if updatedColumn in ["regular_expense", "amount", "months"]:
            update_stmt = f"""UPDATE REG_REGULAR_EXPENSES SET {updatedColumn} = '{updatedItemValue}' WHERE REGULAR_EXPENSE_ID = {regExpID}"""

        # column "exp_category" is changed through combobox, but "exp_category_id" must be updated
        if updatedColumn in ["exp_category"]:
            updatedColumn = "exp_category_id"
            updatedColumnIndex = 1
            expenseCategoryIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), updatedColumnIndex)
            updatedItemValue = expenseCategoryIDIndex.data()
            update_stmt = f"""UPDATE REG_REGULAR_EXPENSES SET {updatedColumn} = {updatedItemValue} WHERE REGULAR_EXPENSE_ID = {regExpID}"""
        
        
        # if DML statement is generated, do DB update
        if update_stmt:
            from data_tables.data_tables_core.populate_table import populateTable
            self._executeDDL(update_stmt)
            table = globals.tableDict["tableView_Expenses"]
            # refresh data in tableView_Expenses
            populateTable(table)

        self.tableData.tableObject.model().blockSignals(False)
       
    #+++++++++++++++++++++++++++
    # Insert new row into Regular Expenses table - tableView_Regular_Expenses
    #++++
    def insertRegularExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Reg_Expense(callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Delete row from Regular Expenses table - tableView_Regular_Expenses
    #++++
    def deleteRegularExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Regular Expenses ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 0).data())
        # selected item - Category ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Description
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        # selected item - Months
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 4).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Regular_Expenses', rowData=rowData, callback=self.repopulateData)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)
        
        
   #+++++++++++++++++++++++++++
    # # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

                
            table = globals.tableDict["tableView_Regular_Expenses"]
            # refresh data in tableView_Regular_Expenses
            populateTable(table)
            
            # refresh data in tableView_Expenses
            table = globals.tableDict["tableView_Expenses"]
            populateTable(table)



    #+++++++++++++++++++++++++++
    # Create combobox
    #++++
    def comboBoxDelegate(self):
        comboColumnIndex = 2
        
        query = "SELECT exp_category_id, exp_category FROM REG_EXPENSE_CATEGORIES ORDER BY exp_category_id ASC"
        self.expenseCategoriesComboDict, comboList = ComboBoxDelegate.getComboBoxData(query)
        delegate = ComboBoxDelegate(comboList, self.handleComboBoxChange)
        self.tableData.tableObject.setItemDelegateForColumn(comboColumnIndex, delegate)


    #+++++++++++++++++++++++++++
    # This method will be called when the combobox signal is emitted
    #++++
    def handleComboBoxChange(self, text):
        # get key from selected combobox value (text)
        expenseCategoryID = next((key for key, val in self.expenseCategoriesComboDict.items() if val == text), None)
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        incomeCategoryIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 1)
        self.tableData.tableObject.model().setData(incomeCategoryIDIndex, expenseCategoryID, Qt.ItemDataRole.EditRole)

        self.tableData.tableObject.model().blockSignals(False)