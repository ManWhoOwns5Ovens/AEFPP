import os, pathlib, re, collections
import chardet

import PyPDF2, docx_parser as docxParser, filetype
import hashlib

import FileData

inputFiles=[]
def fileIngestion():
    inputPath=pathlib.Path("./input")
    
    if inputPath.exists():
        for file in os.listdir(inputPath):
            tempPath=os.path.join(inputPath, file)
            kind=filetype.guess(tempPath)
            if kind.extension=="txt" or kind.extension=="pdf" or kind.extension=="docx":
                tempName=file
                tempSize=os.path.getsize(tempPath)
                tempCDate=os.path.getctime(tempPath)

                newFile = FileData.FileData(tempPath,tempName,tempSize,tempCDate)
                inputFiles.append(newFile)


def textExtraction(): # turning files into raw searchable text
    for file in inputFiles:
        filePath= file.getPath()
        if os.access(filePath, os.R_OK):
            fileType=filetype.guess(filePath)
            content=""

            match fileType.extension:
                case "txt":
                    with open(filePath, 'rb') as file: #open file in binary to detect encoding
                        content = file.read()
                        txtEncoding= chardet.detect(content)['encoding']
                    with open(filePath, "r", encoding=txtEncoding, errors="replace") as file: #open file with the right encoding
                        content = file.read()

                case "pdf":
                    reader=PyPDF2.PdfReader(filePath)
                    for page in reader.pages:
                        text=page.extract_text()
                        if text and text.strip(): #if page has a text layer
                            content+=text

                case "docx":
                    doc= docxParser.DocumentParser(filePath)
                    for _type, paragraph in doc.parse():
                        content+=paragraph

            file.setRawContent(content)
            content=normaliseString(content,file)
            file.setNormalContent(content)
        else:
            pass

def normaliseString(inputString,file):    
    inputString=inputString.strip() # remove whitespaces

    mapping =  dict.fromkeys(range(32), None)
    inputString = inputString.translate(mapping) #remove control characters

    inputString=inputString.lower()

    return inputString

def metadataEnrichment():
    for file in inputFiles:
        content=file.getNormalisedContent()

        file.setCharCount(len(content))
        words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ'-]+", content)
        file.setWordCount(len(words))

        file.setUniqueWordCount(len(set(words)))

        wordFreq=collections.Counter(words) #{word : frequency}


fileIngestion()
textExtraction()
metadataEnrichment()