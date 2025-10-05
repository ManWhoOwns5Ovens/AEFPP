import os, pathlib, re, magic, collections
import hashlib

import ExtractText
from Data import FileData, DocumentData
import DatabaseOps

def fileIngestion(inputFiles):
    inputPath=pathlib.Path("./input")
    
    if inputPath.exists():
        for file in os.listdir(inputPath):
            tempPath=os.path.join(inputPath, file)
            kind=magic.from_file(tempPath, mime=True)
            if kind=='application/pdf' or kind=='text/plain' or kind=='application/zip':
                tempName=file
                tempSize=os.path.getsize(tempPath)
                tempCDate=os.path.getctime(tempPath)

                newFile = FileData(tempPath,tempName,tempSize,tempCDate)
                inputFiles[newFile]= DocumentData()
            
def textExtraction(inputFiles): # turning files into raw searchable text
    for file in inputFiles.keys():
        filePath= file.getPath()
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
                        continue
                case 'application/zip':
                    try:
                        content=ExtractText.extractDocx(filePath)
                    except Exception as ex:
                        file.setStatus('error')
                        print('Failed to parse '+ file.getName()+' at '+filePath)
                        continue
                case 'text/plain':
                    try:
                        content=ExtractText.extractTxt(filePath)
                    except Exception as ex:
                        file.setStatus('error')
                        print('Failed to parse '+ file.getName()+' at '+filePath)
                        continue

            document=inputFiles[file]                
            document.setRawContent(content)
            content=normaliseString(content)
            document.setNormalContent(content)

        if len(content.strip()) == 0:
            file.setStatus('empty')
        else:
            file.setStatus("text_extracted")

#normalises extracted text so it can be stored within the same format
def normaliseString(inputString):    
    inputString=inputString.strip() # remove whitespaces

    mapping =  dict.fromkeys(range(32), None)
    inputString = inputString.translate(mapping) #remove control characters

    inputString=inputString.lower()

    return inputString

def metadataConstruction(inputFiles):
    for file in inputFiles.keys():
        document=inputFiles[file]
        content=document.getNormalisedContent()

        document.setCharCount(len(content))
        words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ'-]+", content)
        document.setWordCount(len(words))

        document.setUniqueWordCount(len(set(words)))

        wordFreq=collections.Counter(words) #{word : frequency}

        rawContent=document.getRawContent()
        file.setMD5Hash(hashlib.md5(rawContent.encode()).hexdigest())# use hex to get a readable hex string over raw bytes
        file.setSHA256Hash(hashlib.sha256(rawContent.encode()).hexdigest())

        file.setStatus("metadata_complete")

def addFilesToDB():
    inputFiles={} # dictionary {file data : document data}
    fileIngestion(inputFiles)
    textExtraction(inputFiles)
    metadataConstruction(inputFiles)
    for file in inputFiles:
        DatabaseOps.saveData(file,inputFiles[file])

def main():
    addFilesToDB()  
    DatabaseOps.searchKeyTerm(normaliseString(input()))

if __name__=="__main__":
    main()