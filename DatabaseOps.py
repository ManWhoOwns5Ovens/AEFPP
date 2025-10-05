import sqlalchemy as db
import sqlalchemy.orm as orm
from datetime import datetime
import os

base = orm.declarative_base() # keep track of my ORM classes, File & Document
class File(base):
    __tablename__ = "File"
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Path = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    Size = db.Column(db.Integer)
    CreatDat = db.Column(db.DateTime)
    MD5 = db.Column(db.String(32))
    SHA256 = db.Column(db.String(64))
    Status = db.Column(db.String(255))

    documents = orm.relationship("Document", back_populates="file")

class Document(base):
    __tablename__ = "Document"
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FileId = db.Column(db.Integer, db.ForeignKey("File.Id"))
    RawTxt = db.Column(db.Text)
    NormalTxt = db.Column(db.Text)
    CharCount = db.Column(db.Integer)
    WordCount = db.Column(db.Integer)
    UniqueCount = db.Column(db.Integer)

    file = orm.relationship("File", back_populates="documents")

def createSession():
    engine=db.create_engine('sqlite:///aefpp.db') #connection factory to my db - pool of connections
    base.metadata.create_all(engine)
    localSession=orm.sessionmaker(bind=engine)# stores interactions with the db
    return localSession()

def saveData(file,document):
    if checkForHash(file):
        session=createSession()
        newFile = File(
            Path=file.getPath(),
            Name=file.getName(),
            Size=file.getSize(),
            CreatDat=datetime.fromtimestamp(file.getCreationDate()),
            MD5=file.getMD5(),
            SHA256=file.getSHA256(),
            Status=file.getStatus()
        )
        session.add(newFile)# push changes to db but doesnt commit yet - creates IDs lets me use them as FKs

        newDoc = Document(
            FileId=newFile.Id,
            RawTxt=document.getRawContent(),
            NormalTxt=document.getNormalisedContent(),
            CharCount=document.getCharCount(),
            WordCount=document.getWordCount(),
            UniqueCount=document.getUnique()
        )
        session.add(newDoc)
        session.commit() # finalise transaction to db, query interactions from session, without commit nothing is saved
        session.close()

def checkForHash(file):
    session=createSession()

    query=db.select(File).where(File.MD5== file.getMD5())
    result=session.execute(query).scalars().all()

    if result!=[]:
        query=db.select(File).where(File.SHA256== file.getSHA256())
        result=session.execute(query).scalars().all()
    session.close()
    return result==[]

def searchKeyTerm(keyTerm):
    session=createSession()
    searchTerm='%'+keyTerm+'%'

    query=(db.select(File.Path)
           .where(Document.NormalTxt.like(searchTerm))
           .where(Document.Id==File.Id)
           )
        
    result=session.execute(query).scalars().all()
    try:
        for path in result:
            os.startfile('.\\'+str(path))
    except:
        print('Cannot find file.')

    print(result)

