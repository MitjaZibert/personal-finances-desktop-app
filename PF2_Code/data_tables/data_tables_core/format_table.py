# ===========================================================================================
# Table formatting class
# ===========================================================================================
# ===========================================================================================

# Imports:

# Sys libraries

# PyQt Windows libraries
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView

# App Specific libraries

# +++++++++++++++++++++++++++
# Format Table Objects
# +++++++++++++++++++++++++++  
def formatTable(table):
    
    table.tableObject.setAlternatingRowColors(True) 


    table.tableObject.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    table.tableObject.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    
    header = table.tableObject.horizontalHeader()      
    header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed) 
    
    table.tableObject.setGeometry(table.geometry[0], table.geometry[1], table.geometry[2], table.geometry[3]) # x, y, w, h

    # +++++++++++++++++++++++++++
    # Set tables columns
    #++++
    
    i = 0
    for colWidth in table.columnWidths:

        # Set column width
        table.tableObject.setColumnWidth(i, colWidth)

        # Set column as hidden if width == 0
        if colWidth == 0:
            table.tableObject.setColumnHidden(i, True) 

        i += 1


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  