import mysql.connector
from data import UserNotExists, DatabaseError
from difflib import get_close_matches
from helper import normalize_list
import datetime
from traceback import print_exc
from passwords import MySql

database = mysql.connector.connect(
  host="localhost",
  user="",
  passwd="",
  auth_plugin='mysql_native_password',
  port="3306",
  database="",
  autocommit=True
)
cursor = database.cursor(buffered=True)

def XPupdate(user, value, cursor=cursor, database=database):
    cursor.execute("SELECT Nome FROM xptable") #checks if user exists
    allusers = normalize_list(cursor.fetchall())
    match = get_close_matches(user, allusers, n=1, cutoff=0.5)
    if len(match) == 0: # if user do not exist create it and add X XPs
        raise UserNotExists(user + " is not a valid user")

    else: #adds or removes X xps from an user
        cursor.execute("SELECT xpvalue FROM xptable WHERE Nome=\'" + match[0] + "'")
        CurrentXP = [int(i[0]) for i in cursor.fetchall()][0]
        TotalXP = CurrentXP + int(value)
        cursor.execute("UPDATE xptable SET xpvalue = " + str(TotalXP) + " WHERE Nome='" + match[0] + "'")
    return [str(TotalXP), match[0]]

def XPdump(user, cursor=cursor,  database=database):
    cursor.execute("SELECT Nome FROM xptable") #checks if user exists
    allusers = normalize_list(cursor.fetchall())
    match = get_close_matches(user, allusers, n=1, cutoff=0.5)
    if enumerate(match) == 0: # if user do exist, if not creates it
        #cursor.execute("INSERT INTO xptable (Nome, xpvalue) VALUES (\"" + user + "\", 0)")
        raise UserNotExists(user + " is not a valid user")
    else: #dump function
        cursor.execute("SELECT xpvalue FROM xptable WHERE Nome=\'" + match[0] + "'")
        output = [int(i[0]) for i in cursor.fetchall()][0]
        return [str(output), match[0]]

def AddHomework(date, subject, content, cursor=cursor,  database=database):
    try:
        cursor.execute("INSERT INTO homeworks (date, subject, content) VALUES (\'" + str(date) + "\', \'" + str(subject) + "\', \'" + str(content) + "\')")
    except:
        raise DatabaseError
        print_exc()
def DumpHomewok(date: str, cursor=cursor,  database=database):
    try:
        cursor.execute("SELECT subject, content FROM homeworks WHERE date=\'" + date + "\'")
        return cursor.fetchall()
    except:
        raise DatabaseError
        print_exc()

def GetList(cursor=cursor,  database=database):
    cursor.execute("SELECT Nome FROM xptable") #checks if user exists
    return normalize_list(cursor.fetchall())

def scoreboard(cursor=cursor, database=database):
    cursor.execute("SELECT Nome, xpvalue FROM xptable WHERE xpvalue <>0 ORDER BY xpvalue DESC")
    return cursor.fetchall()

if __name__ == "__main__":
    try:
        while True:
            uname = input("Choose user: ")
            xps = input("How many XPs: ")
            XPupdate(uname, xps)
            dump = input("Dump User: ")
            print(XPdump(dump))
    except KeyboardInterrupt:
        quit()
    finally:
        cursor.close()
