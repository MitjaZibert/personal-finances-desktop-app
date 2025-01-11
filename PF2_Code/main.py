# ===========================================================================================
# Personal Finances App v.2
# ===========================================================================================

# Imports 


# System libraries
import sys
from PyQt6.QtWidgets import QApplication

# PyQt Windows libraries
from win_main import WinMain

# App Specific libraries
import globals

# =================================================
if __name__ == "__main__":
    try:
        # Set initial global variables
        globals.set_globals()

        # Run App 
        app = QApplication(sys.argv)
        
        # Create and show window
        mainWindow = WinMain()
        mainWindow.show()
        
        # Start event loop
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")  # Catch any exceptions

# *********************************************************************************************
# *********************************************************************************************
# NOTES
# *********************************************************************************************



