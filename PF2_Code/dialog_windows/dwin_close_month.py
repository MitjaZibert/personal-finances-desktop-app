
# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6 import QtWidgets

# App Specific libraries
import globals
from ui_qt.ui_dwin_close_month import Ui_DWin_Close_Month
from util.get_translation import getTranslation

# ===========================================================================================

# Change Month's Status window
class DWin_Close_Month(QtWidgets.QDialog, Ui_DWin_Close_Month):
    def __init__(self, messageDate, callback, parent=None):
        super(DWin_Close_Month, self).__init__(parent)

        # Setup Currencies Window
        self.setupUi(self)

        language = globals.app_language
        langFile = getTranslation()

        self.setWindowTitle(langFile[language]['changeMonthStatusTitle'])
        self.buttonBoxCloseMonth.button(QtWidgets.QDialogButtonBox.StandardButton.Yes).setText(langFile[language]['buttonYes'])
        self.buttonBoxCloseMonth.button(QtWidgets.QDialogButtonBox.StandardButton.No).setText(langFile[language]['buttonNo'])


        messageText = langFile[language]['changeMonthStatus']
        messageText = messageText + " " + messageDate
        self.labelAlert.setText(str(messageText))

        # Callback method
        self.callback = callback
    
        # +++++++ Buttons ++++++++
        # (button) Save
        self.buttonBoxCloseMonth.accepted.connect(self.updateStatus)

        # (button) Close
        self.buttonBoxCloseMonth.rejected.connect(self.closeWin)
        
    # +++++++++++++++++++++++++++
    # Update month's status
    #++++
    def updateStatus(self):   
        self.callback(True)
        self.close()
        
    # +++++++++++++++++++++++++++
    # Discard changes
    #++++
    def closeWin(self):
        self.callback(False)
        self.close()