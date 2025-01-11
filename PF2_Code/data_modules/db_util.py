# ===========================================================================================
# Database interaction static methods
# ===========================================================================================
# ===========================================================================================

# Imports:

# Sys libraries

# App Specific libraries
#from .db_connect import getConn
import globals

class DB_Util():
    def __init__(self):

        # DB connection
        #self.conn = getConn()
        self.conn = globals.current_db_conn

    # +++++++++++++++++++++++++++
    # Execute SQL query and return data
    # +++++++++++++++++++++++++++
    def getData(self, query: str, args = None):
        cur = self.conn.cursor()
        cur.execute(query, args)
        cur.close()

        return cur

    # +++++++++++++++++++++++++++
    # Execute DDL (insert/update/delete)
    # +++++++++++++++++++++++++++
    def executeDDL (self, ddl: str):
        cur = self.conn.cursor()
        cur.execute(ddl)
        cur.close()

    # +++++++++++++++++++++++++++
    # Call db procedure
    # +++++++++++++++++++++++++++
    def callDBProc(self, proc_name: str, inParam1 = None):
        cur = self.conn.cursor()
        if inParam1 != None:
            cur.callproc(proc_name, [inParam1, ])
        else:
            cur.callproc(proc_name)

        cur.close()

    # +++++++++++++++++++++++++++
    # Save (commit)
    #++++
    def saveData(self):
        self.conn.commit()

    # +++++++++++++++++++++++++++
    # Rollback 
    #++++
    def rollbackData(self):
        self.conn.rollback()

    # +++++++++++++++++++++++++++
    # Insert data
    #++++
    # def insertData(self, insert_stmt: str):
    #     self.executeDDL(ddl = insert_stmt)

    # # +++++++++++++++++++++++++++
    # # Update data
    # #++++
    # def updateData(self, update_stmt: str):
    #         self.executeDDL(ddl = update_stmt)

    # # +++++++++++++++++++++++++++
    # # Delete row
    # #++++
    # def deleteRow(self, delete_stmt: str):
    #     self.executeDDL(ddl = delete_stmt)

    

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # NOTES
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
    # conn timeout - how to solve?


    # using parameters
    # cells = ('cell_1', 'cell_2')
    # cursor.execute('select count(*) from instance where cell_name in %(cell_names)s;', {'cell_names': cells})
    # # or alternately
    # cursor.execute('select count(*) from instance where cell_name in %s;', [cells])
    # If args is a list or tuple, %s can be used as a placeholder in the query. 
    # If args is a dict, %(name)s can be used as a placeholder in the query.