
# ===========================================================================================
# General util static methods
# ===========================================================================================
# ===========================================================================================

# Imports:

# System libraries
from os import path
import configparser

# App Specific libraries
import globals


# +++++++++++++++++++++++++++
# Return selected file data/content
# +++++++++++++++++++++++++++
def readFile(file_name, rootPath = False):
   
    # Add app path to the file name
    if rootPath:
        file_name = globals.root_path + file_name
    else:
        file_name = globals.app_path + file_name

    
    file = path.join(path.dirname(__file__), file_name)
    
    fileContent = configparser.ConfigParser()
    fileContent.read(file, encoding="utf8")

    # Get the value and replace the literal \n with actual newline
    # Process all sections and their key-value pairs
    for section in fileContent.sections():
        for key in fileContent[section]:
            fileContent[section][key] = fileContent[section][key].replace('\\n', '\n')

    return fileContent

# *********************************************************************************************
# *********************************************************************************************
# USEFUL NOTES
# *********************************************************************************************
# #list all sections and all items
# for each_section in conf.sections():
#     for (each_key, each_val) in conf.items(each_section):
#         print each_key
#         print each_val