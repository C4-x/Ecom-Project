import sqlite3
from datetime import datetime, timedelta

db = sqlite3.connect('Project.db')
cur = db.cursor()
user_id = 0
logged_in = False


def Login():
    uname = input('Enter Username: ')
    passwd = input('Enter password: ')

    user_result = cur.execute("SELECT username FROM Users WHERE username = ?", (uname,)).fetchone()
    if user_result:
        password_result = cur.execute("SELECT password FROM Users WHERE username = ?", (uname,)).fetchone()
        if password_result[0] == passwd:
            user_id_result = cur.execute("SELECT id FROM Users WHERE username = ?", (uname,)).fetchone()
            global user_id
            user_id = user_id_result[0]
            global logged_in
            logged_in = True
        else:
            print('Invalid password')
    else:
        print('User doesn\'t exist')


def Add_user():
    id = int(input('Enter id: '))
    name = input('Enter name: ')
    email = input('Enter email: ')
    password = input('Enter password: ')
    role = input('Enter role: ')

    cur.execute('INSERT INTO Users(id,name,email,password,role) VALUES(?,?,?,?,?)', (id, name, email, password, role))


def Order():
    items = cur.execute('SELECT * FROM Products;').fetchall()
    for i in items:
        print(i)
    order = int(input('Enter ProductId to Buy (0 to exit): '))
    if order != 0:
        q = int(input('Enter Quantity Required: '))
        eid = cur.execute('SELECT MAX(id) FROM Orders;').fetchone()[0]
        eid = 1 if eid is None else eid + 1

        oid = cur.execute('SELECT MAX(id) FROM Order_items;').fetchone()[0]
        oid = 1 if oid is None else oid + 1

        price = cur.execute('SELECT price FROM Products WHERE id = ?', (order,)).fetchone()[0]
        total_amt = (q * price) + (0.28 * (q * price))  
        status = 'Pending'
        cur.execute('INSERT INTO Orders (id, user_id, date, total_amount, status) VALUES (?,?,?,?,?)',
                    (eid, user_id, datetime.today().strftime('%Y-%m-%d'), total_amt, status))
        cur.execute('INSERT INTO Order_items (id, order_id, product_id, quantity, price) VALUES (?,?,?,?,?)',
                    (oid, eid, order, q, price))  
        db.commit()
        print(f'Order Placed! With Order_id {oid}\n')



def Track_order():
    user_orders = cur.execute('SELECT * FROM Orders WHERE user_id = ?', (user_id,)).fetchall()
    for i in user_orders:
        print(i)
    order_id = int(input('Enter Order_id: '))
    order_det = cur.execute('SELECT * FROM Order_items WHERE order_id = ?', (order_id,)).fetchall()
    product_det = cur.execute('SELECT * FROM Products;').fetchall()
    for i in order_det:
        print(i, product_det[int(i[2]) - 1])


def Admin_Authentication():
    admin_username = input("Enter Admin Username: ")
    admin_password = input("Enter Admin Password: ")

    result = cur.execute('SELECT * FROM Users WHERE username = ? AND role = ?', (admin_username, 'admin')).fetchone()
    if result:
        if result[3] == admin_password:
            print("Admin Login Successful!")
            return True
        else:
            print("Invalid Password!")
    else:
        print("Admin User Not Found!")
    return False





