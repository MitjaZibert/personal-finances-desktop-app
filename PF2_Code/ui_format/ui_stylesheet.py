
# ===========================================================================================

# Imports:

# System libraries

# PyQt Windows libraries
from PyQt6 import QtGui
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QLinearGradient


# App Specific libraries
import globals

# =========================================================
# Global Stylesheets
#class UIStylesheet():

    # # +++++++++++++++++++++++++++
    # # Stylesheet config file
    # #++++
    # def __init__(self):
    #     # get config values
    #     stylesheetFile = readFile(r'\Config\stylesheet_config.ini')

    #     self.currentRowActiveColor = stylesheetFile['colors']['currentRowActiveColor']
    #     self.currentMonthRowColor = stylesheetFile['colors']['currentMonthRowColor']
    #     self.currentRowInactiveColor = stylesheetFile['colors']['currentRowInactiveColor']

# +++++++++++++++++++++++++++
# Style buttons with image instead of text
# +++++++++++++++++++++++++++
def styleButtonWithImage(object):
    object.setStyleSheet("border: none")

# +++++++++++++++++++++++++++
# get RGB Color
#++++
def getRGBColor( colorObject):
    if "," in colorObject:
        R = int(colorObject.split(",",2)[0])
        G = int(colorObject.split(",",2)[1])
        B = int(colorObject.split(",",2)[2])
        color = QColor(R, G, B)
    else:
        color = QColor(colorObject)

    return color

# +++++++++++++++++++++++++++
# set label text color - red for negative
#++++
def fontColor(item, value):
    if value < 0:
        setItemTextColor(item, QBrush(QColor(255, 46, 66)))
    else:   
        setItemTextColor(item, "black")

# +++++++++++++++++++++++++++
# set item text color
#++++
def setItemTextColor(item, color):
    pal = item.palette()
    pal.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(color))
        
    item.setPalette(pal)


 # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++
# WINDOW STYLSHEETS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

# +++++++++++++++++++++++++++
# Window colors
#++++
def setWindowStyle(winMain):
    None

    # winPalette = QPalette()
    # gradient = QLinearGradient(300, 1500, 00, 00) # left / top / right / bottom
    # gradient.setColorAt(0.0, QColor(getRGBColor(globals.windowColorA)))
    # gradient.setColorAt(1.0, QColor(getRGBColor(globals.windowColorB)))
    # brush = QBrush(gradient)
    # winPalette.setBrush(QPalette.ColorRole.Window, brush) # Background color
    
    # winMain.setPalette(winPalette)

    # winMain.ui.tabWidget_Main.widget(0).setAutoFillBackground(True)
    # winMain.ui.tabWidget_Main.widget(1).setAutoFillBackground(True)
    # winMain.ui.tabWidget_Main.widget(2).setAutoFillBackground(True)

    '''
    tabPalette = QPalette()
    gradient = QLinearGradient(0, 0, 300, 700) # left / top / right / bottom
    gradient.setColorAt(0.0, QColor(getRGBColor(globals.tabColorA)))
    gradient.setColorAt(1.0, QColor(getRGBColor(globals.tabColorB)))
    brush = QBrush(gradient)
    tabPalette.setBrush(QPalette.ColorRole.Base, brush) # Background color
    tabPalette.setColor(QPalette.ColorRole.WindowText, QColor(getRGBColor(globals.windowTextColor)))  # Text color
    
    #winMain.ui.tabWidget_Main.setAutoFillBackground(True)
    #winMain.ui.tabWidget_Main.setPalette(tabPalette)
    
    #winMain.ui.tabWidget_Main.widget(0).setPalette(tabPalette)
    #winMain.ui.tabWidget_Main.widget(1).setPalette(tabPalette)
    #winMain.ui.tabWidget_Main.widget(2).setPalette(tabPalette)
    '''

# +++++++++++++++++++++++++++
# Table stylesheet
#++++
def setTable(table, setInactive = False):
    background = "#2d89ef"
    tableRows = "background-color: red;"
    #table.setStyleSheet(tableRows) 

    # table.setStyleSheet("""
    #     QTableWidget::item:selected {
    #     background-color: #2d89ef; /* Example color */
    #     color: white;
    #     }   
    #     QTableWidget::item {
    #         background-color: red;
    #         color: black;
    #     }""")



