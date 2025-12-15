import sqlite3 as sql
import bcrypt


# this was an example i'm just leaving it in here in case i need to use it
def getdata():
    connection = sql.connect("databaseFiles/database.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    connection.close()
    return cursor


# authenticates login
def loginput(user, pwd):
    connection = sql.connect("databaseFiles/database.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM user_data WHERE username = ?", (user,))
    details = cursor.fetchall()
    connection.close()
    if details == []:
        print("login failed!")
        return False
    else:
        hashedinput = pwd.encode("utf-8")
        return bcrypt.checkpw(hashedinput, details[0])


# adds user
def signupinput(user, pwd):
    try:
        connection = sql.connect("databaseFiles/database.db", check_same_thread=False)
        cursor = connection.cursor()
        bytes = pwd.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        cursor.execute(
            "INSERT INTO user_data (username,password) VALUES (?,?)", (user, hash)
        )
        connection.commit()
        connection.close()
        return True
    except sql.IntegrityError:
        return False


# TEST CODE FOR THE INPUT SYSTEM - NO HASHING NO INPUT VALIDATION WE DIE LIKE
# usertest = input("no ")
# passtest = input("yes ")

# cursor.execute(f"INSERT INTO user_data (username, password) VALUES ('{usertest}','{passtest}')")

# cursor.execute("SELECT * FROM user_data")
# SensitiveInformation = cursor.fetchall()
# print(SensitiveInformation)

# if username and password combination brings results from sql database, log user in
# if not, say incorrect username or password

# youtube tutorials
# https://www.youtube.com/watch?v=biU3SvIctWI - html form output to python variable
# https://www.youtube.com/watch?v=lK-P5kOiQ6Y - how to use sql in python
