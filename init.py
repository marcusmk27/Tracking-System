import sqlite3

connection = sqlite3.connect('database2024.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('ab0295s', 'testing')
            )

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('ab0296b', 'Mkwanazi1')
            )

connection.commit()
connection.close()