def Sale_Summary():
    total_sales = cur.execute("SELECT SUM(total_amount) FROM Orders WHERE status = 'Completed';").fetchone()[0]
    print("Total Sales: ₹", total_sales)

    period = input("Enter period (day/week/month): ").lower()
    if period == "day":
        date = datetime.today().strftime("%Y-%m-%d")
        total_sales_day = cur.execute("SELECT SUM(total_amount) FROM Orders WHERE date = ? AND status = 'Completed'", (date,)).fetchone()[0]
        print(f"Sales on {date}: ₹", total_sales_day)
    elif period == "week":
        week_start = datetime.today() - timedelta(days=datetime.today().weekday())
        week_start = week_start.strftime("%Y-%m-%d")
        total_sales_week = cur.execute("SELECT SUM(total_amount) FROM Orders WHERE date >= ? AND status = 'Completed'", (week_start,)).fetchone()[0]
        print(f"Sales this week: ₹", total_sales_week)
    elif period == "month":
        month = datetime.today().strftime("%Y-%m")
        total_sales_month = cur.execute("SELECT SUM(total_amount) FROM Orders WHERE strftime('%Y-%m', date) = ? AND status = 'Completed'", (month,)).fetchone()[0]
        print(f"Sales this month: ₹", total_sales_month)


def Inventory_Report():
    products = cur.execute("SELECT * FROM Products;").fetchall()
    for product in products:
        product_id = product[0]
        product_name = product[1]
        total_sold = cur.execute("SELECT SUM(quantity) FROM Order_items WHERE product_id = ?", (product_id,)).fetchone()[0]
        print(f"Product: {product_name}, Total Sold: {total_sold}")


def Product_Management():
    action = input("Would you like to add, update, or remove a product? (add/update/remove): ").lower()
    if action == 'add':
        id = int(input("Enter product ID: "))
        name = input("Enter product name: ")
        description = input("Enter product description: ")
        price = float(input("Enter product price: ").replace(',', ''))
        image_url = input("Enter image URL: ")
        category = input("Enter product category: ")
        stock = int(input("Enter stock quantity: "))
        
        cur.execute("INSERT INTO Products (id, name, description, price, image_url, category, stock) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (id, name, description, price, image_url, category, stock))
        db.commit()
        print("Product added successfully!")
    elif action == 'update':
        product_id = int(input("Enter the product ID to update: "))
        product = cur.execute("SELECT * FROM Products WHERE id = ?", (product_id,)).fetchone()
        
        if product:
            print("Current details:", product)
            name = input(f"Enter new name (current: {product[1]}): ") or product[1]
            description = input(f"Enter new description (current: {product[2]}): ") or product[2]
            price = input(f"Enter new price (current: {product[3]}): ") or product[3]
            price = float(price.replace(',', '')) if price else product[3]  
            image_url = input(f"Enter new image URL (current: {product[4]}): ") or product[4]
            category = input(f"Enter new category (current: {product[5]}): ") or product[5]
            stock = input(f"Enter new stock quantity (current: {product[6]}): ") or product[6]
            stock = int(stock)  
            cur.execute("UPDATE Products SET name = ?, description = ?, price = ?, image_url = ?, category = ?, stock = ? WHERE id = ?", 
                        (name, description, price, image_url, category, stock, product_id))
            db.commit()
            print("Product updated successfully!")
        else:
            print("Product not found!")
    elif action == 'remove':
        product_id = int(input("Enter the product ID to remove: "))
        
        product = cur.execute("SELECT * FROM Products WHERE id = ?", (product_id,)).fetchone()
        if product:
            cur.execute("DELETE FROM Products WHERE id = ?", (product_id,))
            db.commit()
            print("Product removed successfully!")
        else:
            print("Product not found!")



def Admin_Panel():
    if Admin_Authentication():
        print("\nWelcome to the Admin Panel!\n")
        while True:
            print("1) Sale Summary\n2) Inventory Report\n3) Product Management\n4) Exit")
            choice = int(input("Enter choice: "))
            if choice == 1:
                Sale_Summary()
            elif choice == 2:
                Inventory_Report()
            elif choice == 3:
                Product_Management()
            elif choice == 4:
                break
            else:
                print("Invalid choice!")


Login()
if logged_in:
    choice = int(input('1)Buy\n2)Track Order\n3)Admin Panel\nEnter Choice ==> '))
    if choice == 1:
        Order()
    elif choice == 2:
        Track_order()
    elif choice == 3:
        Admin_Panel()

