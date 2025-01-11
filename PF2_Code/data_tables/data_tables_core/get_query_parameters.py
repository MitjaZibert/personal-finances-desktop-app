# ===========================================================================================
# Set SQL parameters
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries

# PyQt Windows libraries

# App Specific libraries
import globals

# =========================================================

# +++++++++++++++++++++++++++
# Get query parameters for table queries that take parameters
# +++++++++++++++++++++++++++  
def getQueryParameters(table):
    args = None
    tableName = table.tableObject.objectName()
    
    if tableName == 'tableView_Incomes':
        args = {table.query_args[0]: globals.selected_year, table.query_args[1]: globals.selected_month}
        
    if tableName == 'tableView_Expenses':
        args = {table.query_args[0]: globals.selected_year, table.query_args[1]: globals.selected_month}

    return args