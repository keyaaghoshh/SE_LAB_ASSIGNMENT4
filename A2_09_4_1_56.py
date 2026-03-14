import sqlite3


db = sqlite3.connect("A2_09_4_1_56.db")

cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

db.commit()


def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))

    sql = "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)"
    cursor.execute(sql, (name, price, quantity))
    db.commit()

    print("Product added successfully.")


def view_products():
    cursor.execute("SELECT * FROM products")

    rows = cursor.fetchall()

    if not rows:
        print("No products found.")
    else:
        for row in rows:
            print(row)


def update_product():
    pid = int(input("Enter product ID: "))
    quantity = int(input("Enter new quantity: "))

    sql = "UPDATE products SET quantity=? WHERE id=?"
    cursor.execute(sql, (quantity, pid))
    db.commit()

    print("Product updated.")


def delete_product():
    pid = int(input("Enter product ID: "))

    cursor.execute("DELETE FROM products WHERE id=?", (pid,))
    db.commit()

    print("Product deleted.")


def purchase_product():
    pid = int(input("Enter product ID: "))
    qty = int(input("Enter quantity: "))

    cursor.execute("SELECT price, quantity FROM products WHERE id=?", (pid,))
    result = cursor.fetchone()

    if result:
        price, stock = result

        if stock >= qty:
            total = price * qty

            cursor.execute(
                "UPDATE products SET quantity = quantity - ? WHERE id=?",
                (qty, pid)
            )

            cursor.execute(
                "INSERT INTO purchases (product_id, quantity, total_price) VALUES (?, ?, ?)",
                (pid, qty, total)
            )

            db.commit()

            print("Purchase successful. Total =", total)

        else:
            print("Not enough stock.")

    else:
        print("Product not found.")


def view_purchase_history():
    cursor.execute("SELECT * FROM purchases")

    rows = cursor.fetchall()

    if not rows:
        print("No purchases yet.")
    else:
        for row in rows:
            print(row)



while True:

    print("\n===== Inventory System =====")
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Purchase Product")
    print("6. View Purchase History")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_product()

    elif choice == "2":
        view_products()

    elif choice == "3":
        update_product()

    elif choice == "4":
        delete_product()

    elif choice == "5":
        purchase_product()

    elif choice == "6":
        view_purchase_history()

    elif choice == "7":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Try again.")
