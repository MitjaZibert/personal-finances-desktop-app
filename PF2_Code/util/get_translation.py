
# ===========================================================================================
# General util static methods
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries
import configparser


# App Specific libraries
from util.read_file import readFile


# +++++++++++++++++++++++++++
# Get translations from lang_config.ini file
# +++++++++++++++++++++++++++
def getTranslation():
    
    langFile = readFile(r'\Config\lang_config.ini')


    return langFile

