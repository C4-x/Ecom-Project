import sqlite3
from datetime import datetime
db = sqlite3.connect('Project.db')
cur = db.cursor()
items = cur.execute('SELECT * FROM Products;').fetchall()
for i in items:
    k = 1
    for j in i:
        d = {1:'ProductId',2:'ProductName',3:'Description',4:'Price',5:'Img',6:'Category',7:'Stock'}
        print(k)
        print(f'{d[k]}:{j}',end=' ')
        k += 1
        print(k)
    print('\n')
