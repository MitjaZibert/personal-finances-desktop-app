# ===========================================================================================
# QAbstractTableModel - custom table view model
# 
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries
from datetime import date

# PyQt Windows libraries
from PyQt6 import QtCore

# App Specific libraries

# =========================================================

# Class
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, tableDict):
        super(TableModel, self).__init__()
        
        # data must be in a LIST of LISTS format
        self.data = data

        # table class instance
        self.tableDict = tableDict
        self.backgroundColors = dict()
        self.backgroundColors_scope = "cell" #cell, row, column

    # +++++++++++++++++++++++++++ 
    # Define each table cell based on it's data
    # +++++++++++++++++++++++++++ 
    def data(self, index, role):
        # default QT role order:
            # before roles flags() is called
            # 6 - FontRole
            # 7 - TextAlignmentRole
            # 9 - ForegroundRole
            # 10 - CheckStateRole
            # 1 - DecorationRole
            # 0 - DisplayRole
            # 8 - BackgroundRole

        value = self.data[index.row()][index.column()]
        
        if not index.isValid():
            return None
        
        # +++++++++++++
        if role == QtCore.Qt.ItemDataRole.CheckStateRole:
            
            if self.tableDict.columnCheckBox[index.column()] in (1, 2):
                if value == 1: # PartiallyChecked is ignored
                    return QtCore.Qt.CheckState.Checked
                elif value == 2:
                    return QtCore.Qt.CheckState.Checked
                else:
                    return QtCore.Qt.CheckState.Unchecked

        # +++++++++++++     
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
          
            # for checkbox don't display value
            if self.tableDict.columnCheckBox[index.column()] in (1, 2):
                return ""
            else:
                #roundedNumber = self.tableDict.roundedNumber[index.column()]
                #if roundedNumber > 0:
                    # value = str(round(value, roundedNumber)) # rounding to more than 2 decimals doesn't work like this in Python - need to change
                    #value = str(round(value, 2))
                
                return str(value)
       
                
        # +++++++++++++  
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
         
            dictIndex = None
            for key, val in self.backgroundColors.items():
                # get first key
                dictIndex = key
                # after getting first key break loop
                break
            
            ix = self.index(index.row(), index.column())
            
            if dictIndex and self.backgroundColors_scope == "row":
                ix = self.index(index.row(), dictIndex.column())

            if dictIndex and self.backgroundColors_scope == "column":
                ix = self.index(dictIndex.row(), index.column())

            # Change background color for one cell or all row or column cells
            if ix in self.backgroundColors:
                color = self.backgroundColors[ix]
                
                return color
    
        # +++++++++++++   
        if role == QtCore.Qt.ItemDataRole.EditRole:
            return str(value)

        
    # +++++++++++++++++++++++++++ 
    # Custom model setData method
    # +++++++++++++++++++++++++++ 
    def setData(self, index, value, role, customRule = None):

        self.backgroundColors.clear()
        
        # +++++++++++++
        # QtCore.Qt.CheckState.Unchecked == 0
        # QtCore.Qt.CheckState.PartiallyChecked == 1
        # QtCore.Qt.CheckState.Checked == 2
        if (role == QtCore.Qt.ItemDataRole.CheckStateRole 
            and self.tableDict.columnCheckBox[index.column()] in (1, 2)):
            
            # select the row of a clicked checkbox
            tableObject = self.tableDict.tableObject
            index = self.index(index.row(), index.column())
            tableObject.setCurrentIndex(index)
           
            self.data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)

            return True
        
        # +++++++++++++
        elif (value is not None 
            and role == QtCore.Qt.ItemDataRole.EditRole):
           
            self.data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)

            return True
        
        # +++++++++++++
        if (role == QtCore.Qt.ItemDataRole.BackgroundRole):

            # Set cell index for changing the background color
            ix = self.index(index.row(), index.column())
            self.backgroundColors[ix] = value

            if customRule:
                self.backgroundColors_scope = customRule
            
            return True    
       
        return False 

     
    # +++++++++++++++++++++++++++ 
    # Set model flags
    # +++++++++++++++++++++++++++ 
    def flags(self, index):
        flags = super().flags(index)

        cellEnabled = self._dataDependantCellFlag(index)
        
        flags = QtCore.Qt.ItemFlag.NoItemFlags
        flags |= QtCore.Qt.ItemFlag.ItemIsEnabled

        # Disable all table cells
        if self.tableDict.tableEnabled == False or cellEnabled == False:
            flags |= ~QtCore.Qt.ItemFlag.ItemIsEditable & ~QtCore.Qt.ItemFlag.ItemIsUserCheckable
        
        else:
            # Enable cell
            if self.tableDict.columnEditable[index.column()] == True:
                flags |= QtCore.Qt.ItemFlag.ItemIsEditable
                
                
            # Cell is checkbox twostate
            if self.tableDict.columnEditable[index.column()] == True and self.tableDict.columnCheckBox[index.column()] == 1:
                flags |= QtCore.Qt.ItemFlag.ItemIsUserCheckable
                

            # Cell is checkbox tristate
            if self.tableDict.columnEditable[index.column()] == True and self.tableDict.columnCheckBox[index.column()] == 2:
                flags |= QtCore.Qt.ItemFlag.ItemIsUserCheckable & QtCore.Qt.ItemFlag.ItemIsAutoTristate
                
        
        return flags

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # The nested-list data structure of each data table
    # Get table row dimension
    # .row() indexes into the outer list
    def rowCount(self, index):
        # The length of the outer list.
        rowCount = len(self.data)

        return rowCount

    # Get table column dimension
    # .column() indexes into the sub-list
    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        
        columnCount = 0
        if len(self.data) > 0:
            columnCount = len(self.data[0])

        return columnCount
    
    # +++++++++++++++++++++++++++ 
    # +++++++++++++++++++++++++++ 

    # Set header data (column names)
    def setHeaderData(self, section, orientation, data, role = QtCore.Qt.ItemDataRole.EditRole):
        if orientation == QtCore.Qt.Orientation.Horizontal and role in (QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role = QtCore.Qt.ItemDataRole.DisplayRole):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except:
                pass
        return super().headerData(section, orientation, role)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++ 
