

import os
import json

INVENTORY_FILE = "inventory.txt"

class InventoryItem:
    """Represents a single inventory item."""
    def __init__(self, name, quantity, cost, verified=False):
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.verified = verified

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "cost": self.cost,
            "verified": self.verified
        }

    @staticmethod
    def from_dict(data):
        return InventoryItem(
            data.get("name", ""),
            data.get("quantity", 0),
            data.get("cost", 0.0),
            data.get("verified", False)
        )

class Inventory:
    """Handles inventory operations and file storage."""
    def __init__(self, filename=INVENTORY_FILE):
        self.filename = filename
        self.items = self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [InventoryItem.from_dict(item) for item in data]
        except Exception:
            print("Error: Could not load inventory file. Starting with empty inventory.")
            return []

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump([item.to_dict() for item in self.items], f)
        except Exception:
            print("Error: Could not save inventory.")

    def add_item(self, item):
        self.items.append(item)
        self.save()

    def update_item(self, idx, name=None, quantity=None, cost=None):
        item = self.items[idx]
        if name:
            item.name = name
        if quantity is not None:
            item.quantity = quantity
        if cost is not None:
            item.cost = cost
        self.save()

    def verify_item(self, idx):
        self.items[idx].verified = True
        self.save()

    def delete_item(self, idx):
        del self.items[idx]
        self.save()

class InventoryCLI:
    """Command-line interface for the inventory system."""
    def __init__(self):
        self.inventory = Inventory()

    def add_item(self):
        name = input("Enter item name: ").strip()
        if not name:
            print("Item name cannot be empty.")
            return
        try:
            quantity = int(input("Enter quantity: "))
            cost = float(input("Enter cost per item: "))
        except ValueError:
            print("Invalid input. Quantity must be an integer and cost a number.")
            return
        item = InventoryItem(name, quantity, cost)
        self.inventory.add_item(item)
        print(f"Item '{name}' added.")
        print("\033[92mSuccess!\033[0m")

    def view_items(self):
        if not self.inventory.items:
            print("Inventory is empty.")
            return
        print("\nCurrent Inventory:")
        for idx, item in enumerate(self.inventory.items, 1):
            status = "Checked" if item.verified else "Not Checked"
            print(f"{idx}. Name: {item.name}, Qty: {item.quantity}, Cost: {item.cost}, Status: {status}")

    def update_item(self):
        self.view_items()
        if not self.inventory.items:
            return
        try:
            idx = int(input("Enter item number to update: ")) - 1
            if idx < 0 or idx >= len(self.inventory.items):
                print("Invalid item number.")
                return
            item = self.inventory.items[idx]
            print(f"Updating '{item.name}' (leave blank to keep current value)")
            name = input(f"New name [{item.name}]: ").strip() or item.name
            quantity_input = input(f"New quantity [{item.quantity}]: ").strip()
            cost_input = input(f"New cost [{item.cost}]: ").strip()
            quantity = int(quantity_input) if quantity_input else item.quantity
            cost = float(cost_input) if cost_input else item.cost
            self.inventory.update_item(idx, name, quantity, cost)
            print("Item updated.")
            print("\033[92mSuccess!\033[0m")
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error: {e}")

    def verify_item(self):
        self.view_items()
        if not self.inventory.items:
            return
        try:
            idx = int(input("Enter item number to verify: ")) - 1
            if idx < 0 or idx >= len(self.inventory.items):
                print("Invalid item number.")
                return
            self.inventory.verify_item(idx)
            print(f"Item '{self.inventory.items[idx].name}' marked as checked.")
            print("\033[92mSuccess!\033[0m")
        except ValueError:
            print("Invalid input.")

    def delete_item(self):
        self.view_items()
        if not self.inventory.items:
            return
        try:
            idx = int(input("Enter item number to delete: ")) - 1
            if idx < 0 or idx >= len(self.inventory.items):
                print("Invalid item number.")
                return
            name = self.inventory.items[idx].name
            self.inventory.delete_item(idx)
            print(f"Item '{name}' deleted.")
            print("\033[92mSuccess!\033[0m")
        except ValueError:
            print("Invalid input.")

    def print_banner(self):
        # Simpler colored title, no lines
        print("\033[96mInventory Management System\033[0m")

    def main_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            print("\033[92m1. Add Item\033[0m")
            print("\033[92m2. View Items\033[0m")
            print("\033[92m3. Update Item\033[0m")
            print("\033[92m4. Verify Item\033[0m")
            print("\033[92m5. Delete Item\033[0m")
            print("\033[91m6. Exit\033[0m")
            choice = input("\033[94mChoose an option (1-6): \033[0m").strip()
            if choice == '1':
                self.add_item()
                input("Press Enter to continue...")
            elif choice == '2':
                self.view_items()
                input("Press Enter to continue...")
            elif choice == '3':
                self.update_item()
                input("Press Enter to continue...")
            elif choice == '4':
                self.verify_item()
                input("Press Enter to continue...")
            elif choice == '5':
                self.delete_item()
                input("Press Enter to continue...")
            elif choice == '6':
                print("\033[95mExiting. Goodbye!\033[0m")
                break
            else:
                print("\033[91mInvalid choice. Please select 1-6.\033[0m")
                input("Press Enter to continue...")

if __name__ == "__main__":
    InventoryCLI().main_menu()
