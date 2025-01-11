# ===========================================================================================
# Get selected month's number or translated name
# 
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries

# PyQt Windows libraries

# App Specific libraries
import globals
from util.get_translation import getTranslation

# =========================================================

# +++++++++++++++++++++++++++
# Get month's number (int)
# +++++++++++++++++++++++++++  
def getMonthInt(monthName):
    language = globals.app_language # Get app language
    langFile = getTranslation() # Get column headers in chosen language
    
    monthNo = 0
    for i in range (1, 13):
        month = langFile[language]['m_' + str(i)]
        if monthName == month:
            monthNo = i

    return monthNo

# +++++++++++++++++++++++++++
# Get month's translated name (string)
# +++++++++++++++++++++++++++  
def getMonthName(monthNo):
    language = globals.app_language # Get app language
    langFile = getTranslation() # Get column headers in chosen language
    
    monthName = langFile[language]['m_' + str(monthNo)]

    return monthName


# *********************************************************************************************
# *********************************************************************************************
# CLASS NOTES
# *********************************************************************************************
#
