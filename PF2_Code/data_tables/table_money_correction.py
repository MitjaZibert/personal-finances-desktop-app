# ===========================================================================================
# Code specific to TableView Money_Correction
# 
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries


# PyQt Windows libraries
from PyQt6 import QtCore
from PyQt6.QtWidgets import QAbstractItemView
from PyQt6.QtCore import QItemSelectionModel

# App Specific libraries
import globals
from data_modules import DB_Util
import data_modules.data_calculations as data_calculations
from util import getMonthName 
from ui_format import ui_stylesheet

# Data Manipulation for Incomes Table
class TableMoneyCorrection():
    def __init__(self):
        self.tableData = globals.tableDict["tableView_Money_Correction"]
        self.db = DB_Util()


    #+++++++++++++++++++++++++++
        # Execute DDL on DBS
        # Refresh tableView_Balance
    #++++
    def _executeDDL(self, ddl):
        self.db.executeDDL(ddl)

        # do commit on DB
        self.db.saveData()


    # =========================================================
    # Main Window - Table Money Correction functionality
    #++++
    def tableMoneyCorrectionFunctionality(self):
        # Update data
        def _updateData():
            self.dataMoneyCorrection.updateMoneyCorrection()

        self.tableData.tableObject.model().dataChanged.connect(_updateData)

    #+++++++++++++++++++++++++++
    # Update changes on Money_Correction table - tableView_Money_Correctiony 
    #++++
    def updateMoneyCorrection(self):
        
        self.tableData.tableObject.model().blockSignals(True)
        
        itemIndex = self.tableData.tableObject.selectionModel().currentIndex()
        
        # changed item row ID
        corrIDIndex = self.tableData.tableObject.model().index(itemIndex.row(), 0)
        corrID = corrIDIndex.data()
        
        # DB table name of the updated column
        updatedColumn = self.tableData.db_columns[itemIndex.column()]
        
        # Updated value
        updatedItemValue = itemIndex.data()
        
        # DML statement
        update_stmt = None

        # db_columns = ["money_correction_id", "year", "month", "amount", "notes"],
                                 
        if updatedColumn in ["amount", "notes"]:
            update_stmt = "UPDATE MONEY_CORRECTION SET " + str(updatedColumn) + " = '" + str(updatedItemValue) + "' WHERE MONEY_CORRECTION_ID = " + str(corrID)

        
        # if DML statement is generated, do DB update
        if update_stmt:
            self._executeDDL(update_stmt)
            self.repopulateData(repopulate = True, repopulateSingle = "tableView_Balance")
        

        self.tableData.tableObject.model().blockSignals(False)
        

    # +++++++++++++++++++++++++++
    # Set focus and color for the current year/month row in tableView_Money_Correction
    # +++++++++++++++++++++++++++   
    def setCurrentMonthRow(self, setFocus = False):
        # 1:
        # - Find current year/month 
        # - Focus and color the (year/month) row in tableView_Balance
        
        # Notes for code below:
            # PySide2.QtCore.QAbstractItemModel.match
            # match(strting cell index, Qt::DisplayRole=0, search value, number of hits (-1 to search through all))
        tableObject = self.tableData.tableObject
        tableModel = tableObject.model()

        yearCol = 1
        monthCol = 2
        currentMonthName = getMonthName(globals.current_month)
    
        # Get teh first current year cell
        indexMatch = tableModel.index(0, yearCol)
        yearsIndexList = tableModel.match(indexMatch, 0, globals.current_year, 1)
        
        # Get current month cell starting from the row in yearsIndexList
        indexMatch1 = tableModel.index(yearsIndexList[0].row(), monthCol)
        monthIndexList = tableModel.match(indexMatch1, 0, currentMonthName, 1)
        
        # current month row number
        currentMonthRow = monthIndexList[0].row()
        
        # Set focus on current year/month rows
        if setFocus:
            index = tableModel.index(currentMonthRow, 0)
            tableObject.setCurrentIndex(index)
            tableObject.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
            tableObject.selectionModel().select(index, QItemSelectionModel.SelectionFlag.SelectCurrent)
            tableObject.selectionModel().select(index, QItemSelectionModel.SelectionFlag.Clear)
            
        # Set color for the current year/month row
        color = ui_stylesheet.getRGBColor(globals.currentMonthRowColor)
        tableModel.setData(tableModel.index(currentMonthRow, 0), color, QtCore.Qt.ItemDataRole.BackgroundRole, customRule = "row")

    #+++++++++++++++++++++++++++
    # Repopulate data as a callback
    #++++

    def repopulateData(self, repopulate = True, repopulateSingle = None):
        if repopulate:
            from data_tables.data_tables_core.populate_table import populateTable


            if repopulateSingle == None or repopulateSingle == "tableView_Balance":        
                table = globals.tableDict["tableView_Balance"]
                # refresh data in tableView_Balance
                populateTable(table, setRowFocus = False)

            
            data_calculations.recalculateAmounts()
        