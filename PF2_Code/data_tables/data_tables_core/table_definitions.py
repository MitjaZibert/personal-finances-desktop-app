
# PyQt Windows libraries

# App Specific libraries
from data_tables.data_tables_core import Table
from data_tables.data_tables_core import TableModel


# All data tables definitions
def tableDefinitions(windowClass, tableDict):
    
    # Name of the Window Class
    className = type(windowClass).__name__

    # Tables for WinMain window class
    if className == "WinMain":
        # tableView_Balance: Monthly balance
        tableDict["tableView_Balance"] = Table(tableObject = windowClass.ui.tableView_Balance,
                                        tableModel = TableModel,
                                        db_columns = ["year", "month", "", "", "", "", "", "", "", "", ""],
                                        query = """SELECT I.YEAR YEAR, I.MONTH MONTH, 
                                                    I.INC_ALL_SUM INC_ALL, I.INC_RECEIVED_SUM INC_RECEIVED, I.INC_OPEN_SUM INC_OPEN,
                                                    E.EXP_ALL_SUM EXP_ALL, E.EXP_PAYED_SUM EXP_PAYED, E.EXP_OPEN_SUM EXP_OPEN, 
                                                        M.AMOUNT CORRECTION, 
                                                        (I.INC_ALL_SUM  - E.EXP_ALL_SUM) AS BALANCE, 
                                                        SUM(I.INC_ALL_SUM  - E.EXP_ALL_SUM) OVER (ORDER BY I.YEAR, I.MONTH) AS TURNOVER,
                                                        I.CLOSED
                                                FROM INCOMES_SUM I
                                                INNER JOIN EXPENSES_SUM E ON I.YEAR = E.YEAR AND I.MONTH = E.MONTH
                                                INNER JOIN MONEY_CORRECTION M ON I.YEAR = M.YEAR AND I.MONTH = M.MONTH
                                                ORDER BY I.YEAR, I.MONTH asc;""",
                                  query_args = [],
                                  geometry= [10, 10, 858, 270],
                                  columnWidths=[50, 80, 70, 70, 80, 70, 70, 70, 70, 70, 70, 40],
                                  tableEnabled = True,
                                  columnEditable=[False, False, False, False, False, False, False, False, False, False, False, True],
                                  roundedNumber=[0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                                  columnCheckBox=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                                  )

        # tableView_Allocation: Money Allocation data
        tableDict["tableView_Allocation"] = Table(tableObject = windowClass.ui.tableView_Allocation,
                                    tableModel = TableModel,
                                  db_columns = ["alloc_id", "curr_id", "allocation", "alloc_amount", "curr_code", "value", "alloc_desc", "available"],
                                  query = """SELECT M.ALLOC_ID, C.CURR_ID, M.ALLOCATION, M.ALLOC_AMOUNT, C.CURR_CODE, M.VALUE, M.ALLOC_DESC, M.AVAILABLE 
                                                    FROM MONEY_ALLOCATION M
                                                    INNER JOIN REG_CURRENCY C ON M.CURR_ID = C.CURR_ID 
                                                    ORDER BY M.AVAILABLE DESC, M.VALUE DESC, M.ALLOCATION;""",
                                  query_args = [],
                                  geometry= [10, 10, 600, 270],
                                  columnWidths=[0, 0, 130, 70, 70, 70, 170, 40],
                                  tableEnabled = True,
                                  columnEditable=[True, True, True, True, True, False, True, True],
                                  roundedNumber=[0, 0, 0, 2, 0, 2, 0, 0],
                                  columnCheckBox=[0, 0, 0, 0, 0, 0, 0, 1]
                                  )

        # tableView_Incomes: Incomes monthly data
        tableDict["tableView_Incomes"] = Table(tableObject = windowClass.ui.tableView_Incomes,
                                    tableModel = TableModel,
                                    db_columns = ["incomes_sum_id", "income_id", "inc_category", "income", "notes", "amount_all", "amount_recieved", "amount_open", "correction", "update_regular_income", "regular_income_id"],
                                  query = """SELECT I.INCOMES_SUM_ID, INCOME_ID, C.INC_CATEGORY, INCOME, IFNULL(NOTES, ""), 
                                                    AMOUNT_ALL, AMOUNT_RECEIVED, AMOUNT_OPEN, 0 AS CORRECTION, 
                                                    UPDATE_REGULAR_INCOME, REGULAR_INCOME_ID
                                                    FROM INCOMES I
                                                    INNER JOIN INCOMES_SUM S
                                                    ON I.INCOMES_SUM_ID = S.INCOMES_SUM_ID
                                                    INNER JOIN REG_INCOME_CATEGORIES C 
                                                    ON I.INC_CATEGORY_ID = C.INC_CATEGORY_ID 
                                                    AND S.YEAR = %(year)s AND S.MONTH = %(month)s 
                                                    ORDER BY INCOME_ID""",
                                    query_args = ['year', 'month'],
                                    geometry= [10, 10, 905, 270],
                                    columnWidths=[0, 0, 170, 180, 180, 70, 70, 70, 70, 50, 0],
                                    tableEnabled = True,
                                    columnEditable=[False, False, False, True, True, True, False, False, True, True, False],
                                    roundedNumber=[0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
                                    columnCheckBox=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
                                    )

        # tableView_Expenses: Expenses monthly data
        tableDict["tableView_Expenses"] = Table(tableObject = windowClass.ui.tableView_Expenses,
                                tableModel = TableModel,
                                  db_columns = ["expenses_sum_id", "expense_id", "exp_category", "expense", "notes", "amount_all", "amount_payed", "amount_open", "correction", "update_regular_expense", "regular_expense_id"],
                                query = """SELECT E.EXPENSES_SUM_ID, EXPENSE_ID, C.EXP_CATEGORY, EXPENSE, IFNULL(NOTES, ""), 
                                                    AMOUNT_ALL, AMOUNT_PAYED, AMOUNT_OPEN, 0 AS CORRECTION, 
                                                    UPDATE_REGULAR_EXPENSE, REGULAR_EXPENSE_ID 
                                                    FROM EXPENSES E
                                                    INNER JOIN EXPENSES_SUM SE
                                                    ON E.EXPENSES_SUM_ID = SE.EXPENSES_SUM_ID
                                                    INNER JOIN REG_EXPENSE_CATEGORIES C 
                                                    ON E.EXP_CATEGORY_ID = C.EXP_CATEGORY_ID 
                                                    AND SE.YEAR = %(year)s AND SE.MONTH = %(month)s    
                                                    ORDER BY -REGULAR_EXPENSE_ID DESC, EXPENSE""",
                                  query_args = ['year', 'month'],
                                  geometry= [10, 10, 905, 270],
                                  columnWidths=[0, 0, 170, 180, 180, 70, 70, 70, 70, 50, 0],
                                  tableEnabled = True,
                                  columnEditable=[False, False, False, True, True, True, False, False, True, True, False],
                                  roundedNumber=[0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
                                  columnCheckBox=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
                                  )
        
        # tableView_Income_Categories: Reg Income Categories data
        tableDict["tableView_Income_Categories"] = Table(tableObject = windowClass.ui.tableView_Income_Categories,
                                    tableModel = TableModel,
                                  db_columns = ["inc_category_id", "inc_category", "inc_cat_desc"],
                                  query = """SELECT inc_category_id, inc_category, inc_cat_desc 
                                                FROM REG_INCOME_CATEGORIES
                                                ORDER BY inc_category_id ASC""",
                                  query_args = [],
                                  geometry= [10, 10, 830, 271],
                                  columnWidths=[0, 200, 587],
                                  tableEnabled = True,
                                  columnEditable=[False, True, True],
                                  roundedNumber=[0, 0, 0],
                                  columnCheckBox=[0, 0, 0]
                                  )
        
        # tableView_Regular_Incomes: Reg Regular Incomes data
        tableDict["tableView_Regular_Incomes"] = Table(tableObject = windowClass.ui.tableView_Regular_Incomes,
                                    tableModel = TableModel,
                                  db_columns = ["regular_income_id", "inc_category_id", "inc_category", "regular_income", "amount"],
                                  query = """SELECT RI.REGULAR_INCOME_ID, RI.INC_CATEGORY_ID, IC.INC_CATEGORY, RI.REGULAR_INCOME, RI.AMOUNT  
                                                FROM REG_REGULAR_INCOMES AS RI
                                                INNER JOIN REG_INCOME_CATEGORIES IC ON RI.INC_CATEGORY_ID = IC.INC_CATEGORY_ID
                                                ORDER BY RI.REGULAR_INCOME_ID ASC""",
                                  query_args = [],
                                  geometry= [10, 10, 830, 271],
                                  columnWidths=[0, 0, 200, 517, 70],
                                  tableEnabled = True,
                                  columnEditable=[False, False, True, True, True],
                                  roundedNumber=[0, 0, 0, 0, 2],
                                  columnCheckBox=[0, 0, 0, 0, 0]
                                  )
        
        # tableView_Expense_Categories: Reg Expense Categories data
        tableDict["tableView_Expense_Categories"] = Table(tableObject = windowClass.ui.tableView_Expense_Categories,
                                    tableModel = TableModel,
                                  db_columns = ["exp_category_id", "exp_category", "exp_cat_desc"],
                                  query = """SELECT exp_category_id, exp_category, exp_cat_desc 
                                                FROM REG_EXPENSE_CATEGORIES
                                                ORDER BY exp_category_id ASC""",
                                  query_args = [],
                                  geometry= [10, 10, 830, 271],
                                  columnWidths=[0, 200, 587],
                                  tableEnabled = True,
                                  columnEditable=[False, True, True],
                                  roundedNumber=[0, 0, 0],
                                  columnCheckBox=[0, 0, 0]
                                  )
        
        # tableView_Regular_Expenses: Reg Regular Expenses data
        tableDict["tableView_Regular_Expenses"] = Table(tableObject = windowClass.ui.tableView_Regular_Expenses,
                                    tableModel = TableModel,
                                  db_columns = ["regular_expense_id", "exp_category_id", "exp_category", "regular_expense", "amount", "months"],
                                  query = """SELECT RE.REGULAR_EXPENSE_ID, RE.EXP_CATEGORY_ID, EC.EXP_CATEGORY, RE.REGULAR_EXPENSE, RE.AMOUNT , RE.MONTHS 
                                                FROM REG_REGULAR_EXPENSES AS RE
                                                INNER JOIN REG_EXPENSE_CATEGORIES EC ON RE.EXP_CATEGORY_ID = EC.EXP_CATEGORY_ID
                                                ORDER BY RE.REGULAR_EXPENSE_ID ASC""",
                                  query_args = [],
                                  geometry= [10, 10, 830, 271],
                                  columnWidths=[0, 0, 200, 317, 70, 200],
                                  tableEnabled = True,
                                  columnEditable=[False, False, True, True, True, True],
                                  roundedNumber=[0, 0, 0, 0, 2, 0],
                                  columnCheckBox=[0, 0, 0, 0, 0, 0]
                                  )
        
        # tableView_Money_Correction: Money Correction data
        tableDict["tableView_Money_Correction"] = Table(tableObject = windowClass.ui.tableView_Money_Correction,
                                    tableModel = TableModel,
                                  db_columns = ["money_correction_id", "year", "month", "amount", "notes"],
                                  query = """SELECT money_correction_id, year, month, amount, notes
                                                FROM MONEY_CORRECTION
                                                ORDER BY money_correction_id ASC""",
                                  query_args = [],
                                  geometry= [10, 50, 500, 180],
                                  columnWidths=[0, 50, 80, 70, 250],
                                  tableEnabled = True,
                                  columnEditable=[False, False, False, True, True],
                                  roundedNumber=[0, 0, 0, 2, 0],
                                  columnCheckBox=[0, 0, 0, 0, 0]
                                  )

        # tableView_Currency: Reg Currencies data
        tableDict["tableView_Currency"] = Table(tableObject = windowClass.ui.tableView_Currency,
                                    tableModel = TableModel,
                                  db_columns = ["curr_id", "curr_code", "curr_name", "curr_rate", "rate_date", "crypto"],
                                  query = """SELECT curr_id, curr_code, curr_name, curr_rate, rate_date, crypto
                                                FROM REG_CURRENCY
                                                ORDER BY curr_code ASC""",
                                  query_args = [],
                                  geometry= [10, 290, 565, 315],
                                  columnWidths=[0, 100, 200, 70, 100, 50],
                                  tableEnabled = True,
                                  columnEditable=[False, False, True, True, True, True],
                                  roundedNumber=[0, 0, 0, 0, 0, 0],
                                  columnCheckBox=[0, 0, 0, 0, 0, 1]
                                  )