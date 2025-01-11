# ===========================================================================================
# Set Data Tables headers
# ===========================================================================================
# ===========================================================================================

# Imports:

# Sys libraries

# PyQt Windows libraries
from PyQt6 import QtCore

# App Specific libraries
from util.get_translation import getTranslation
import globals

# set Data Tables headers
def tableHeaders(table):
    model = table.tableModel

    language = globals.app_language # Get app language
    langFile = getTranslation() # Get column headers in chosen language
    
    col_no = len(table.columnWidths)
    model.horizontalHeaders = [''] * col_no

    for col in range(col_no):
        
        #Set column headers in chosen language
        try:
            col_header = langFile[language][table.tableObject.objectName() + '_col_' + str(col)]
            model.setHeaderData(col, QtCore.Qt.Orientation.Horizontal, col_header)
        except KeyError as e:
            print ('No header translation for table_column "%s"' % str(e))

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  