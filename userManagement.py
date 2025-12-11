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
test2 = input("no ")
test = input("yes ")

validatedtest = 

for i in test:
    if i == "'":
        print("nuh uh")
    else:
        validatedtest = validatedtest + i

cursor.execute(
    f"SELECT * FROM user_data WHERE username = '{test2}' AND password = '{test}'"
)
SensitiveInformation = cursor.fetchall()
if SensitiveInformation == "":
    print("username or password is incorrect.")
else:
    print("you have been logged in!")

# if username and password combination brings results from sql database, log user in
# if not, say incorrect username or password

connection.close()

# https://www.youtube.com/watch?v=lK-P5kOiQ6Y

### example
# def getUsers():
#    con = sql.connect("databaseFiles/database.db")
#    cur = con.cursor()
#    cur.execute("SELECT * FROM id7-tusers")
#    con.close()
#    return cur
