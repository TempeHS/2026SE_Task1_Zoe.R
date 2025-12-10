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

user = input("user: ")
password = input("password: ")

cursor.execute(
    "SELECT * FROM user_data WHERE username = ? AND password = ?",
    (user, password),
)
SensitiveInformation = cursor.fetchall()
for i in SensitiveInformation:
    print(i)

connection.close()


### example
# def getUsers():
#    con = sql.connect("databaseFiles/database.db")
#    cur = con.cursor()
#    cur.execute("SELECT * FROM id7-tusers")
#    con.close()
#    return cur
