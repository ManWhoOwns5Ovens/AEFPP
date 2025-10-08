import os, pathlib, re, magic, collections
import hashlib

import ExtractText
from Data import FileData, DocumentData
import DatabaseOps

def fileIngestion(filePath):
    kind=magic.from_file(filePath, mime=True)
    if kind=='application/pdf' or kind=='text/plain' or kind=='application/zip':
        tempName=os.path.basename(filePath).split('/')[-1]
        tempSize=os.path.getsize(filePath)
        tempCDate=os.path.getctime(filePath)

        return FileData(filePath,tempName,tempSize,tempCDate)
            
def textExtraction(file,filePath): # turning files into raw searchable text
    if os.access(filePath, os.R_OK):
        kind=magic.from_file(filePath, mime=True)
        content=''
        match kind:
            case 'application/pdf':
                try:
                    content=ExtractText.extractPDF(filePath)
                except Exception as ex:
                    file.setStatus('error')
                    print('Failed to parse '+ file.getName()+' at '+filePath)
            case 'application/zip':
                try:
                    content=ExtractText.extractDocx(filePath)
                except Exception as ex:
                    file.setStatus('error')
                    print('Failed to parse '+ file.getName()+' at '+filePath)
            case 'text/plain':
                try:
                    content=ExtractText.extractTxt(filePath)
                except Exception as ex:
                    file.setStatus('error')
                    print('Failed to parse '+ file.getName()+' at '+filePath)

        document=DocumentData()            
        document.setRawContent(content)
        content=normaliseString(content)
        document.setNormalContent(content)

    if len(content.strip()) == 0:
        file.setStatus('empty')
        raise Exception('Empty')
    else:
        file.setStatus("text_extracted")

    return (file,document)

#normalises extracted text so it can be stored within the same format
def normaliseString(inputString):    
    inputString=inputString.strip() # remove whitespaces

    mapping =  dict.fromkeys(range(32), None)
    inputString = inputString.translate(mapping) #remove control characters

    inputString=inputString.lower()

    return inputString

def metadataConstruction(file,document):
    if file.getStatus() != 'empty':
        content=document.getNormalisedContent()

        document.setCharCount(len(content))
        words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ'-]+", content)

        document.setWordCount(len(words))
        document.setUniqueWordCount(len(set(words)))

        print(collections.Counter(words))
        document.setWordFreq(collections.Counter(words)) #{word : frequency}

        rawContent=document.getRawContent()
        file.setMD5Hash(hashlib.md5(rawContent.encode()).hexdigest())# use hex to get a readable hex string instead of raw bytes
        file.setSHA256Hash(hashlib.sha256(rawContent.encode()).hexdigest())

        file.setStatus("metadata_complete")
    return (file,document)

def addFilesToDB(filePath):
    #inputFiles={} # dictionary {file data : document data}
    file=fileIngestion(filePath)
    file,document=textExtraction(file,filePath)
    file,document=metadataConstruction(file,document)
    DatabaseOps.saveData(file,document)

