import sqlite3

def runSqlCommand(command):
    cursor.execute(command)
    conn.commit()

def closeConnection():
    conn.close()

def createTables():
    runSqlCommand('CREATE TABLE FILES (' \
    'ID int NOT NULL AUTO_INCREMENT' \
    'PRIMARY KEY(ID)'\
    'PATH string'
    'NAME string'
    'SIZE int'
    'CREATED_AT DATETIME' 
    ');')

conn=sqlite3.connect('aefpp.db')
cursor = conn.cursor()



