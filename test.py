import sqlite3
from datetime import datetime
db = sqlite3.connect('Project.db')
cur = db.cursor()
print(''.join(x for x in str(cur.execute(f'SELECT price FROM Products WHERE id = 1;').fetchone()) if x.isdigit()))
print(int(''.join(x for x in str(cur.execute(f'SELECT id FROM Users WHERE username = \'admin\';').fetchone()) if x.isdigit())))


