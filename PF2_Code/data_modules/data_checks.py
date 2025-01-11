# ===========================================================================================
# Calculations
# 
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries
import datetime

# PyQt Windows libraries

# App Specific libraries
from data_modules import DB_Util

# =========================================================

class DataCheck():
    def __init__(self):

        self.db = DB_Util()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++
    # Check if NEW MONTH needs to be added to incomes and expenses
    #++++
    def checkNewMonth(self):
        def addNewMonth(year, month):
            # ===== INCOMES =====
            insertStmt = "INSERT INTO INCOMES_SUM ( YEAR, MONTH, INC_ALL_SUM, INC_RECEIVED_SUM, INC_OPEN_SUM, CLOSED) VALUES (" + str(year) + ", " + str(month) + ",0,0,0,0)"
            self.db.executeDDL(ddl=insertStmt)
            
            query = "SELECT max(INCOMES_SUM_ID) from INCOMES_SUM"
            data = self.db.getData(query).fetchone()
            incSumID = data[0]

            insertStmt = """INSERT INTO INCOMES (INCOMES_SUM_ID, INC_CATEGORY_ID, INCOME, AMOUNT_ALL, AMOUNT_RECEIVED, AMOUNT_OPEN, REGULAR_INCOME_ID, UPDATE_REGULAR_INCOME) 
                            SELECT """ + str(incSumID) + ", INC_CATEGORY_ID, REGULAR_INCOME, AMOUNT, 0.0, AMOUNT, REGULAR_INCOME_ID, 1 FROM REG_REGULAR_INCOMES"
            self.db.executeDDL(ddl=insertStmt)
            
            # ===== EXPENSES =====
            insertStmt = "INSERT INTO EXPENSES_SUM (YEAR, MONTH, EXP_ALL_SUM, EXP_PAYED_SUM, EXP_OPEN_SUM, CLOSED) VALUES (" + str(year) + ", " + str(month) + ",0,0,0,0)"
            self.db.executeDDL(ddl=insertStmt)
            
            query = "SELECT max(EXPENSES_SUM_ID) from EXPENSES_SUM"
            data = self.db.getData(query).fetchone()
            expSumID = data[0]

            self.db.callDBProc(proc_name='insert_new_month_expenses', inParam1=expSumID)

            # ===== MONEY CORRECTION =====
            insertStmt = "INSERT INTO MONEY_CORRECTION (YEAR, MONTH, AMOUNT) VALUES (" + str(year) + ", " + str(month) + ", 0)"
            self.db.executeDDL(ddl=insertStmt)
            
            
            
        # +++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++ 
        # +++++++++++++++++++++++++++

        

        query = "SELECT CAST(max(YEAR) as INTEGER) AS year, CAST(max(MONTH) as INTEGER) AS month FROM INCOMES_SUM WHERE year = (SELECT max(YEAR) AS year FROM INCOMES_SUM) "
        data = self.db.getData(query).fetchone()
        currMaxYear = data[0]
        currMaxMonth = data[1]
        
        date = datetime.datetime.today()
        currYear = date.year
        currMonth = date.month

        newYear = 0
        newMonth = 0

        monthsAdded = False 

        if currMaxYear == currYear: # if the projection is behind more than one month
            if currMaxMonth == 12:
                newYear = currMaxYear + 1
                newMonth = 1
            else:
                newYear = currMaxYear
                newMonth = currMaxMonth + 1
        
            addNewMonth(newYear, newMonth)
            monthsAdded = True

        elif currMaxYear > currYear and currMaxMonth < currMonth:
            newYear = currMaxYear
            newMonth = currMaxMonth + 1
            
            addNewMonth(newYear, newMonth)
            monthsAdded = True

        # if a new month was added, redistribute savings amount to all future months
        if monthsAdded == True:
            self.db.saveData()


    # +++++++++++++++++++++++++++
    # Check any irregularities
    #++++
    def checkDBIrregularities(self):

        updateStmt = "UPDATE INCOMES SET UPDATE_REGULAR_INCOME = 0 where UPDATE_REGULAR_INCOME = 1 and REGULAR_INCOME_ID is null"
        self.db.executeDDL(ddl=updateStmt)

        updateStmt = "UPDATE EXPENSES SET UPDATE_REGULAR_EXPENSE = 0 where UPDATE_REGULAR_EXPENSE = 1 and REGULAR_EXPENSE_ID is null"
        self.db.executeDDL(ddl=updateStmt)
        
        self.db.saveData()