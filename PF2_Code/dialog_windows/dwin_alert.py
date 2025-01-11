
# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports:
# System libraries

# PyQt6 libraries
from PyQt6 import QtWidgets

# App Specific libraries
import globals
from util.get_translation import getTranslation
from ui_qt.ui_dwin_alert import Ui_DWin_Alert


# ===========================================================================================

# Alert win
class DWin_Alert(QtWidgets.QDialog, Ui_DWin_Alert):
    def __init__(self, winTitle, winMessage, parent=None):
        super(DWin_Alert, self).__init__(parent)

        # Setup Window
        self.setupUi(self)
        
        language = globals.app_language
        langFile = getTranslation()
        self.buttonBoxOk.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText(langFile[language]['buttonOK'])

        self.setWindowTitle(winTitle)
        self.labelAlert.setText(winMessage)

        # (button) Close
        self.buttonBoxOk.accepted.connect(self.closeWin)
        
    # +++++++++++++++++++++++++++
    # Close window
    #++++
    def closeWin(self):
        #self.callback()
        self.close()