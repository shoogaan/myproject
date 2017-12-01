import sqlite3

with sqlite3.connect("myflaskapp.db") as connection:

    c = connection.cursor()

    c.execute("DROP TABLE users")

    c.execute("""CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        name CHAR(100) NOT NULL,
        username CHAR(30) NOT NULL UNIQUE,
        email CHAR(100) NOT NULL UNIQUE,
        password CHAR(100) NOT NULL,
        register_date DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME'))
        )""")

    c.execute('INSERT INTO users VALUES(1, "Bob", "Bobino", "bob@bobino.com", "12345", "2016-02-03 17:51:28")')

    c.execute('INSERT INTO users VALUES(2, "Jane", "Janis", "jane@janis.com", "12345", "2016-02-03 17:51:28")')

    c.execute('INSERT INTO users VALUES(3, "Elvis", "Presley", "elvis@presley.com", "12345", "2016-02-03 17:51:28")')
