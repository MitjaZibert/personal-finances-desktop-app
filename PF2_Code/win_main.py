# ===========================================================================================
#!/usr/bin/env python
# pyqt6rc \Users\mitja\Programiranje\Personal_Finances\PF2_Dev\PF2_Source\personal-finances-desktop-app\PF2_Code\ui_qt\ui_win_main.ui -o \Users\mitja\Programiranje\Personal_Finances\PF2_Dev\PF2_Source\personal-finances-desktop-app\PF2_Code\ui_qt\
# pyqt6rc Users\mitja\Programiranje\Personal_Finances\PF2_Dev\PF2_Source\personal-finances-desktop-app\Custom_Icons\PF_Icons.qrc -o Users\mitja\Programiranje\Personal_Finances\PF2_Dev\PF2_Source\personal-finances-desktop-app\Custom_Icons\PF_Icons_rc.py
# pyside6-rcc \Users\mitja\Programiranje\Personal_Finances\PF2_Dev\PF2_Source\personal-finances-desktop-app\PF2_Code\Custom_Icons\PF_Icons.qrc -o \Users\mitja\Programiranje\Personal_Finances\PF2_Dev\PF2_Source\personal-finances-desktop-app\PF2_Code\Custom_Icons\PF_Icons_rc.py


# Installations
# conda install pymysql
#
# ===========================================================================================
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore

# App Specific libraries
import globals
from ui_format.win_main_ui import WinMainUi
from ui_qt.ui_win_main import Ui_WinMain

from data_modules.data_checks import DataCheck
from util import Currencies

from win_main_func import WinMainFunc

#from app_func import AppFunc
from data_tables.data_tables_core import populateTable
from data_tables.data_tables_core import tableHeaders
from data_tables.data_tables_core import formatTable
from data_tables.data_tables_core.table_definitions import tableDefinitions

# =========================================================

# Win_Main class
class WinMain(QMainWindow):
    
    def __init__(self):
        
        super(WinMain, self).__init__()

        # +++++++++++++++++++++++++++
        # =====> Main Window UI
        # +++++++++++++++++++++++++++

        # Setup PyQT UI for this window
        self.ui = Ui_WinMain()
        self.ui.setupUi(self)

        # Modify app UI - All that is not done directly in QT Designer
        self.uiMod = WinMainUi(self)
        self.uiMod.modufyUI()

        # Save Main Window Class instance
        globals.mainWinClass = self

        # +++++++++++++++++++++++++++
        # =====> Initial Data Check and Updates
        # +++++++++++++++++++++++++++

        self.dataCheck = DataCheck()
        # Check if a new month needs to be added
        self.dataCheck.checkNewMonth()
        # Chack any data potential irregularities
        self.dataCheck.checkDBIrregularities()

        # convert currencies
        currencies = Currencies()
        currencies.updateCurrencies()

        # +++++++++++++++++++++++++++
        # =====> Main Window Data
        # +++++++++++++++++++++++++++

        # Set data tables dictionary (defined in table_definitions.py)
        tableDefinitions(self, globals.tableDict)

        # Generate and populate tables
        for table in globals.tableDict.values():
            # Populate all data tables with data (e.g. QTableView)
            populateTable(table)

            # Set headers for all data tables
            tableHeaders(table)

            # Format all data tables
            formatTable(table)

        # +++++++++++++++++++++++++++
        # =====> Main Window Functionality
        # +++++++++++++++++++++++++++

        # Setup current window functionuality (e.g. what each button does)
        self.func = WinMainFunc(self)
        self.func.mainWindowFunctionality()

        #app_func = AppFunc()
        #app_func.appFunctionality()

        # +++++++++++++++++++++++++++
        # =====> Temp DEV Code
        # +++++++++++++++++++++++++++

        self._test()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # keyPressEvents
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def keyPressEvent(self, event):
        # Close app on Escape key press
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Quick testing method
    # +++++++++++++++++++++++++++
    def _test(self):
        
        None
        
        # table = globals.tableDict["tableView_Allocation"]
        # tableModel = globals.tableDict["tableView_Allocation"].tableModel
        # print(tableModel.rowCount(QtCore.QModelIndex))

        # itemIndex = self.data_tables.tableObject.model()
        # item = tableModel.item(0,6)

        # chk = tableModel.index(1, 6)
        # chkbox = chk.data(QtCore.Qt.ItemDataRole.CheckStateRole)
        # print(chkbox)

        # def _test():
        # color = self.uiMod.stylesheets.getRGBColor(self.uiMod.stylesheets.currentMonthRowColor)
        # tableModel = globals.tableDict["tableView_Allocation"].tableModel
        # print(tableModel)
        # test = tableModel.rowCount(1)
        # print(test)
        # tableModel.setData(tableModel.index(2, 0),color,QtCore.Qt.ItemDataRole.BackgroundRole, customRule = "row")

        # self.ui.pushButton_Quit.clicked.connect(_test)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
