# ===========================================================================================
# Data manipulations on Expenses table (update, delete, add, commit, rollback)
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
from data_tables.table_expenses_add_row_win import Win_Add_Row_Expense
import data_modules.data_calculations as data_calculations


# =========================================================

# Data Manipulation for Expenses Table
class TableExpenses():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Expenses"]
        self.db = DB_Util()

        # Get current year/month for this expense
        # tableBalanceData = globals.tableDict["tableView_Balance"]
        # itemIndex = tableBalanceData.tableObject.selectionModel().currentIndex()
        # expenseYearIndex = tableBalanceData.tableObject.model().index(itemIndex.row(), 0)
        # self.expenseYear = expenseYearIndex.data()
        # expenseMonthIndex = tableBalanceData.tableObject.model().index(itemIndex.row(), 1)
        # self.expenseMonth = expenseMonthIndex.data()

        
        self.expenseYear = globals.selected_year
        self.expenseMonth = globals.selected_month

    #+++++++++++++++++++++++++++
        # Execute DDL on DBS
        # Refresh tableView_Balance
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()
        
    # =========================================================
    # Main Window - Table Expenses functionality
    #++++
    def tableExpensesFunctionality(self):
        # Seetings on row chnage
        def _rowChanged():
            self.rowChanged()

        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
        # Update data
        def _updateData():        
            self.updateExpenses()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)
    
    #+++++++++++++++++++++++++++
    # Enable Delete button if ...?
    #++++
    def rowChanged(self):

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        regularIndex = self.tableData.tableObject.model().index(itemIndex.row(), 10)
        regular = regularIndex.data()

        # DELETE ROW Button
        if regular == None:
            globals.mainWinClass.ui.pushButton_DeleteExpense.setEnabled(True)
        else:
            globals.mainWinClass.ui.pushButton_DeleteExpense.setEnabled(False)

            
        # TRANSFER ROW Into Next Month Button
        if self.tableData.tableEnabled and regular == None:
            globals.mainWinClass.ui.pushButton_TransferExpense.setEnabled(True)
        else:
            globals.mainWinClass.ui.pushButton_TransferExpense.setEnabled(False)

    #+++++++++++++++++++++++++++
    # Update changes on Expense table - tableView_Expenses 
    #++++
    def updateExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        expenseIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 1)
        expenseID = expenseIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()
        
        # DML statement
        update_stmt = None
        updateRow = False

        #db_columns = ["expenses_sum_id", "expense_id", "exp_category", "expense", "notes", "amount_all", "amount_payed", "amount_open", "correction", "update_regular_expense", "regular_expense_id"],
        
        if updatedColumn in ["expense", "notes"]:
            update_stmt = "UPDATE EXPENSES SET " + str(updatedColumn) + " = '" + str(updatedItemValue) + "' WHERE EXPENSE_ID = " + str(expenseID)

        if updatedColumn == "correction":
            update_stmt = "UPDATE EXPENSES SET AMOUNT_PAYED = AMOUNT_PAYED + " + str(updatedItemValue) + ", AMOUNT_OPEN = AMOUNT_OPEN - " + str(updatedItemValue) + " WHERE EXPENSE_ID = " + str(expenseID)

            # update col 6: AMOUNT_PAYED
            amountPaidIndex = self.tableData.tableObject.model().index(itemIndex.row(), 6)
            amountPaid = float(amountPaidIndex.data()) + float(updatedItemValue)
            self.tableData.tableObject.model().setData(amountPaidIndex, amountPaid, QtCore.Qt.ItemDataRole.EditRole)

            # update col 7: AMOUNT_OPEN
            amountOpenIndex = self.tableData.tableObject.model().index(itemIndex.row(), 7)
            amountOpen = float(amountOpenIndex.data()) - float(updatedItemValue)
            self.tableData.tableObject.model().setData(amountOpenIndex, amountOpen, QtCore.Qt.ItemDataRole.EditRole)

            # set col 8: CORRECTION back to 0
            self.tableData.tableObject.model().setData(itemIndex, "0", QtCore.Qt.ItemDataRole.EditRole)

        if updatedColumn == "amount_all":
            update_stmt = "UPDATE EXPENSES SET AMOUNT_OPEN = AMOUNT_OPEN + (" + str(updatedItemValue) + " - AMOUNT_ALL), AMOUNT_ALL = " + str(updatedItemValue) + "  WHERE EXPENSE_ID = " + str(expenseID)

            # update col 7: AMOUNT_OPEN
            amountPaidIndex = self.tableData.tableObject.model().index(itemIndex.row(), 6)
            amountOpen = float(updatedItemValue) - float(amountPaidIndex.data())
            
            amountOpenIndex = self.tableData.tableObject.model().index(itemIndex.row(), 7)
            self.tableData.tableObject.model().setData(amountOpenIndex, amountOpen, QtCore.Qt.ItemDataRole.EditRole)

            
        if updatedColumn == "update_regular_expense":
            itemIndex = self.tableData.tableObject.model().index(itemIndex.row(), 9)
            checkState = itemIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)
            
            updatedItemValue = 0

            if checkState == QtCore.Qt.CheckState.Checked:
                
                # Check if selected expense is by deafult a regular exspense (regular_expense_id NOT NULL)
                itemIndex = self.tableData.tableObject.model().index(itemIndex.row(), 10)
                regular_expense_id = itemIndex.data()

                if regular_expense_id is not None:
                    updatedItemValue = 2

                    update_stmt = """UPDATE EXPENSES 
                                    JOIN (select RI.REGULAR_EXPENSE_ID, RI.EXP_CATEGORY_ID, RI.REGULAR_EXPENSE, I.NOTES, RI.AMOUNT, RI.AMOUNT - I.AMOUNT_PAYED AS AMOUNT_OPEN, """ + str(updatedItemValue) + """ 
                                    from EXPENSES I, REG_REGULAR_EXPENSES RI 
                                    where I.REGULAR_EXPENSE_ID = RI.REGULAR_EXPENSE_ID AND RI.REGULAR_EXPENSE_ID = """ + str(regular_expense_id) + """ AND EXPENSE_ID = """ + str(expenseID) + """) AS RegInc
                                    ON EXPENSES.REGULAR_EXPENSE_ID = RegInc.REGULAR_EXPENSE_ID
                                    SET EXPENSES.EXP_CATEGORY_ID = RegInc.EXP_CATEGORY_ID, EXPENSES.EXPENSE = RegInc.REGULAR_EXPENSE, EXPENSES.NOTES = RegInc.NOTES, EXPENSES.AMOUNT_ALL = RegInc.AMOUNT, EXPENSES.AMOUNT_OPEN = RegInc.AMOUNT_OPEN, UPDATE_REGULAR_EXPENSE = 2
                                    WHERE EXPENSES.EXPENSE_ID = """ + str(expenseID)
                    updateRow = True
            else:     
                update_stmt = "UPDATE EXPENSES SET " + str(updatedColumn) + " = " + str(updatedItemValue) + " WHERE EXPENSE_ID = " + str(expenseID)
        

        # if DML statement is generated, do DB update
        if update_stmt:
            self._executeDDL(update_stmt)

            if updateRow == True:
                self._updateRow(itemIndex, expenseID)

            self.repopulateData(repopulate = True, repopulateSingle = "tableView_Balance")

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Insert new row into Expense table - tableView_Expenses
    #++++
    def insertExpense(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        self.winAddRow = Win_Add_Row_Expense(expenseYear=self.expenseYear, expenseMonth=self.expenseMonth, callback=self.repopulateData)
        self.winAddRow.show()

        self.tableData.tableObject.model().blockSignals(False)
        
    #+++++++++++++++++++++++++++
    # Delete row from Expenses table - tableView_Expenses
    #++++
    def deleteExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Expense ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Category
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Expense
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 5).data())
        
        self.winDeleteRow = Win_Delete_Row(table='Expenses', rowData=rowData, callback=self.repopulateData)
        self.winDeleteRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)

    #+++++++++++++++++++++++++++
    # Transfer selected row to the next month
    #++++
    def transferExpenses(self):
        
        self.tableData.tableObject.model().blockSignals(True)

        rowData = []

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        
        # selected item - Expense ID
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 1).data())
        # selected item - Category
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 2).data())
        # selected item - Expense
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 3).data())
        # selected item - Amount
        rowData.append(self.tableData.tableObject.model().index(itemIndex.row(), 5).data())
        
        self.winTransferRow = Win_Transfer_Row(table='Expenses', rowData=rowData, callback=self.repopulateData)
        self.winTransferRow.show()
    

        self.tableData.tableObject.model().blockSignals(False)




    #+++++++++++++++++++++++++++
    # # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True, repopulateSingle = None):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable


            if repopulateSingle == None or repopulateSingle == "tableView_Balance":        
                table = globals.tableDict["tableView_Balance"]
                # refresh data in tableView_Balance
                populateTable(table, setRowFocus = False)

            
            if repopulateSingle == None or repopulateSingle == "tableView_Expenses": 
                table = globals.tableDict["tableView_Expenses"]
                # refresh data in tableView_Expenses
                populateTable(table)
            
            
            data_calculations.recalculateAmounts()
        

