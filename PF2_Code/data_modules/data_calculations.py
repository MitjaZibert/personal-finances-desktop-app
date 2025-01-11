# ===========================================================================================
# Calculations
# 
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries

# PyQt Windows libraries

# App Specific libraries
import globals
from data_modules import DB_Util
from util.get_translation import getTranslation
from util import getMonthInt
from ui_format.ui_stylesheet import fontColor

# =========================================================

#+++++++++++++++++++++++++++
# # Recalculate SUM Amounts
#++++

def recalculateAmounts():

    # Setup window language
    language = globals.app_language
    langFile = getTranslation()

    db = DB_Util()

    # Get current year/month for this expense
    tableBalanceData = globals.tableDict["tableView_Balance"]
    itemIndex = tableBalanceData.tableObject.selectionModel().currentIndex()

    year = tableBalanceData.tableObject.model().index(itemIndex.row(), 0).data()
    monthName = tableBalanceData.tableObject.model().index(itemIndex.row(), 1).data()
    month = getMonthInt(monthName)

    
    #+++++++++++++++++++++++++++
    # Balance Table
    #+++++++++++++++++++++++++++

    # ---------------------------------------------------------------------------------------------------------
    # Total available money
    # ---------------------------------------------------------------------------------------------------------
    query = "SELECT SUM(VALUE) FROM MONEY_ALLOCATION WHERE AVAILABLE = 2"
    data = db.getData(query)
    value = data.fetchone()
    availableMoney = value[0]
    
    globals.mainWinClass.ui.label_Available_Amount.setText(str(availableMoney))
    fontColor(globals.mainWinClass.ui.label_Available_Amount, availableMoney)

    # ---------------------------------------------------------------------------------------------------------
    # Calculate how much is missing from current month's money allocation to cover current month's expenses
    # ---------------------------------------------------------------------------------------------------------
    #query = "SELECT (EXP.EXP_OPEN_SUM + SAV.SAVED) EXP FROM EXPENSES_SUM EXP INNER JOIN SAVINGS_SUM SAV ON EXP.YEAR = SAV.YEAR AND EXP.MONTH = SAV.MONTH WHERE EXP.year = YEAR(CURDATE()) and EXP.month = MONTH(CURDATE())"
    
    query = "SELECT EXP_OPEN_SUM FROM EXPENSES_SUM WHERE year = YEAR(CURDATE()) and month = MONTH(CURDATE())"
    data = db.getData(query)
    value = data.fetchone()
    amount = value[0]

    balance = round((availableMoney - amount), 2)
    globals.mainWinClass.ui.label_Balance_Amount.setText(str(balance))
    fontColor(globals.mainWinClass.ui.label_Balance_Amount, balance)
    
    # ---------------------------------------------------------------------------------------------------------
    # Calculate Money Check
    # ---------------------------------------------------------------------------------------------------------
    
    query = """SELECT (EXP_SUM + ALLOC) -  INC_SUM + CORRECTION AS MONEY_CHECK FROM 
            (SELECT SUM(VALUE) ALLOC FROM MONEY_ALLOCATION) AL, 
            (SELECT SUM(INC_RECEIVED_SUM) INC_SUM
            FROM (SELECT INC_RECEIVED_SUM, (CONCAT(ES.YEAR, LPAD(ES.MONTH, 2, 0))) AS INC_DATE FROM INCOMES_SUM ES) I 
            WHERE INC_DATE <= (SELECT CONCAT(YEAR(CURDATE()), LPAD(MONTH(CURDATE()), 2, 0)))) INC,
            (SELECT SUM(EXP_PAYED_SUM) EXP_SUM
            FROM (SELECT EXP_PAYED_SUM, (CONCAT(ES.YEAR, LPAD(ES.MONTH, 2, 0))) AS EXP_DATE FROM EXPENSES_SUM ES) E 
            WHERE EXP_DATE <= (SELECT CONCAT(YEAR(CURDATE()), LPAD(MONTH(CURDATE()), 2, 0)))) EXP,
            (SELECT SUM(AMOUNT) CORRECTION
            FROM (SELECT AMOUNT, (CONCAT(MC.YEAR, LPAD(MC.MONTH, 2, 0))) AS CORR_DATE FROM MONEY_CORRECTION MC) M 
            WHERE CORR_DATE <= (SELECT CONCAT(YEAR(CURDATE()), LPAD(MONTH(CURDATE()), 2, 0)))) CORR"""
    
    data = db.getData(query)
    value = data.fetchone() 
    checkSum = round(value[0], 2)


    query = "SELECT CURRENCY_CHECK_SUM FROM REG_SYS_VARIABLES"
    data = db.getData(query)
    value = data.fetchone()
    currencyCheck = round(value[0], 2)
    
    moneyCheck = round((checkSum + currencyCheck), 2)

    globals.mainWinClass.ui.label_Money_Check_Amount.setText(str(moneyCheck))
    fontColor(globals.mainWinClass.ui.label_Money_Check_Amount, moneyCheck)

    moneyCheckLabel = langFile[language]['label_Money_Check']
    globals.mainWinClass.ui.label_Money_Check.setText(moneyCheckLabel + " ("+str(currencyCheck)+"€):")
    


    #+++++++++++++++++++++++++++
    # Tab: Allocation
    #+++++++++++++++++++++++++++

    # Available money in EUR
    query = "SELECT SUM(VALUE) FROM MONEY_ALLOCATION WHERE AVAILABLE = 2 AND CURR_ID = 1"
    data = db.getData(query)
    value = data.fetchone()
    amount = value[0]
    
    globals.mainWinClass.ui.label_EUR_Amount.setText(str(amount))
    fontColor(globals.mainWinClass.ui.label_EUR_Amount, amount)

    # Total unavailable money
    query = "SELECT SUM(VALUE) FROM MONEY_ALLOCATION WHERE AVAILABLE = 0"
    data = db.getData(query)
    value = data.fetchone()
    amount = value[0]
    
    globals.mainWinClass.ui.label_Unavailable_Amount.setText(str(amount))
    fontColor(globals.mainWinClass.ui.label_Unavailable_Amount, amount)

    # Total money in other than EUR
    query = "SELECT SUM(VALUE) FROM MONEY_ALLOCATION WHERE CURR_ID != 1"
    data = db.getData(query)
    value = data.fetchone()
    amount = value[0]
    
    globals.mainWinClass.ui.label_NonEUR_Amount.setText(str(amount))
    fontColor(globals.mainWinClass.ui.label_NonEUR_Amount, amount)

    

    #+++++++++++++++++++++++++++
    # Tab: Incomes
    #+++++++++++++++++++++++++++

    if year:
        query = "SELECT INC_ALL_SUM, INC_RECEIVED_SUM, INC_OPEN_SUM FROM INCOMES_SUM WHERE YEAR = " + str(year) + " and MONTH = " +str(month)
        data = db.getData(query)
        inc_sum = data.fetchone()

        income_Total_Amount = inc_sum[0]
        income_Received_Amount = inc_sum[1]
        income_Opened_Amount = inc_sum[2]

        globals.mainWinClass.ui.label_Income_Total_Amount.setText(str(income_Total_Amount))
        globals.mainWinClass.ui.label_Income_Received_Amount.setText(str(income_Received_Amount))
        globals.mainWinClass.ui.label_Income_Opened_Amount.setText(str(income_Opened_Amount))

    #+++++++++++++++++++++++++++
    # Tab: Expenses
    #+++++++++++++++++++++++++++

    if year:
        query = "SELECT EXP_ALL_SUM, EXP_PAYED_SUM, EXP_OPEN_SUM FROM EXPENSES_SUM WHERE YEAR = " + str(year) + " and MONTH = " +str(month)
        data = db.getData(query)
        exp_sum = data.fetchone()

        expense_Total_Amount = exp_sum[0]
        expense_Paid_Amount = exp_sum[1]
        expense_Opened_Amount = exp_sum[2]

        globals.mainWinClass.ui.label_Expense_Total_Amount.setText(str(expense_Total_Amount))
        globals.mainWinClass.ui.label_Expense_Paid_Amount.setText(str(expense_Paid_Amount))
        globals.mainWinClass.ui.label_Expense_Opened_Amount.setText(str(expense_Opened_Amount))

