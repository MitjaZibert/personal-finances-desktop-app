# ===========================================================================================
# Data class for table views
# ===========================================================================================
# ===========================================================================================
from dataclasses import dataclass, field

@dataclass
class Table():
    #tableClassInstance: 
    tableObject: str # window table object
    tableModel: str # TableModel class - QAbstractTableModel
    db_columns: list # columns in the same order as in the query - importnat only for updatable tables (e.g. Incomes)
    query: str # sql query
    query_args: list # dictionary of query parameters (e.g. incomes_sum_id)
    geometry: list[int] = field(default_factory=[0, 0, 0, 0]) # table dimensions (x, y, w, h)
    columnWidths: list[int] = field(default_factory=[]) # if 0 --> column is hidden
    tableEnabled: bool = True # if True --> table cells are editable in accordance with columnEditable parameter (False is set when month is closed)
    columnEditable: list[bool] = field(default_factory=[]) # if True --> column is editable
    roundedNumber: list[int] = field(default_factory=[]) # if > 0 --> column is rounded to given decimals
    columnCheckBox: list[bool] = field(default_factory=[]) # if True --> column is checkbox