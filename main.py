import sqlite3
from datetime import datetime

db = sqlite3.connect('Project.db')
cur = db.cursor()
user_id = 0
logged_in = False


def Login():
    uname = input('Enter Username: ')
    passwd = input('Enter password: ')

    if (''.join(x for x in str(cur.execute(f'SELECT username FROM Users WHERE username = \'{uname}\';').fetchone()) if x.isalpha())) != ' ':
        if ''.join(x for x in str(cur.execute(f'SELECT password FROM Users WHERE username = \'{uname}\';').fetchone()) if x.isalnum()) == passwd:
            global user_id
            user_id = int(''.join(x for x in str(cur.execute(f'SELECT id FROM Users WHERE username = \'{uname}\';').fetchone()) if x.isdigit()))
            global logged_in
            logged_in = True
    else:
        print('Invalid Credentials!!')


def Add_user():
    id = int(input('Enter id: '))
    name = input('Enter name: ')
    email = input('Enter email: ')
    password = input('Enter password: ')
    role = input('Enter role: ')

    cur.execute(f'INSERT INTO Users(id,name,email,password,role) VALUES({id},{name},{email},{password},{role});')


def Order():
    items = cur.execute('SELECT * FROM Products;').fetchall()
    for i in items:
        print(i)
    order = int(input('Enter ProductId to Buy (0 to exit): '))
    if order != 0:
        q = int(input('Enter Quantity Required: '))
        # primary key of Orders
        eid = int(''.join(x for x in str(cur.execute('SELECT MAX(id) FROM Orders;').fetchone()) if x.isdigit()))
        # primary key of Order_items
        oid = int(''.join(x for x in str(cur.execute('SELECT MAX(id) FROM Order_items;').fetchone()) if x.isdigit()))
        price = int(''.join(x for x in str(cur.execute(f'SELECT price FROM Products WHERE id = {order};').fetchone()) if x.isdigit()))
        total_amt = (q * price) + (0.28 * (q * price))
        status = 'Pending'
        cur.execute(f'INSERT INTO Orders VALUES ({eid + 1},{user_id},\'{datetime.today().strftime("%Y-%m-%d")}\',{total_amt},\'{status}\');')
        cur.execute(f'INSERT INTO Order_items VALUES ({oid + 1},{eid + 1},{order},{q},{price})')
        db.commit()
        print(f'Order Placed! With Order_id {oid + 1}\n')


def Track_order():
    user_orders = cur.execute(f'SELECT * FROM Orders WHERE user_id = \'{user_id}\';').fetchall()
    for i in user_orders:
        print(i)
    order_id = int(input('Enter Order_id: '))
    order_det = cur.execute(f'SELECT * FROM Order_items WHERE order_id = \'{order_id}\';').fetchall()
    product_det = cur.execute('SELECT * FROM Products;').fetchall()
    for i in order_det:
        print(i,product_det[(int(i[2]) - 1)])


def Admin_panel():
    if 'admin' in str(cur.execute(f'SELECT role FROM Users WHERE username = \'{user_id}\';').fetchone()):
        print('Welcome Admin!')


Login()
if logged_in:
    choice = int(input('1)Buy\n2)Track Order\n3)Admin Panel\nEnter Choice ==> '))
    if choice == 1:
        Order()
    elif choice == 2:
        Track_order()
    elif choice == 3:
        Admin_panel()
