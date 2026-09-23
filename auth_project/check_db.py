import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT id, username, email FROM users")

rows = cursor.fetchall()

print("Users in database:\n")

for row in rows:
    print(row)

conn.close()