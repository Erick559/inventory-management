# Inventory Management System:
A simple Python system that handles day to day inventory management tasks.

## Overview:
This is a simple inventory management system implemented in Python using SQLite for data storage. 
The system allows users to add items to the inventory, update item quantities, and view the current inventory.

## Features:
- Creates a new database named Inventory if one does not exist
- Add items to the inventory with unique item IDs, names, and quantities.
- Update the quantity of an existing item in the inventory.
- View the current inventory, displaying item IDs, names, and quantities.

## Limitations
- The system can't update already existing items

## Requirements:
- Python 3.10
- Pysqlite3

## Usage:
1. Clone the repository: `git clone https://github.com/Erick559/inventory-management.git`
   
2. Install Python 3.10
 - For Windows visit [python.org](python.org)  and click the download button
   
 - For Linux open your terminal and paste the following commands:
   `$ sudo apt-get update`
   `$ sudo apt-get install python3.6`

3. Install pysqlite3:
   - For both Windows and Linux run the following command:
     `pip install pysqlite3`

4. To run the python file paste the command to either powershell or cmd:
   `python3 inventory_management.py


