import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def runSqlCommand(command):
    pass

def closeConnection():
    pass

def createTables():
    runSqlCommand("""
    CREATE TABLE FILES (
        ID INT NOT NULL AUTO_INCREMENT,
        PATH VARCHAR(255),
        NAME VARCHAR(255),
        SIZE INT,
        CREATED_AT TIMESTAMP,
        MD5_HASH VARCHAR(32),
        SHA256_HASH VARCHAR(64),
        STATUS VARCHAR(50),
        PRIMARY KEY (ID)
    );
    """)

    runSqlCommand("""
    CREATE TABLE DOCUMENTS(
        ID INT NOT NULL AUTO_INCREMENT,
        FILE_ID INT NOT NULL AUTO_INCREMENT,
        RAW_TEXT MEDIUMTEXT
        NORMAL_TEXT MEDIUMTEXT
        CHAR_COUNT INT
        WORD_COUNT INT
        UNIQUE_WORD_COUNT INT
        KEYWORDS VARCHAR(255)
        PRIMARY KEY(ID)
        FOREIGN KEY(FILE_ID) REFERENCES FILES(ID)
    );
    """)

engine= create_engine('sqlite:///aefpp.db')



