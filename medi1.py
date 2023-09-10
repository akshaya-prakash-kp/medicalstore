import mysql.connector


class MedicalStoreManagementSystem:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(host="localhost", user="root", password="04052003", database="medi1")
        self.create_tables()
        self.admin_username = "akshaya"
        self.admin_password = "123"

    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS medicines1 (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL,quantity INT,price INT)''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers1 (id INT AUTO_INCREMENT PRIMARY KEY,first_name VARCHAR(50) NOT NULL, 
            last_name VARCHAR(50) NOT NULL, phone_number VARCHAR(15),
                username VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL
            )
        ''')

        self.conn.commit()

    def admin_login(self):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        if username == self.admin_username and password == self.admin_password:
            print("Welcome admin")
            self.admin_actions()
        else:
            print("Invalid ")

    def admin_actions(self):
        while True:
            print("\nMEDICAL STORE MANAGEMENT SYSTEM ")
            print("1. Delete User")
            print("2. Display Users")
            print("3. Add Medicine")
            print("4. Display Medicines")
            print("5. Delete Medicine")
            print("6. Update Medicine")
            print("7. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                username = input("Enter username  to delete:")
                self.delete_user(username)
            elif choice == "2":
                self.display_users()
            elif choice == "3":
                medicine_name = input("Enter medicine name: ")
                quantity = input("enter the quantity of medicine")
                price = input("enter the price")
                exp_date = input("enter exp date")
                self.add_medicine(medicine_name, quantity, price, exp_date)
            elif choice == "4":
                self.display_medicines()
            elif choice == "5":
                medicine_name = input("Enter medicine name to delete: ")
                self.delete_medicine(medicine_name)
            elif choice == "6":
                medicine_name = input("Enter medicine name to update: ")
                self.update_medicine(medicine_name)
            elif choice == "7":
                break
            else:
                print("Invalid choice")

    def delete_user(self, username):
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM customers1 WHERE username=%s", (username,))
            if cursor.rowcount > 0:
                self.conn.commit()
                print("User", username, "deleted.")
            else:
                print("User", username, "does not exist.")

    def display_users(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT username FROM customers1")
            users = cursor.fetchall()
            if not users:
                print("No users found.")
            else:
                print("\nList of Users:")
                for row in users:
                    print(f"Username: {row[0]}")

    def add_medicine(self, medicine_name, quantity, price, exp_date):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM medicines1 WHERE name=%s", (medicine_name,))
            medicine_exists = cursor.fetchone()[0]
            if medicine_exists > 0:
                print(f"Medicine",medicine_name," added.")

                print(f"Medicine ",medicine_name,"already exists.")
            else:
                cursor.execute(
                    "INSERT INTO medicines1 (name, quantity, price, exp_date) VALUES (%s,%s, %s, %s)",
                    (medicine_name, quantity, price, exp_date)
                )
                self.conn.commit()
    def display_medicines(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT name, quantity, price FROM medicines1")
            medicines = cursor.fetchall()
            if not medicines:
                print("No medicines found.")
            else:
                print("\nList of Medicines:")
                for row in medicines:
                    medicine_name, quantity, price = row
                    print(f" Name: {medicine_name}, Quantity: {quantity}, Price: {price}")

    def delete_medicine(self, medicine_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM medicines1 WHERE name=%s", (medicine_name,))
            medicine_count = cursor.fetchone()[0]
            if medicine_count > 0:
                cursor.execute("DELETE FROM medicines1 WHERE name=%s", (medicine_name,))
                self.conn.commit()
                print("Medicine", medicine_name, "deleted.")
            else:
                print("Medicine", medicine_name, "does not exist.")

    def customer_login(self):
        username = input("Enter customer username: ")
        password = input("Enter customer password: ")
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM customers1 WHERE username = %s AND password = %s", (username, password))
            customer_id = cursor.fetchone()

        if customer_id:
            print("Welcome customer")
            self.customer_actions()
        else:
            print("Invalid username or password")

    def customer_register(self):
        id = input("enter the id:")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        phone_number = input("Enter your phone number: ")
        username = input("enter the username")
        password = input("Enter a password: ")
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO customers1 ( id,first_name, last_name, phone_number,username, password) VALUES (%s, %s,%s, %s, %s, %s)",
                (id, first_name, last_name, phone_number, username, password)
            )
            self.conn.commit()
            print("Account created successfully. You can now log in.")

    def update_medicine(self, medicine_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT quantity, price FROM medicines1 WHERE name=%s", (medicine_name,))
            medicine_data = cursor.fetchone()

            if not medicine_data:
                print("Medicine", medicine_name, "does not exist.")
                return

            new_quantity = input("Enter new quantity  ")
            new_price = input("Enter new price  ")

            cursor.execute("UPDATE medicines1 SET quantity=%s, price=%s WHERE name=%s",
                           (new_quantity, new_price, medicine_name))
            self.conn.commit()

            print("Medicine", medicine_name, "updated successfully.")

    def customer_actions(self):
        while True:
            print("\nMEDICAL STORE MANAGEMENT SYSTEM - Customer Actions")
            print("1. Display Medicines")
            print("2. Purchase Medicine")
            print("3. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.display_medicines()
            elif choice == "2":
                medicine_name = input("Enter medicine name to purchase: ")
                self.purchase_medicine(medicine_name)
            elif choice == "3":
                break
            else:
                print("Invalid choice")

    def purchase_medicine(self, medicine_name):
        quantity = int(input("Enter the quantity of medicine you want to purchase: "))

        with self.conn.cursor() as cursor:
            cursor.execute("SELECT quantity, price FROM medicines1 WHERE name=%s", (medicine_name,))
            medicine_data = cursor.fetchone()

            if medicine_data:
                available_quantity, default_price = medicine_data
                if available_quantity >= quantity:
                    total_price = quantity * default_price
                    remaining_quantity = available_quantity - quantity

                    cursor.execute("UPDATE medicines1 SET quantity=%s WHERE name=%s",
                                   (remaining_quantity, medicine_name))
                    self.conn.commit()

                    print("You have purchased", quantity, "units of", medicine_name, "for a total price of",
                          total_price)
                else:
                    print("Insufficient quantity of", medicine_name, "available.")
            else:
                print("Medicine", medicine_name, "does not exist.")

    def __del__(self):
        self.conn.close()


def main():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "04052003",
        "database": "medi1"
    }
    system = MedicalStoreManagementSystem(**db_config)

    while True:
        print("\n1. Admin Login")
        print("2. Customer Login")
        print("3. Customer Registration")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            system.admin_login()
        elif choice == "2":
            system.customer_login()
        elif choice == "3":
            system.customer_register()
        elif choice == "4":
            print("Exiting the program")
            break
        else:
            print("Invalid choice")


main()