'''
def setTable(self, object, setInactive = False):
    
    # Table HEADER
    # table header font size
    factor = self.tableHeaderFont
    pointSize = factor * self.globalScaleFactor

    fontHeader = object.font()
    #dec2023 fontHeader.setPointSize(pointSize)
    fontHeader.setPointSize(int(pointSize))
    fontHeader.setFamily(self.fontFamily)
    object.horizontalHeader().setFont(fontHeader)
    #dec2023 object.horizontalHeader().setFixedHeight(self.tableHeaderHeight)
    object.horizontalHeader().setFixedHeight(int(self.tableHeaderHeight))
    object.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    tableHeader = "::section{padding: 5px; color: white; background-color:rgb("+self.tableHeaderColor+");border-radius:0px; font-weight:"+str(self.tableHeaderFontWeight)+"; }"
    object.horizontalHeader().setStyleSheet(tableHeader) 
    
    # +++++++++++++++++++++++++++
    # Table ROWS
    # Table rows - alternate colors
    fontRow = object.font()
    #dec2023 fontRow.setPointSize(self.tableRowFont)
    fontRow.setPointSize(int(self.tableRowFont))
    object.setFont(fontRow)
    #tableRows = "color: white; alternate-background-color: rgb("+self.tableRowAlt1Color+"); background-color: rgb("+self.tableRowAlt2Color+");"
    tableRows = "color: white; alternate-background-color: rgb("+self.tableRowAlt1Color+"); background-color: transparent;"
    object.setStyleSheet(tableRows) 

    
    p = QtGui.QPalette(object.palette())
    #if setInactive == True:
    #Setting Inactive row color (back and text)
    colorInactiveBack = self.getRGBColor(self.currentRowInactiveColor)
    p.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight,QtGui.QBrush(colorInactiveBack))
    colorInactiveText = self.getRGBColor(self.currentRowInactiveTextColor)
    p.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText,QtGui.QBrush(colorInactiveText))
        
    #Setting Active row color (back and text)
    colorActiveBack = self.getRGBColor(self.currentRowActiveColor)
    p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight,QtGui.QBrush(colorActiveBack))
    colorActiveText = self.getRGBColor(self.currentRowActiveTextColor)
    p.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText,QtGui.QBrush(colorActiveText))

    object.setPalette(p)

# +++++++++++++++++++++++++++
# Table rows
#++++
def setTableRowHeight(self, table, row):
    #dec2023 table.setRowHeight(row, self.tableRowHeight)
    table.setRowHeight(row, int(self.tableRowHeight))


# +++++++++++++++++++++++++++
# set Table item color
#++++
def setTableItemBackgroundColor(self, item, colorType):
    color = QtGui.QColor(0, 0, 0)
    
    if colorType == 'currentMonth':
        color = self.getRGBColor(self.currentMonthRowColor)
    elif colorType == 'selectedCell':
        color = self.getRGBColor(self.currentRowCellColor)
        
    item.setBackground(color)

# +++++++++++++++++++++++++++
# Table column width
#++++
def setTableColumnWidth(self, object, col, width = 70):
    #width = width * self.conversionFactor
    pointSize = self.globalScaleFactor * width * self.tableColumnWidthFactor
    #dec2023 object.setColumnWidth(col, pointSize)
    object.setColumnWidth(col, int(pointSize))

# +++++++++++++++++++++++++++
# Get all table columns width
#++++
def getTableWidth(self, object):
    colWidth = 0

    for col in range(object.columnCount()):
        if object.isColumnHidden(col) == False:
            colWidth = colWidth + object.columnWidth(col)
    
    # add scrollbar width
    colWidth = colWidth + 20

    return colWidth


# +++++++++++++++++++++++++++
# Item fonts
#++++
# def setItemFont(object, type = None, weight=None):
#     color = "white"
#     if type == 'small label':
#         factor = smallFont
#         color = QColor(169,178, 186)
#     elif type == 'large label':
#         factor = self.largeFont
#         color = "white"
#     elif type == 'checkbox':
#         factor = self.checkboxFont
#         color = QColor(169,178, 186)
#     elif type == 'alert':
#         factor = self.alertMessageFont
#         color = "white"
#     else:
#         factor = self.normalFont
    
    
#     pointSize = factor * self.globalScaleFactor
#     font = object.font()

#     font.setFamily(self.fontFamily)
#     #dec2023 font.setPointSize(pointSize)
#     font.setPointSize(int(pointSize))
#     object.setFont(font)
#     self.setItemTextColor(object, color)

#     if weight == "bold":
#         font.setBold(True)
#         object.setFont(font)
'''