import sqlite3

conn = sqlite3.connect("example.db")

cur = conn.cursor()

cur.execute('SELECT * from customer_churn')

# for row in cur.execute('SELECT * FROM customer_churn'):
# 	print(row)

customerID = ('7590-VHVEG',)
cur.execute('SELECT * FROM customer_churn WHERE field1 = ?', customerID)
# print(cur.fetchone())

#cur.execute("INSERT INTO consumer VALUES (1,'John Doe','john.doe@xyz.com','A')")

# for row in cur.execute('SELECT * from consumer'):
# 	print(row)
cur.execute("SELECT * FROM consumer")
purchases = [(2,'John Paul','john.paul@xyz.com','B'),
             (3,'Chris Paul','john.paul@xyz.com','A'),
            ]

#cur.executemany('INSERT INTO consumer VALUES (?, ?, ?, ?)', purchases)

for row in cur.execute('SELECT * FROM consumer'):
	print(row)

conn.commit()
conn.close()