#+++++++++++++++++++++++++++
    # # Update row data
    #++++

    def _updateRow(self, rowItemIndex, rowId):
        if rowId is not None:
            #query = "SELECT CAT.INC_CATEGORY, INCOME, NOTES, AMOUNT_ALL, AMOUNT_RECEIVED, AMOUNT_OPEN FROM INCOMES I, REG_INCOME_CATEGORIES CAT WHERE I.INC_CATEGORY_ID = CAT.INC_CATEGORY_ID AND I.INCOME_ID = " + str(rowId)
            query = "SELECT EXPENSE, NOTES, AMOUNT_ALL, AMOUNT_PAYED, AMOUNT_OPEN FROM EXPENSES WHERE EXPENSE_ID = " + str(rowId)
            data = self.db.getData(query).fetchone()
            
            expense = data[0]
            notes = data[1]
            amountAll = data[2]
            amountPaid = data[3]
            amountOpen = data[4]

            
            # update col 3: INCOME
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 3)
            self.tableData.tableObject.model().setData(incomeIndex, expense, QtCore.Qt.ItemDataRole.EditRole)
 
            # update col 4: NOTES
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 4)
            self.tableData.tableObject.model().setData(incomeIndex, notes, QtCore.Qt.ItemDataRole.EditRole)
           
            # update col 5: AMOUNT_ALL
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 5)
            self.tableData.tableObject.model().setData(incomeIndex, amountAll, QtCore.Qt.ItemDataRole.EditRole)

            # update col 6: AMOUNT_PAYED
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 6)
            self.tableData.tableObject.model().setData(incomeIndex, amountPaid, QtCore.Qt.ItemDataRole.EditRole)
            
            # update col 7: AMOUNT_OPEN
            incomeIndex = self.tableData.tableObject.model().index(rowItemIndex.row(), 7)
            self.tableData.tableObject.model().setData(incomeIndex, amountOpen, QtCore.Qt.ItemDataRole.EditRole)

