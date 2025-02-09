import MySQLdb
import datetime

db = MySQLdb.connect('localhost','tejsvi','1234','Project')
cur = db.cursor()
user_id = 0
logged_in = False


def Login():
    uname = input('Enter Username: ')
    passwd = input('Enter password: ')

    if cur.execute(f'SELECT username FROM Users WHERE username = \'{uname}\';') != ' ':
        if cur.execute(f'SELECT password FROM Users WHERE username = \'{uname}\';') == passwd:
            global user_id
            user_id = cur.execute(f'SELECT id FROM Users WHERE username = \'{uname}\';')
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

    cur.execute(f'INSERT INTO Users(id,name,email,password,role) VALUES({id},\'{name}\',\'{email}\',\'{password}\',\'{role}\');')


def Order():
    cur.execute('SELECT * FROM Product;')
    order = int(input('Enter ProductId to Buy (0 to exit): '))
    if order != 0:
        eid = cur.execute('SELECT MAX(id) FROM Orders;')
        price = int(cur.execute(f'SELECT price FROM Products WHERE id = {order};'))
        total_amt = price + 0.28 * price
        status = 'Pending'
        cur.execute(f'INSERT INTO Orders(id,user_id,order_date,total_amt,status) VALUES({eid + 1},{user_id},\'{datetime.date()}\',{total_amt},\'{status}\');')
        print('Order Placed!\n')


def Admin_panel():
    if cur.execute(f'SELECT role FROM Users WHERE username = {user_id};') == 'admin':
        print('Welcome Admin!')


Login()
if logged_in:
    choice = int(input('1)Buy\n2)Track Order\n3)Admin Panel\nEnter Choice ==> '))
    if choice == 1:
        Order()
    elif choice == 2:
        pass
    elif choice == 3:
        Admin_panel()
