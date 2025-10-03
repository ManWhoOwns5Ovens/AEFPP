import sqlite3
import sqlalchemy as db


metadata=db.MetaData()

tabFiles=db.Table('Files', metadata,
                  db.Column('Id',db.Integer(), primary_key=True, autoincrement=True),
                  db.Column('Path',db.String(255)),
                  db.Column('Name',db.String(255)),
                  db.Column('Size',db.Integer()),
                  db.Column('CreatDat',db.DateTime()),
                  db.Column('MD5',db.String(32)),
                  db.Column('SHA256',db.String(64)),
                  db.Column('Status',db.String(255))
)

tabDoc=db.Table('Documents', metadata,
                db.Column('Id',db.Integer(),primary_key=True,autoincrement=True),
                db.Column('FileId',db.Integer(),db.ForeignKey('Files.Id')),
                db.Column('RawTxt', db.Text()),
                db.Column('NormalTxt', db.Text()),
                db.Column('CharCount', db.Integer()),
                db.Column('WordCount', db.Integer()),
                db.Column('UniqueCount', db.Integer())
)

engine=db.create_engine('sqlite:///aefpp.db')
conn=engine.connect()
metadata.create_all(engine)

def saveData(file,document):
    pass


