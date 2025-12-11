import sqlite3 as sql
import bcrypt

connection = sql.connect("databaseFiles/database.db")
cursor = connection.cursor()


# cursor.execute(
#    "CREATE TABLE user_data(id INTEGER PRIMARY KEY autoincrement,username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)"
# )
cursor.execute(
    "INSERT INTO user_data(username, password) VALUES ('JohnSoftwareEngineering', 'SecurePassword_1225')"
)

cursor.execute(
    "INSERT INTO user_data(username, password) VALUES ('JaneSoftwareEngineering', 'SecurePassword_1225')"
)

test = input("yes ")

cursor.execute(f"SELECT * FROM user_data WHERE password = '{test}'")
SensitiveInformation = cursor.fetchmany(1)
for i in SensitiveInformation:
    print(i)

connection.close()

# https://www.youtube.com/watch?v=lK-P5kOiQ6Y

### example
# def getUsers():
#    con = sql.connect("databaseFiles/database.db")
#    cur = con.cursor()
#    cur.execute("SELECT * FROM id7-tusers")
#    con.close()
#    return cur
