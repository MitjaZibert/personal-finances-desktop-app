# ===========================================================================================
# Code specific to TableView Balance
#
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries


# PyQt Windows libraries
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QAbstractItemView
from PyQt6.QtCore import QItemSelectionModel

# App Specific libraries
import globals
from data_modules import DB_Util
from util import getMonthName
from util import getMonthInt
from ui_format import ui_stylesheet
from util.get_translation import getTranslation
from dialog_windows.dwin_close_month import DWin_Close_Month
from dialog_windows.dwin_alert import DWin_Alert

# =========================================================


# Code specific to TableView Balance
class TableBalance:
    def __init__(self, table):
        self.table = table

        self.tableData = globals.tableDict["tableView_Balance"]
        self.db = DB_Util()

        self.monthClosed = True

    # =========================================================
    # Main Window - Table Balance functionality
    #++++
    def tableBalanceFunctionality(self):
        from data_tables.data_tables_core.populate_table import populateTable

        
        self.dataBalance = TableBalance(self.table)

        # Signal and function for row change in tableView_Balance
        # Refresh data in tableView_Incomes and tableView_Expenses
        def _rowChanged():
            
            if globals.activeWidget == "tableView_Balance":
                
                clickedItemIndex = self.tableData.tableObject.currentIndex()
                
                # set currently selected year and month row
                globals.selected_year = self.tableData.tableObject.model().index(clickedItemIndex.row(), 0).data()
                selected_month = self.tableData.tableObject.model().index(clickedItemIndex.row(), 1).data()
                selected_month_int = getMonthInt(selected_month)
                globals.selected_month = selected_month_int

                monthClosedIndex = self.tableData.tableObject.model().index(clickedItemIndex.row(), 11)
                monthClosed = monthClosedIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)
            
                tableIncomes = globals.tableDict["tableView_Incomes"]
                tableExpenses = globals.tableDict["tableView_Expenses"]
                
                tableIncomes.tableEnabled = True
                tableExpenses.tableEnabled = True
                
                if monthClosed == QtCore.Qt.CheckState.Checked:
                    tableIncomes.tableEnabled = False
                    tableExpenses.tableEnabled = False
                
                # refresh data in tableView_Incomes and tableView_Expenses
                populateTable(tableIncomes)
                populateTable(tableExpenses)



                # Set month and year in Incomes and Expenses TAB for the current year/month row
                globals.mainWinClass.ui.label_Month.setText(str(selected_month))
                globals.mainWinClass.ui.label_Year.setText(str(globals.selected_year))
     
        self.tableData.tableObject.selectionModel().currentRowChanged.connect(_rowChanged)
        
       
        # Update data
        def _updateData():        
            self.dataBalance.updateMonthStatus()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)

    # +++++++++++++++++++++++++++
    # Set focus and color for the current year/month row in tableView_Balance
    # +++++++++++++++++++++++++++
    def setCurrentMonthRow(self, setFocus=False):
        # 1:
        # - Find current year/month
        # - Focus and color the (year/month) row in tableView_Balance

        # Notes for code below:
        # PySide2.QtCore.QAbstractItemModel.match
        # match(strting cell index, Qt::DisplayRole=0, search value, number of hits (-1 to search through all))
        tableObject = self.table.tableObject
        tableModel = tableObject.model()

        yearCol = 0
        monthCol = 1
        currentMonthName = getMonthName(globals.current_month)

        # Get teh first current year cell
        indexMatch = tableModel.index(0, yearCol)
        yearsIndexList = tableModel.match(indexMatch, 0, globals.current_year, 1)

        # Get current month cell starting from the row in yearsIndexList
        indexMatch1 = tableModel.index(yearsIndexList[0].row(), monthCol)
        monthIndexList = tableModel.match(indexMatch1, 0, currentMonthName, 1)

        # current month row number
        currentMonthRow = monthIndexList[0].row()

        # Set color for the current year/month row
        color = ui_stylesheet.getRGBColor(globals.currentMonthRowColor)
        tableModel.setData(
            tableModel.index(currentMonthRow, 0),
            color,
            QtCore.Qt.ItemDataRole.BackgroundRole,
            customRule="row",
        )

        # Set focus on current year/month rows
        if setFocus:
            index = tableModel.index(currentMonthRow, 0)
            tableObject.setCurrentIndex(index)
            tableObject.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
            tableObject.selectionModel().select(
                index, QItemSelectionModel.SelectionFlag.SelectCurrent
            )
            tableObject.selectionModel().select(
                index, QItemSelectionModel.SelectionFlag.Clear
            )

            # Set month and year in Incomes and Expenses TAB for the current year/month row
            globals.mainWinClass.ui.label_Month.setText(str(currentMonthName))
            globals.mainWinClass.ui.label_Year.setText(str(globals.current_year))
            
    # +++++++++++++++++++++++++++
    # Execute DDL on DBS
    # Refresh tableView_Balance
    # ++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()

    # If user wants to change the status of the month (closed/opened), check if incomes and expesnes are closed
    def updateMonthStatus(self):
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        incomesOpen = float(
            self.tableData.tableObject.model().index(itemIndex.row(), 4).data()
        )
        expensesOpen = float(
            self.tableData.tableObject.model().index(itemIndex.row(), 7).data()
        )

        if incomesOpen == 0 and expensesOpen == 0:
            self.updateStatus_DialogWin()
        else:

            # if user choses not to make the change, return checkbox to original state
            self._invertCheckboxState(itemIndex)

            language = globals.app_language
            langFile = getTranslation()

            windowTitle = langFile[language]["changeMonthStatusTitle"]
            windowMessage = langFile[language]["changeMonthStatusError"]

            # promt user for comfirmation to change month's status
            self.myDialog = DWin_Alert(winTitle=windowTitle, winMessage=windowMessage)
            self.myDialog.show()

    # Prompt user for the the status of the month (closed/opened) change
    def updateStatus_DialogWin(self):
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        def callbackChangeCloseStatus(changeStatus: bool = False):
            if changeStatus == True:
                # user changed the status of the month (closed/opened)
                chkIndex = self.tableData.tableObject.model().index(itemIndex.row(), 11)
                # new month status state
                checkState = chkIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)

                self.monthClosed = True
                if checkState == QtCore.Qt.CheckState.Checked:
                    self.monthClosed = False

                self.updateBalance()
            else:
                # if user choses not to make the change, return checkbox to original state
                self._invertCheckboxState(itemIndex)

        year = self.tableData.tableObject.model().index(itemIndex.row(), 0).data()
        month = self.tableData.tableObject.model().index(itemIndex.row(), 1).data()
        messageDate = str(month) + ", " + str(year)

        # promt user for comfirmation to change month's status
        self.myDialog = DWin_Close_Month(
            messageDate=messageDate, callback=callbackChangeCloseStatus
        )
        self.myDialog.show()

    # +++++++++++++++++++++++++++
    # Update changes on Balance (Incomes and Expenses) table - tableView_Balance
    # ++++
    def updateBalance(self):

        self.tableData.tableObject.model().blockSignals(True)

        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()

        # DML statement
        update_stmt = None

        if itemIndex.column() == 11:
            chkIndex = self.tableData.tableObject.model().index(itemIndex.row(), 11)
            checkState = chkIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)

            monthClosed = 0

            if checkState == QtCore.Qt.CheckState.Checked:
                monthClosed = 2

            update_stmt = (
                "UPDATE INCOMES_SUM SET CLOSED = "
                + str(monthClosed)
                + "  WHERE YEAR = "
                + str(globals.selected_year)
                + "  AND MONTH = "
                + str(globals.selected_month)
            )

            if update_stmt:
                self._executeDDL(update_stmt)

            update_stmt = (
                "UPDATE EXPENSES_SUM SET CLOSED = "
                + str(monthClosed)
                + "  WHERE YEAR = "
                + str(globals.selected_year)
                + "  AND MONTH = "
                + str(globals.selected_month)
            )

            if update_stmt:
                self._executeDDL(update_stmt)

        # if DML statement is generated, do DB update
        if update_stmt:
            # self._executeDDL(update_stmt)
            self._repopulateTable(repopulate=True)

        self.tableData.tableObject.model().blockSignals(False)

    # +++++++++++++++++++++++++++
    # # Repopulate table data as a callback
    # ++++

    def _repopulateTable(self, repopulate=True, repopulateSingle=None):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable

            if repopulateSingle == None or repopulateSingle == "tableView_Incomes":
                # refresh data in tableView_Incomes
                table = globals.tableDict["tableView_Incomes"]
                table.tableEnabled = self.monthClosed
                populateTable(table)

            if repopulateSingle == None or repopulateSingle == "tableView_Expenses":
                # refresh data in tableView_Expenses
                table = globals.tableDict["tableView_Expenses"]
                table.tableEnabled = self.monthClosed
                populateTable(table)

    # +++++++++++++++++++++++++++
    # # Revert month status checkbox state
    # ++++

    def _invertCheckboxState(self, itemIndex):
        # if user choses not to make the change, return checkbox to original state

        def check_state_to_boolean(check_state):
            return (
                check_state == QtCore.Qt.CheckState.Checked
                or check_state == QtCore.Qt.CheckState.PartiallyChecked
            )

        self.tableData.tableObject.model().blockSignals(True)

        chkIndex = self.tableData.tableObject.model().index(itemIndex.row(), 11)

        checkState = chkIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)

        # invert current check state
        checkStateBool = not check_state_to_boolean(checkState)

        self.tableData.tableObject.model().setData(
            itemIndex, checkStateBool, QtCore.Qt.ItemDataRole.EditRole
        )

        self.tableData.tableObject.model().blockSignals(False)
