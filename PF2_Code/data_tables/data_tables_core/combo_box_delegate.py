# ===========================================================================================
# Table Model Combobox item
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries

# PyQt Windows libraries
from PyQt6.QtWidgets import QStyledItemDelegate, QComboBox
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal

# App Specific libraries
from data_modules import DB_Util



class ComboBoxDelegate(QStyledItemDelegate):
    comboBoxChanged = pyqtSignal(str)

    def __init__(self, comboList, handleComboBoxChange, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.comboList = comboList
        self.handleComboBoxChange = handleComboBoxChange

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.comboList)

        # Connect the currentIndexChanged signal to a handleComboBoxChange function in relevant table class
        combo.currentIndexChanged.connect(lambda: self.comboBoxChanged.emit(combo.currentText()))
        self.comboBoxChanged.connect(self.handleComboBoxChange)
        
        return combo

    def setEditorData(self, editor, index):
        value = index.data()
        if value:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), QtCore.Qt.ItemDataRole.EditRole)


    # +++++++++++++++++++++++++++
    # Custom function - populates DB values into list and dictionary
    # +++++++++++++++++++++++++++  
    def getComboBoxData(query):
            # get query result
            db = DB_Util()
            dbCurr = db.getData(query)
            dbRows = dbCurr.fetchall()

            comboList = [] # used in combobox delegate
            comboDict = {} # used for pairing selected value from combo with its key (ID)
            for key, value in dbRows:
                comboDict[key] = value
                comboList.append(value)

            return comboDict, comboList