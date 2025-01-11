# ===========================================================================================
# Custom PF_MainWindow modification
# All that is not done directly in QT Designer
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries


# PyQt Windows libraries
from PyQt6 import QtCore, QtGui

# App Specific libraries
import globals
from ui_format.ui_stylesheet import styleButtonWithImage, setWindowStyle, setTable
from util.get_translation import getTranslation

# =========================================================


# Format the UI of the WinMain
class WinMainUi:
    def __init__(self, WinMain):
        self.winMain = WinMain

    def modufyUI(self):
        self.setLanguage()
        self.windowStylesheets()
        self.windowIcons()
        self.setDataTablesStyle()
        self.setOtherItems()

        # show first tab - Allocation
        self.winMain.ui.tabWidget_Main.setCurrentIndex(0)

    # +++++++++++++++++++++++++++
    # Setup current window language
    # +++++++++++++++++++++++++++
    def setLanguage(self):
        # Setup window language
        language = globals.app_language
        langFile = getTranslation()


        # Windows
        self.winMain.setWindowTitle(langFile[language]["main_window_title"])

        #
        #
        # Balance window
        #
        #

        self.winMain.ui.tabWidget_Main.setTabText(
            0, langFile[language]["tabWidget_Main_tab_0"]
        )
        self.winMain.ui.tabWidget_Main.setTabText(
            1, langFile[language]["tabWidget_Main_tab_1"]
        )
        self.winMain.ui.tabWidget_Main.setTabText(
            2, langFile[language]["tabWidget_Main_tab_2"]
        )

        # Balance
        self.winMain.ui.label_Available.setText(langFile[language]["label_Available"])
        self.winMain.ui.label_Balance.setText(langFile[language]["label_Balance"])
        self.winMain.ui.label_Money_Check.setText(
            langFile[language]["label_Money_Check"]
        )

        # Allocation TAB
        self.winMain.ui.label_Unavailable.setText(
            langFile[language]["label_Unavailable"]
        )
        self.winMain.ui.label_EUR.setText(langFile[language]["label_EUR"])
        self.winMain.ui.label_NonEUR.setText(langFile[language]["label_NonEUR"])

        # Incomes TAB
        self.winMain.ui.label_Income_Total.setText(
            langFile[language]["label_Income_Total"]
        )
        self.winMain.ui.label_Income_Received.setText(
            langFile[language]["label_Income_Received"]
        )
        self.winMain.ui.label_Income_Opened.setText(
            langFile[language]["label_Income_Opened"]
        )

        # Expenses TAB
        self.winMain.ui.label_Expense_Total.setText(
            langFile[language]["label_Expense_Total"]
        )
        self.winMain.ui.label_Expense_Paid.setText(
            langFile[language]["label_Expense_Paid"]
        )
        self.winMain.ui.label_Expense_Opened.setText(
            langFile[language]["label_Expense_Opened"]
        )


        #
        #
        # Registires window
        #
        #
        self.winMain.ui.label_IncomesRegistry.setText(langFile[language]["label_IncomesRegistry"])
 
        self.winMain.ui.tabWidget_IncomesRegistry.setTabText(
            0, langFile[language]["tabWidget_IncomesRegistry_tab_0"]
        )
        self.winMain.ui.tabWidget_IncomesRegistry.setTabText(
            1, langFile[language]["tabWidget_IncomesRegistry_tab_1"]
        )

        
        self.winMain.ui.label_ExpensesRegistry.setText(langFile[language]["label_ExpensesRegistry"])

        self.winMain.ui.tabWidget_ExpensesRegistry.setTabText(
            0, langFile[language]["tabWidget_ExpensesRegistry_tab_0"]
        )
        self.winMain.ui.tabWidget_ExpensesRegistry.setTabText(
            1, langFile[language]["tabWidget_ExpensesRegistry_tab_1"]
        )



        self.winMain.ui.label_MoneyCorrection.setText(
            langFile[language]["label_MoneyCorrection"]
        )

        self.winMain.ui.label_Currencies.setText(langFile[language]["label_Currencies"])

    # +++++++++++++++++++++++++++
    # Setup current window stylesheets
    # +++++++++++++++++++++++++++
    def windowStylesheets(self):

        setWindowStyle(self.winMain)

        styleButtonWithImage(self.winMain.ui.pushButton_Main)
        styleButtonWithImage(self.winMain.ui.pushButton_Registries)
        styleButtonWithImage(self.winMain.ui.pushButton_Settings)
        styleButtonWithImage(self.winMain.ui.pushButton_Quit)

    # +++++++++++++++++++++++++++
    # Setup current window icons
    # +++++++++++++++++++++++++++
    def windowIcons(self):
        iconsPath = globals.root_path

        def _setIcon(item, iconName, iconSize):
            # Set Icons Path and Name
            iconFullName = iconsPath + iconName

            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconFullName),
                QtGui.QIcon.Mode.Normal,
                QtGui.QIcon.State.Off,
            )

            item.setIcon(icon)
            item.setIconSize(iconSize)

        iconSize = QtCore.QSize(36, 36)

        iconName = "/Custom_Icons/WinSavings.png"
        iconItem = self.winMain.ui.pushButton_Main
        _setIcon(iconItem, iconName, iconSize)

        iconName = "/Custom_Icons/WinIncomeCategories.png"
        iconItem = self.winMain.ui.pushButton_Registries
        _setIcon(iconItem, iconName, iconSize)

        iconName = "/Custom_Icons/WinSavingsCrypto.png"
        iconItem = self.winMain.ui.pushButton_Settings
        _setIcon(iconItem, iconName, iconSize)

        iconName = "/Custom_Icons/exitApp.png"
        iconItem = self.winMain.ui.pushButton_Quit
        _setIcon(iconItem, iconName, iconSize)

        iconSize = QtCore.QSize(32, 32)

        iconName = "/Custom_Icons/AddRow.png"

        iconItem = self.winMain.ui.pushButton_AddAllocation
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddIncome
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddExpense
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddIncomeCat
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddRegIncome
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddExpenseCat
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddRegExpense
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_AddCurrency
        _setIcon(iconItem, iconName, iconSize)

        iconName = "/Custom_Icons/DeleteRow.png"

        iconItem = self.winMain.ui.pushButton_DeleteAllocation
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteIncome
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteExpense
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteIncomeCat
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteRegIncome
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteExpenseCat
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteRegExpense
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.pushButton_DeleteCurrency
        _setIcon(iconItem, iconName, iconSize)

        iconItem = self.winMain.ui.labelAvailableIcon
        iconName = iconsPath + "/Custom_Icons/AvailableMoney.png"
        iconItem.setPixmap(QtGui.QPixmap(iconName))

        iconItem = self.winMain.ui.labelBalanceIcon
        iconName = iconsPath + "/Custom_Icons/Balance.png"
        iconItem.setPixmap(QtGui.QPixmap(iconName))

        iconItem = self.winMain.ui.labelMoneyCheckIcon
        iconName = iconsPath + "/Custom_Icons/MoneyCheck.png"
        iconItem.setPixmap(QtGui.QPixmap(iconName))


    # +++++++++++++++++++++++++++
    # Setup all tables
    # +++++++++++++++++++++++++++
    def setDataTablesStyle(self):
        #for table in globals.tableDict.values():
            #setTable(table)

        setTable(self.winMain.ui.tableView_Allocation)

    # +++++++++++++++++++++++++++
    # Setup other items
    # +++++++++++++++++++++++++++
    def setOtherItems(self):
        
        windowTitleColor = globals.windowTitleColor
        self.winMain.ui.label_Available.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Balance.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Money_Check.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_IncomesRegistry.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_ExpensesRegistry.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_MoneyCorrection.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Currencies.setStyleSheet(f"color: rgb({windowTitleColor});")

        
        self.winMain.ui.label_Unavailable.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_EUR.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_NonEUR.setStyleSheet(f"color: rgb({windowTitleColor});")

        self.winMain.ui.label_Income_Total.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Income_Received.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Income_Opened.setStyleSheet(f"color: rgb({windowTitleColor});")

        self.winMain.ui.label_Expense_Total.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Expense_Paid.setStyleSheet(f"color: rgb({windowTitleColor});")
        self.winMain.ui.label_Expense_Opened.setStyleSheet(f"color: rgb({windowTitleColor});")

        labelMonthRGBColor = globals.tabMonthLabel
        self.winMain.ui.label_Month.setStyleSheet(f"color: rgb({labelMonthRGBColor});")

        labelYearRGBColor = globals.tabYearLabel
        self.winMain.ui.label_Year.setStyleSheet(f"color: rgb({labelYearRGBColor});")

        if globals.app_db != "mysqlDB_dev":
            self.winMain.ui.label_Demo.setVisible(False)
