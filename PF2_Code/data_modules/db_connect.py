# ===========================================================================================
# Database interaction static methods
# ===========================================================================================
# ===========================================================================================

# Imports:

# Sys libraries
import pymysql

# App Specific libraries
from util.read_file import readFile
import globals

# ===========================================================================================

# Global variables
conf_host = None
conf_port = None
conf_user = None
conf_pass = None
conf_db = None

# +++++++++++++++++++++++++++
# Define MySQL connector
# +++++++++++++++++++++++++++
def _defineConnectionParameters():

    # set db config data
    db_config_file = readFile(r'\Config\db_config.ini')
    
    global conf_host
    conf_host = db_config_file[globals.app_db]['host']
    global conf_port
    conf_port = int(db_config_file[globals.app_db]['port'])
    global conf_user
    conf_user = db_config_file[globals.app_db]['user']
    global conf_pass
    conf_pass = db_config_file[globals.app_db]['pass']
    global conf_db
    conf_db = db_config_file[globals.app_db]['db']

# +++++++++++++++++++++++++++
# Connect to MySql DB
# +++++++++++++++++++++++++++
def getConn():
    
    # Check if db connection parameters are already defined
    if not conf_host:
        _defineConnectionParameters()

    # Connect to database
    try:
        conn = pymysql.connect(host=conf_host, port=conf_port, user=conf_user, passwd=conf_pass, db=conf_db)
        return conn
        
    except pymysql.err.OperationalError:
        print('Unable to make a connection to the mysql database.')
        return None

# +++++++++++++++++++++++++++
# Close MySql DB connection
#++++
def closeConn():
    globals.current_db_conn.close()

