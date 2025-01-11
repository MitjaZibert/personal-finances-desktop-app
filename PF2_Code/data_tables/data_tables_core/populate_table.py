# ===========================================================================================
# DB related class for Main Window
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries

# PyQt Windows libraries

# App Specific libraries
from util import getMonthName
from data_modules import DB_Util
from .get_query_parameters import getQueryParameters
from data_tables.data_tables_core.table_model import TableModel
from data_tables.data_tables_core import formatTable
from data_tables.table_balance import TableBalance
import data_modules.data_calculations as data_calculations

# =========================================================
# +++++++++++++++++++++++++++
# Check if current data needs additional editing before set in table (e.g. convert month number into a month name)
# !! data_tables - list of lists - gets updated
# +++++++++++++++++++++++++++  
def _preTableModelGen(table, data_tables):

    if table.tableObject.objectName() == 'tableView_Balance':

        # convert month number into a month name    
        i = 0
        for mon in data_tables:
            monthName = getMonthName(mon[1])
            data_tables[i][1] = monthName
            i += 1

    if table.tableObject.objectName() == 'tableView_Money_Correction':

        # convert month number into a month name    
        i = 0
        for mon in data_tables:
            monthName = getMonthName(mon[2])
            data_tables[i][2] = monthName
            i += 1  
    
# +++++++++++++++++++++++++++
# Populate Table Viwes with data
# +++++++++++++++++++++++++++  
def populateTable(table, setRowFocus = True):
    #print(table.tableObject.objectName())

    table.tableObject.blockSignals(True)
    
    db = DB_Util()
    
    # check if query accepts any argumnets
    args = None
    if table.query_args:
        args = getQueryParameters(table)
    
    # get query result
    dbCurr = db.getData(table.query, args)
    dbTuple = dbCurr.fetchall()
    dataList = [list(tup) for tup in dbTuple]
    tableData = list(dataList)

    #Check if current tableview needs pre-editing
    _preTableModelGen(table, tableData)

    # Set data to the table view - populate table
    tableModel = TableModel(tableData, table)
    table.tableModel = tableModel
    table.tableObject.setModel(tableModel)

    #Check if current tableview needs additional settings
    _postTableModelGen(table, tableData, setRowFocus)

    table.tableObject.blockSignals(False)

# +++++++++++++++++++++++++++
# Check if current tableview additional editing after set in table (e.g. set data_tables)
# +++++++++++++++++++++++++++  
def _postTableModelGen(table, data_tables, setRowFocus):
    from data_tables.data_tables_core import tableHeaders

    def _get_combo_data(query):
        # get query result
        db = DB_Util()
        dbCurr = db.getData(query)
        dbRows = dbCurr.fetchall()

        comboList = [] # used in combobox delegate
        comboDict = {} # used for pairing selected value from combo with its key (ID)
        for key, value in dbRows:
            comboDict[key] = value
            comboList.append(value)

        return comboDict, comboList


    if table.tableObject.objectName() == 'tableView_Balance':
        from data_tables.table_balance import TableBalance

        tableBalance = TableBalance(table)
        # table model functionality
        tableBalance.tableBalanceFunctionality()
        #Initialize app data (e.g. current year/month)
        tableBalance.setCurrentMonthRow(setFocus=setRowFocus)
    

    if table.tableObject.objectName() == 'tableView_Allocation':   
        from data_tables.table_allocation import TableAllocation

        tableAllocation = TableAllocation()        
        # set combobox for currency
        tableAllocation.comboBoxDelegate()
        # table model functionality
        tableAllocation.tableAllocationFunctionality()

        data_calculations.recalculateAmounts()

    
    if table.tableObject.objectName() == 'tableView_Incomes':
        from data_tables.table_incomes import TableIncomes

        tableIncomes = TableIncomes()
        # table model functionality
        tableIncomes.tableIncomesFunctionality()

        data_calculations.recalculateAmounts()


    if table.tableObject.objectName() == 'tableView_Expenses':
        from data_tables.table_expenses import TableExpenses
        
        tableExpenses = TableExpenses()
        # table model functionality
        tableExpenses.tableExpensesFunctionality()

        data_calculations.recalculateAmounts()


    if table.tableObject.objectName() == 'tableView_Income_Categories':
        from data_tables.table_cat_incomes import TableIncomesCategories

        tableIncomesCategories = TableIncomesCategories()

        # table model functionality
        tableIncomesCategories.tableIncomesCategoriesFunctionality()

        
    if table.tableObject.objectName() == 'tableView_Regular_Incomes':
        from data_tables.table_regular_incomes import TableRegularIncomes

        tableRegularIncomes = TableRegularIncomes()     
        # set combobox for inc_category
        tableRegularIncomes.comboBoxDelegate()
        # table model functionality
        tableRegularIncomes.tableRegularIncomesFunctionality()


    if table.tableObject.objectName() == 'tableView_Expense_Categories':
        from data_tables.table_cat_expenses import TableExpensesCategories

        tableExpensesCategories = TableExpensesCategories()
        # table model functionality
        tableExpensesCategories.tableExpensesCategoriesFunctionality()

    
    if table.tableObject.objectName() == 'tableView_Regular_Expenses':    
        from data_tables.table_regular_expenses import TableRegularExpenses
        
        tableRegularExpenses = TableRegularExpenses()
        # set combobox for inc_category
        tableRegularExpenses.comboBoxDelegate()
        # table model functionality
        tableRegularExpenses.tableRegularExpensesFunctionality()

        
    if table.tableObject.objectName() == 'tableView_Currency':
        from data_tables.table_currencies import TableCurrency

        tableCurrencies = TableCurrency()
        # table model functionality
        tableCurrencies.tableCurrenciesFunctionality()

    
    if table.tableObject.objectName() == 'tableView_Money_Correction':
        from data_tables.table_money_correction import TableMoneyCorrection
        
        tableMoneyCorrection = TableMoneyCorrection()
        #Initialize app data (e.g. current year/month)
        tableMoneyCorrection.setCurrentMonthRow(setFocus=True)
        # table model functionality
        tableMoneyCorrection.tableMoneyCorrectionFunctionality()
        


    # Set headers for data table
    tableHeaders(table)

    # Format data table
    formatTable(table)

