import sqlite3
import threading
from contextlib import contextmanager

class Item:
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity

class InventorySystem:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.create_table_if_not_exists()
        self.lock = threading.Lock()

    def create_table_if_not_exists(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')
            

    def add_item(self, item_id, name, quantity):
            with self.connection:
                try:
                    self.connection.execute('''
                        INSERT INTO inventory (item_id, name, quantity)
                        VALUES (?, ?, ?)
                        ''', (item_id, name, quantity))
                    print(f"Item added: Item ID: {item_id}, Name: {name}, Quantity: {quantity}")
                except sqlite3.IntegrityError:
                    self.update_item_quantity(item_id, quantity)

    def update_item_quantity(self, item_id, quantity):
        with self.lock:
            with self.connection:
                self.connection.execute('''
                    UPDATE inventory
                    SET quantity = ?
                    WHERE item_id = ?
                ''', (quantity, item_id))
                print(f"Item quantity updated: Item ID: {item_id}, New Quantity: {quantity}")

    def get_item(self, item_id):
        with self.lock:
            cursor = self.connection.execute('''
                SELECT item_id, name, quantity
                FROM inventory
                WHERE item_id = ?
            ''', (item_id,))
            row = cursor.fetchone()
            if row:
                item = Item(*row)
                print(f"Item retrieved: Item ID: {item.item_id}, Name: {item.name}, Quantity: {item.quantity}")
                return item
            return None

    def view_inventory(self):
        with self.lock:
            cursor = self.connection.execute('''
                SELECT item_id, name, quantity
                FROM inventory
            ''')
            for row in cursor:
                item = Item(*row)
                print(f"Item ID: {item.item_id}, Name: {item.name}, Quantity: {item.quantity}")

def main():
    db_file = "inventory.db"
    inventory_system = InventorySystem(db_file)

    print("Database connection established.")
    print("Inventory table created.")

    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. Update Item Quantity")
        print("3. View Inventory")
        print("0. Exit")
        choice = input("Enter your choice: ")
        print("")

        if choice == '1':
            try:
                item_id = int(input("Enter Item ID: "))
                name = input("Enter Item Name: ")
                quantity = int(input("Enter Quantity: "))
                inventory_system.add_item(item_id, name, quantity)
            except ValueError:
                print("Invalid input. Please enter valid numeric values.")

        elif choice == '2':
            try:
                item_id = int(input("Enter Item ID: "))
                quantity = int(input("Enter New Quantity: "))
                inventory_system.update_item_quantity(item_id, quantity)
            except ValueError:
                print("Invalid input. Please enter valid numeric values.")

        elif choice == '3':
            inventory_system.view_inventory()

        elif choice == '0':
            print("Exiting the system.")
            inventory_system.connection.commit()
            inventory_system.connection.close()
            break

        inventory_system.connection.commit()

if __name__ == "__main__":
    main()
