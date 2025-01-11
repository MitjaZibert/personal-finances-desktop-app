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
from data_tables.table_cat_incomes_add_row_win import Win_Add_Row_Cat_Incomes

# =========================================================

# Code specific to tableView_Income_Categories
class TableIncomesCategories():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Income_Categories"]
        self.db = DB_Util()


    #+++++++++++++++++++++++++++
    # Execute DDL on DBS
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()

    # =========================================================
    # Main Window - Table Incomes Categories functionality
    #++++
    def tableIncomesCategoriesFunctionality(self):
         # Seetings on row chnage
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():        
            self.updateCatIncomes()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)


    #+++++++++++++++++++++++++++
    # Enable Delete button if Category is not used in other tables
    #++++
    def rowChanged(self):
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        catIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        catID = catIDIndex.data()

        
        query = "SELECT COUNT(INC_CATEGORY_ID) FROM INCOMES WHERE INC_CATEGORY_ID = " + str(catID)
        data = self.db.getData(query).fetchone()
        count = int(data[0])
    
        if count > 0:
            globals.mainWinClass.ui.pushButton_DeleteIncomeCat.setEnabled(False)
        else:
            globals.mainWinClass.ui.pushButton_DeleteIncomeCat.setEnabled(True)


    #+++++++++++++++++++++++++++
    # Update changes on Incomes Category table - tableView_Income_Categories
    #++++
    def updateCatIncomes(self):

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
        
        #db_columns = ["inc_category_id", "inc_category", "inc_cat_desc"]
                               
        # column "inc_category", "inc_cat_desc"
        if updatedColumn in ["inc_category", "inc_cat_desc"]:
            update_stmt = "UPDATE REG_INCOME_CATEGORIES SET " + str(updatedColumn) + " = '" + str(updatedItemValue) + "' WHERE INC_CATEGORY_ID = " + str(catID)

        
        # if DML statement is generated, do DB update
        if update_stmt:
            self._executeDDL(update_stmt)

        self.tableData.tableObject.model().blockSignals(False)
       
    #+++++++++++++++++++++++++++
    # Insert new row into Incomes Category table - tableView_Income_Categories
    #++++
    def insertCatIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Cat_Incomes(callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Delete row from Incomes Category table - tableView_Income_Categories
    #++++
    def deleteCatIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Category ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 0).data())
        # selected item - Category
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Description
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Cat_Incomes', rowData=rowData, callback=self.repopulateData)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)
        
        
   #+++++++++++++++++++++++++++
    # # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

                
            table = globals.tableDict["tableView_Income_Categories"]
            # refresh data in tableView_Income_Categories
            populateTable(table)
