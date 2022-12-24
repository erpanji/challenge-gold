import sqlite3

conn = sqlite3.connect('data/gold.db')

print("Opened database successfully")

conn.execute('''CREATE TABLE data (sebelumcleansing varchar(15000), sesudah cleansing varchar (15000));''')
print("Table create successfully")

conn.close()