# Custom functionality
# +++++++++++++++++++++++++++ 

    def _dataDependantCellFlag(self, index):
        
        cellEnabled = True

        regCol = None
        
        # If regular income/expense row is NOT enabled for editing
        if self.tableDict.tableObject.objectName() == 'tableView_Incomes':
            regCol = self.tableDict.db_columns.index("update_regular_income")
            corrCol = self.tableDict.db_columns.index("correction")
        
        if self.tableDict.tableObject.objectName() == 'tableView_Expenses':
            regCol = self.tableDict.db_columns.index("update_regular_expense")
            corrCol = self.tableDict.db_columns.index("correction")
    
        if regCol:        
            regColIndex = self.tableDict.tableObject.model().index(index.row(), regCol)
            checkState = regColIndex.data(QtCore.Qt.ItemDataRole.CheckStateRole)
            
            if checkState == QtCore.Qt.CheckState.Checked and index.column() not in (regCol, corrCol):
                cellEnabled = False
        
        return cellEnabled

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTES
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# you can store indexes for the whole row (col = 0)
    
# ix = self.index(index.row(), 0)
# pix = QtCore.QPersistentModelIndex(ix)
# self.backgroundColors[pix] = value
# return True 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ARCHIVE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ 
    # Custom model insertRows method
    # +++++++++++++++++++++++++++ 

    # def insertRows(self, data):
    #     self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
    #     self.data.append(data)
    #     self.endInsertRows()

    # # +++++++++++++++++++++++++++ 
    # # Custom model removeRows method
    # # +++++++++++++++++++++++++++ 
    # def removeRows(self, index, position, rows):
    #     #parent = index.parent()
    #     parent = self.index

    #     self.beginRemoveRows(parent, position, position)
    #     #self.beginRemoveRows(parent, position, position + rows - 1)

    #     #for x in range(0, rows):
    #     self.removeRow(position)

    #     self.endRemoveRows()

    #     return True    