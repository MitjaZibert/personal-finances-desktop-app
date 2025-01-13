# Personal Finance Desktop App

## Overview
The **Personal Finance Desktop App** is a Python-based application designed to help users manage their finances effectively. Built with **PyQt6** for the user interface and **MySQL** for server-side data management, the app provides a comprehensive set of features for tracking incomes, expenses, and yearly financial projection. 

The app dynamically generates and populates data tables using `QAbstractTableModel`, with all table definitions centralized in a `table_definitions.py` file. This modular approach ensures flexibility and maintainability.

---

## Key Features
- **Monthly Overview**: View a clear summary of incomes and expenses for each month.
- **Financial Projections**: A 12-month financial projection based on regular incomes and expenses.
- **Money Allocation**: Track current money allocation across various categories (e.g., bank accounts, cash, savings, assets).
- **Detailed Insights**:
  - Monthly incomes overview.
  - Monthly expense overview.
- **Category Registries**:
  - Income categories.
  - Regular income categories.
  - Expense categories.
  - Regular expense categories (configurable for specific months).
- **Multi-Currency Support**:
  - Automatically updated currency exchange rates.
- **Monthly Balance Summary**: Clear display of monthly balance and available funds.
- **Month Locking**: Lock individual months after closing incomes and expenses.
- **Data Management**:
  - Add or delete individual monthly incomes and expenses.
  - Transfer incomes and expenses to a new month.
- **Multi-Language Support**: Easily configurable translations via a `lang_config.ini` file.

---

## Technical Details
### Backend
- **Database**: The app uses a relational database consisting of 12 tables modeled in **Third Normal Form (3NF)**. 
- **Triggers and Procedures**: Database triggers and procedures are implemented to handle data manipulation on the server side.

### Frontend
- **PyQt6**: The app's GUI is built using PyQt6, providing a modern and responsive user interface.
- **Dynamic Table Management**: Data tables are dynamically generated and populated using `QAbstractTableModel`. All table definitions are stored in a centralized `table_definitions.py` file.

#### Example Table Definition:
```python
# tableView_Allocation: Money Allocation data
tableDict["tableView_Allocation"] = Table(
    tableObject=windowClass.ui.tableView_Allocation,
    tableModel=TableModel,
    db_columns=["alloc_id", "curr_id", "allocation", "alloc_amount", "curr_code", "value", "alloc_desc", "available"],
    query="""SELECT M.ALLOC_ID, C.CURR_ID, M.ALLOCATION, M.ALLOC_AMOUNT, C.CURR_CODE, M.VALUE, M.ALLOC_DESC, M.AVAILABLE 
             FROM MONEY_ALLOCATION M
             INNER JOIN REG_CURRENCY C ON M.CURR_ID = C.CURR_ID 
             ORDER BY M.AVAILABLE DESC, M.VALUE DESC, M.ALLOCATION;""",
    query_args=[],
    geometry=[10, 10, 600, 270],
    columnWidths=[0, 0, 130, 70, 70, 70, 170, 40],
    tableEnabled=True,
    columnEditable=[True, True, True, True, True, False, True, True],
    roundedNumber=[0, 0, 0, 2, 0, 2, 0, 0],
    columnCheckBox=[0, 0, 0, 0, 0, 0, 0, 1]
)
```

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/personal-finance-app.git
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
   - Import the provided SQL schema into your MySQL server.
   - Update the database connection details in the app's configuration file.

4. Run the application:
   ```bash
   python main.py
   ```

---

## Usage
- Configure your regular incomes and expenses.
- Use the monthly overview to track your financial balance.
- Lock months after finalizing your data to prevent accidental changes.
- Explore yearly balance projection to plan your finances effectively.

---

## Contributing
This is a showcase project and is not published for accepting contributions! But, feel free to fork the repository and use it for your own, personal needs.

---

## License
This project is not licensed.

---

## Screenshots
![ERD - Personal Finances v2](https://github.com/user-attachments/assets/54a05314-d4ce-4259-87cc-fb32adc27fb1)
