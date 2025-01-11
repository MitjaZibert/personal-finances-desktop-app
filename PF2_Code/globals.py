# ===========================================================================================
# Global variables
# ===========================================================================================
# ===========================================================================================


# ===== NOT OPTIMAL - To be changed in how code is written
current_db_conn = None # current DB connection - !!! must be changed how this is approached
tableDict = {} # Dictionary of all data tables and its definitions
mainWinClass = None

# ========
app_path = None # App Source Code directory 
root_path = None # Root App directory 
app_language = "EN" # App language - read from app.config.ini
app_db = None # Database to be used - read from app.config.ini

current_date = None # set in util.util_app.py
current_year = None # set in util.util_app.py
current_month = None # set in util.util_app.py

selected_year = None # set in windowClass.ui.tableView_Balance
selected_month = None # set in windowClass.ui.tableView_Balance

currentMonthRowColor = None # Set background roe color for current month in TableView Balance
currentRowActiveColor = None # Active table row background color
currentRowInactiveColor = None # Inactive table row background color


windowColorA = None # Window background color (gradient A)
windowColorB = None # Window background color (gradient B)
windowTitleColor = None # Window main labels color
windowTextColor = None # Window text color
tabColorA = None # Tabs background color (gradient A)
tabColorB = None # Tabs background color (gradient B)

activeWidget = None # Currently active app widget

tabMonthLabel = None # Main Win tab - selected month color
tabYearLabel = None # Main Win tab - selected year color
# ===========================================================================================
# ===========================================================================================
# ===========================================================================================


# ===========================================================================================
# Set Global variables
# ===========================================================================================
# ===========================================================================================

# System libraries
import sys, os
from os import path
import datetime

# App Specific libraries
import globals
from util.read_file import readFile
from data_modules import db_connect

# +++++++++++++++++++++++++++
# Set app global variables - called from pf_main.py
# +++++++++++++++++++++++++++
def set_globals():
    
    # set app root path
    globals.app_path = path.dirname(path.abspath(sys.argv[0]))
    globals.root_path = os.path.dirname(globals.app_path)
    
    # read app_config.ini data
    globals.app_config_file = readFile(r'\PF2_Config\app_config.ini', rootPath=True)
    
    # set app language
    globals.app_language = globals.app_config_file['LANG']['app_language']

    # set db
    globals.app_db = globals.app_config_file['DB']['app_db']
    globals.app_db = globals.app_db.strip("'")
    
    globals.current_db_conn = db_connect.getConn()

    # set Dates
    date = datetime.datetime.today()
    globals.current_date = date
    globals.current_year = str(date.year)
    globals.current_month = str(date.month) 
    globals.selected_year = globals.current_year
    globals.selected_month = globals.current_month



    # Stylesheet values
    stylesheetFile = readFile(r'\Config\stylesheet_config.ini')

    globals.currentMonthRowColor = stylesheetFile['colors']['currentMonthRowColor']
    globals.currentRowActiveColor = stylesheetFile['colors']['currentRowActiveColor']
    globals.windowColorA = stylesheetFile['colors']['windowColorA']
    globals.windowColorB = stylesheetFile['colors']['windowColorB']
    globals.windowTitleColor = stylesheetFile['colors']['windowTitleColor']
    globals.windowTextColor = stylesheetFile['colors']['windowTextColor']
    #globals.tabColorA = stylesheetFile['colors']['tabColorA']
    #globals.tabColorB = stylesheetFile['colors']['tabColorB']

    globals.tabMonthLabel = stylesheetFile['colors']['tabMonthLabel']
    globals.tabYearLabel = stylesheetFile['colors']['tabYearLabel']

