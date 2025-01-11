# ===========================================================================================
# Main Window functionality
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries
import sys

# PyQt Windows libraries
from PyQt6.QtWidgets import QApplication

# App Specific libraries
import globals
from data_modules import closeConn
from data_tables.table_allocation import TableAllocation
from data_tables.table_incomes import TableIncomes
from data_tables.table_expenses import TableExpenses
from data_tables.table_cat_incomes import TableIncomesCategories
from data_tables.table_cat_expenses import TableExpensesCategories
from data_tables.table_money_correction import TableMoneyCorrection
from data_tables.table_regular_incomes import TableRegularIncomes
from data_tables.table_regular_expenses import TableRegularExpenses
from data_tables.table_currencies import TableCurrency

# =========================================================

# Main Window functionality
class WinMainFunc():
    def __init__(self, winObject):
        self.winMain = winObject

    def mainWindowFunctionality(self):

        def _on_focusChanged():
            try:
                # store currently selected widget
                globals.activeWidget = QApplication.focusWidget().objectName()
            except:
                # on close window no widget is selected
                None
            

        QApplication.instance().focusChanged.connect(_on_focusChanged)
       
        # +++
        # Button: Main page
        def _setPageIndex(pageIndex: int):
            self.winMain.ui.stackedWidget_Main.setCurrentIndex(pageIndex)

            if pageIndex == 3: #BUG for some reason this doesn't yet work
                tableMoneyCorrection = TableMoneyCorrection()
                tableMoneyCorrection.setCurrentMonthRow(setFocus=True)

        self.winMain.ui.pushButton_Main.clicked.connect(lambda: _setPageIndex(0))
        self.winMain.ui.pushButton_Registries.clicked.connect(lambda: _setPageIndex(1))
        self.winMain.ui.pushButton_Settings.clicked.connect(lambda: _setPageIndex(2))

 
        # +++
        # Button: Add Allocation Button
        
        def _addAllocation():
            addRowWindow = TableAllocation()
            addRowWindow.insertAllocation()

        self.winMain.ui.pushButton_AddAllocation.clicked.connect(_addAllocation)       
    
        # Button: Add Income Button
        def _addIncome():
            addRowWindow = TableIncomes()
            addRowWindow.insertIncomes()

        self.winMain.ui.pushButton_AddIncome.clicked.connect(_addIncome)      

        
        # Button: Add Expense Button
        def _addExpense():
            addRowWindow = TableExpenses()
            addRowWindow.insertExpense()

        self.winMain.ui.pushButton_AddExpense.clicked.connect(_addExpense)    
    
    
        # Button: Add Income Categories Button
        def _addIncomeCat():
            addRowWindow = TableIncomesCategories()
            addRowWindow.insertCatIncomes()

        self.winMain.ui.pushButton_AddIncomeCat.clicked.connect(_addIncomeCat)    

        
        # Button: Add Regular Income Button
        def _addRegularIncome():
            addRowWindow = TableRegularIncomes()
            addRowWindow.insertRegularIncomes()

        self.winMain.ui.pushButton_AddRegIncome.clicked.connect(_addRegularIncome)  


        # Button: Add Expense Categories Button
        def _addExpenseCat():
            addRowWindow = TableExpensesCategories()
            addRowWindow.insertCatExpenses()

        self.winMain.ui.pushButton_AddExpenseCat.clicked.connect(_addExpenseCat)    

        
        # Button: Add Regular Expense Button
        def _addRegularExpense():
            addRowWindow = TableRegularExpenses()
            addRowWindow.insertRegularExpenses()

        self.winMain.ui.pushButton_AddRegExpense.clicked.connect(_addRegularExpense)  

        
        # Button: Add Currency Button
        def _addCurrency():
            addRowWindow = TableCurrency()
            addRowWindow.insertRegCurrency()

        self.winMain.ui.pushButton_AddCurrency.clicked.connect(_addCurrency)  
    

        # +++
        # Button: Delete Row Button
        def _deleteRow(table):
            if table == 'Allocation':
                deleteRowWindow = TableAllocation()
                deleteRowWindow.deleteAllocation()

            if table == 'Income':
                deleteRowWindow = TableIncomes()
                deleteRowWindow.deleteIncomes()
            
            if table == 'Expense':
                deleteRowWindow = TableExpenses()
                deleteRowWindow.deleteExpenses()
            
            if table == 'Cat_Incomes':
                deleteRowWindow = TableIncomesCategories()
                deleteRowWindow.deleteCatIncomes()
                
            if table == 'Regular_Incomes':
                deleteRowWindow = TableRegularIncomes()
                deleteRowWindow.deleteRegularIncomes()

            if table == 'Cat_Expenses':
                deleteRowWindow = TableExpensesCategories()
                deleteRowWindow.deleteCatExpenses()
                
            if table == 'Regular_Expenses':
                deleteRowWindow = TableRegularExpenses()
                deleteRowWindow.deleteRegularExpenses()
            
            if table == 'Currencies':
                deleteRowWindow = TableCurrency()
                deleteRowWindow.deleteRegCurrency()

        
        self.winMain.ui.pushButton_DeleteAllocation.clicked.connect(lambda: _deleteRow('Allocation')) 
        self.winMain.ui.pushButton_DeleteIncome.clicked.connect(lambda: _deleteRow('Income')) 
        self.winMain.ui.pushButton_DeleteExpense.clicked.connect(lambda: _deleteRow('Expense')) 
        self.winMain.ui.pushButton_DeleteIncomeCat.clicked.connect(lambda: _deleteRow('Cat_Incomes')) 
        self.winMain.ui.pushButton_DeleteRegIncome.clicked.connect(lambda: _deleteRow('Regular_Incomes')) 
        self.winMain.ui.pushButton_DeleteExpenseCat.clicked.connect(lambda: _deleteRow('Cat_Expenses'))
        self.winMain.ui.pushButton_DeleteRegExpense.clicked.connect(lambda: _deleteRow('Regular_Expenses')) 
        self.winMain.ui.pushButton_DeleteCurrency.clicked.connect(lambda: _deleteRow('Currencies')) 


        # +++
        # Button: Transfer Row Button
        def _transferRow(table):

            if table == 'Income':
                deleteRowWindow = TableIncomes()
                deleteRowWindow.transferIncomes()
            
            if table == 'Expense':
                deleteRowWindow = TableExpenses()
                deleteRowWindow.transferExpenses()
        
        self.winMain.ui.pushButton_TransferIncome.clicked.connect(lambda: _transferRow('Income')) 
        self.winMain.ui.pushButton_TransferExpense.clicked.connect(lambda: _transferRow('Expense')) 

        # +++
        # Button: Quit App
        def _quitApp():
            closeConn()
            sys.exit()
        
        self.winMain.ui.pushButton_Quit.clicked.connect(_quitApp)
