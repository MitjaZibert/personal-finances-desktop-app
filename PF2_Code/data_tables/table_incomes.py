# ===========================================================================================
# Data manipulations on Incomes table (update, delete, add, commit, rollback)
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
from dialog_windows.win_transfer_row import Win_Transfer_Row
from data_tables.table_incomes_add_row_win import Win_Add_Row_Income
import data_modules.data_calculations as data_calculations


# =========================================================

# Data Manipulation for Incomes Table
class TableIncomes():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Incomes"]
        self.db = DB_Util()

        # Get current year/month for this income
        # tableBalanceData = globals.tableDict["tableView_Balance"]
        # itemIndex = tableBalanceData.tableObject.selectionModel().currentIndex()
        # incomeYearIndex = tableBalanceData.tableObject.model().index(itemIndex.row(), 0)
        # self.incomeYear = incomeYearIndex.data()
        # incomeMonthIndex = tableBalanceData.tableObject.model().index(itemIndex.row(), 1)
        # self.incomeMonth = incomeMonthIndex.data()

        self.incomeYear = globals.selected_year
        self.incomeMonth = globals.selected_month
        
    #+++++++++++++++++++++++++++
        # Execute DDL on DBS
        # Refresh tableView_Balance
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()
        

    # =========================================================
    # Main Window - Table Incomes functionality
    #++++
    def tableIncomesFunctionality(self):

        # Seetings on row chnage
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():        
            self.updateIncomes()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)


    #+++++++++++++++++++++++++++
    # Enable/Disable buttons
    #++++
    def rowChanged(self):
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        regularIndex = self.tableData.tableObject.model().index(itemIndex.row(), 10)
        regular = regularIndex.data()

        # DELETE ROW Button
        if regular == None:
            globals.mainWinClass.ui.pushButton_DeleteIncome.setEnabled(True)
        else:
            globals.mainWinClass.ui.pushButton_DeleteIncome.setEnabled(False)

        # TRANSFER ROW Into Next Month Button
        if self.tableData.tableEnabled and regular == None:
            globals.mainWinClass.ui.pushButton_TransferIncome.setEnabled(True)
        else:
            globals.mainWinClass.ui.pushButton_TransferIncome.setEnabled(False)

    #+++++++++++++++++++++++++++
    # Update changes on Incomes table - tableView_Incomes 
    #++++
    def updateIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        incomeIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 1)
        incomeID = incomeIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()

        
        
        # DML statement
        update_stmt = None
        updateRow = False

        # db_columns = ["incomes_sum_id", "income_id", "inc_category", "income", "notes", "amount_all", "amount_recieved", "amount_open", "correction", "update_regular_income", "regular_income_id"],
           
        if updatedColumn in ["income", "notes"]:
            update_stmt = "UPDATE INCOMES SET " + str(updatedColumn) + " = '" + str(updatedItemValue) + "' WHERE INCOME_ID = " + str(incomeID)

        if updatedColumn == "correction":
            update_stmt = "UPDATE INCOMES SET AMOUNT_RECEIVED = AMOUNT_RECEIVED + " + str(updatedItemValue) + ", AMOUNT_OPEN = AMOUNT_OPEN - " + str(updatedItemValue) + " WHERE INCOME_ID = " + str(incomeID)

            # update col 6: AMOUNT_RECEIVED
            amountReceivedIndex = self.tableData.tableObject.model().index(itemIndex.row(), 6)
            amountReceived = float(amountReceivedIndex.data()) + float(updatedItemValue)
            self.tableData.tableObject.model().setData(amountReceivedIndex, amountReceived, QtCore.Qt.ItemDataRole.EditRole)
            # update col 7: AMOUNT_OPEN
            amountOpenIndex = self.tableData.tableObject.model().index(itemIndex.row(), 7)
            amountOpen = float(amountOpenIndex.data()) - float(updatedItemValue)
            self.tableData.tableObject.model().setData(amountOpenIndex, amountOpen, QtCore.Qt.ItemDataRole.EditRole)

            # set col 8: CORRECTION back to 0
            self.tableData.tableObject.model().setData(itemIndex, "0", QtCore.Qt.ItemDataRole.EditRole)

        if updatedColumn == "amount_all":
            update_stmt = "UPDATE INCOMES SET AMOUNT_OPEN = AMOUNT_OPEN + (" + str(updatedItemValue) + " - AMOUNT_ALL), AMOUNT_ALL = " + str(updatedItemValue) + "  WHERE INCOME_ID = " + str(incomeID)

            # update col 7: AMOUNT_OPEN
            amountReceivedIndex = self.tableData.tableObject.model().index(itemIndex.row(), 6)
            amountOpen = float(updatedItemValue) - float(amountReceivedIndex.data())
            
            amountOpenIndex = self.tableData.tableObject.model().index(itemIndex.row(), 7)
            self.tableData.tableObject.model().setData(amountOpenIndex, amountOpen, QtCore.Qt.ItemDataRole.EditRole)

            
        if updatedColumn == "update_regular_income":
            itemIndex = self.tableData.tableObject.model().index(itemIndex.row(), 9)
            checkState = itemIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)
            
            updatedItemValue = 0

            if checkState == QtCore.Qt.CheckState.Checked:
                
                # Check if selected income is by deafult a regular income (regular_income_id NOT NULL)
                itemIndex = self.tableData.tableObject.model().index(itemIndex.row(), 10)
                regular_income_id = itemIndex.data()

                if regular_income_id is not None:
                    updatedItemValue = 2

                    update_stmt = """UPDATE INCOMES 
                                    JOIN (select RI.REGULAR_INCOME_ID, RI.INC_CATEGORY_ID, RI.REGULAR_INCOME, I.NOTES, RI.AMOUNT, RI.AMOUNT - I.AMOUNT_RECEIVED AS AMOUNT_OPEN, """ + str(updatedItemValue) + """ 
                                    from INCOMES I, REG_REGULAR_INCOMES RI 
                                    where I.REGULAR_INCOME_ID = RI.REGULAR_INCOME_ID AND RI.REGULAR_INCOME_ID = """ + str(regular_income_id) + """ AND INCOME_ID = """ + str(incomeID) + """) AS RegInc
                                    ON INCOMES.REGULAR_INCOME_ID = RegInc.REGULAR_INCOME_ID
                                    SET INCOMES.INC_CATEGORY_ID = RegInc.INC_CATEGORY_ID, INCOMES.INCOME = RegInc.REGULAR_INCOME, INCOMES.NOTES = RegInc.NOTES, INCOMES.AMOUNT_ALL = RegInc.AMOUNT, INCOMES.AMOUNT_OPEN = RegInc.AMOUNT_OPEN, UPDATE_REGULAR_INCOME = 2
                                    WHERE INCOMES.INCOME_ID = """ + str(incomeID)
                    updateRow = True

            else:
                update_stmt = "UPDATE INCOMES SET " + str(updatedColumn) + " = " + str(updatedItemValue) + " WHERE INCOME_ID = " + str(incomeID)
        

        # if DML statement is generated, do DB update
        if update_stmt:
            self._executeDDL(update_stmt)

            if updateRow == True:
                self._updateRow(itemIndex, incomeID)

            self._repopulateTable(repopulate = True, repopulateSingle = "tableView_Balance")

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Insert new row into Incomes table - tableView_Incomes
    #++++
    def insertIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Income(incomeYear=self.incomeYear, incomeMonth=self.incomeMonth, callback=self._repopulateTable)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
       
    #+++++++++++++++++++++++++++
    # Delete row from Incomes table - tableView_Incomes
    #++++
    def deleteIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Incomes ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Category
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Income
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 5).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Incomes', rowData=rowData, callback=self._repopulateTable)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)
        

    #+++++++++++++++++++++++++++
    # Transfer selected row to the next month
    #++++
    def transferIncomes(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Incomes ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Category
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Income
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 5).data())
        
        self.winDeleteRow = Win_Transfer_Row(table='Incomes', rowData=rowData, callback=self._repopulateTable)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)


    
    #+++++++++++++++++++++++++++
    # # Repopulate table data as a callback
    #++++

    def _repopulateTable(self, repopulate = True, repopulateSingle = None):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

            if repopulateSingle == None or repopulateSingle == "tableView_Balance": 
                table = globals.tableDict["tableView_Balance"]
                # refresh data in tableView_Balance
                populateTable(table, setRowFocus = False)

            if repopulateSingle == None or repopulateSingle == "tableView_Incomes": 
                table = globals.tableDict["tableView_Incomes"]
                # refresh data in tableView_Incomes
                populateTable(table)

            data_calculations.recalculateAmounts()


    #+++++++++++++++++++++++++++
    # # Update row data
    #++++

    def _updateRow(self, rowItemIndex, rowId):
        if rowId is not None:
            #query = "SELECT CAT.INC_CATEGORY, INCOME, NOTES, AMOUNT_ALL, AMOUNT_RECEIVED, AMOUNT_OPEN FROM INCOMES I, REG_INCOME_CATEGORIES CAT WHERE I.INC_CATEGORY_ID = CAT.INC_CATEGORY_ID AND I.INCOME_ID = " + str(rowId)
            query = "SELECT INCOME, NOTES, AMOUNT_ALL, AMOUNT_RECEIVED, AMOUNT_OPEN FROM INCOMES WHERE INCOME_ID = " + str(rowId)
            data = self.db.getData(query).fetchone()
            
            income = data[0]
            notes = data[1]
            amountAll = data[2]
            amountReceived = data[3]
            amountOpen = data[4]

            
            # update col 3: INCOME
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 3)
            self.tableData.tableObject.model().setData(incomeIndex, income, QtCore.Qt.ItemDataRole.EditRole)
 
            # update col 4: NOTES
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 4)
            self.tableData.tableObject.model().setData(incomeIndex, notes, QtCore.Qt.ItemDataRole.EditRole)
           
            # update col 5: AMOUNT_ALL
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 5)
            self.tableData.tableObject.model().setData(incomeIndex, amountAll, QtCore.Qt.ItemDataRole.EditRole)

            # update col 6: AMOUNT_RECEIVED
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 6)
            self.tableData.tableObject.model().setData(incomeIndex, amountReceived, QtCore.Qt.ItemDataRole.EditRole)
            
            # update col 7: AMOUNT_OPEN
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 7)
            self.tableData.tableObject.model().setData(incomeIndex, amountOpen, QtCore.Qt.ItemDataRole.EditRole)

