# ===========================================================================================
# Code specific to TableView Expenses Categories
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
from data_tables.table_cat_expenses_add_row_win import Win_Add_Row_Cat_Expenses

# =========================================================

# Code specific to tableView_Expense_Categories
class TableExpensesCategories():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Expense_Categories"]
        self.db = DB_Util()


    #+++++++++++++++++++++++++++
    # Execute DDL on DBS
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()


    # =========================================================
    # Main Window - Table Expense Category functionality
    #++++
    def tableExpensesCategoriesFunctionality(self):
    
        # Seetings on row chnage
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():        
            self.updateCatExpenses()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)


    #+++++++++++++++++++++++++++
    # Enable Delete button if Category is not used in other tables
    #++++
    def rowChanged(self):
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        catIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        catID = catIDIndex.data()

        
        query = "SELECT COUNT(EXP_CATEGORY_ID) FROM EXPENSES WHERE EXP_CATEGORY_ID = " + str(catID)
        data = self.db.getData(query).fetchone()
        count = int(data[0])
    
        if count > 0:
            globals.mainWinClass.ui.pushButton_DeleteExpenseCat.setEnabled(False)
        else:
            globals.mainWinClass.ui.pushButton_DeleteExpenseCat.setEnabled(True)


    #+++++++++++++++++++++++++++
    # Update changes on Expenses Category table - tableView_Expense_Categories
    #++++
    def updateCatExpenses(self):

        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        catIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        catID = catIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()
        
        # DML statement
        update_stmt = None
        
        #db_columns = ["exp_category_id", "exp_category", "exp_cat_desc"]
                               
        # column "inc_category", "inc_cat_desc"
        if updatedColumn in ["exp_category", "exp_cat_desc"]:
            update_stmt = "UPDATE REG_EXPENSE_CATEGORIES SET " + str(updatedColumn) + " = '" + str(updatedItemValue) + "' WHERE EXP_CATEGORY_ID = " + str(catID)

        
        # if DML statement is generated, do DB update
        if update_stmt:
            self._executeDDL(update_stmt)

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Insert new row into Expenses Category table - tableView_Expense_Categories
    #++++
    def insertCatExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Cat_Expenses(callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Delete row from Expenses Category table - tableView_Expense_Categories
    #++++
    def deleteCatExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Category ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 0).data())
        # selected item - Category
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Description
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Cat_Expenses', rowData=rowData, callback=self.repopulateData)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)
        
   #+++++++++++++++++++++++++++
    # # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

                
            table = globals.tableDict["tableView_Expense_Categories"]
            # refresh data in tableView_Expense_Categories
            populateTable(table)
