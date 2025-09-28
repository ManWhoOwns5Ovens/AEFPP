import chardet, PyPDF2, docx_parser as docxParser
def extractTxt(filePath):
    with open(filePath, 'rb') as file: #open file in binary to detect encoding
        content = file.read()
        txtEncoding= chardet.detect(content)['encoding']
    with open(filePath, "r", encoding=txtEncoding, errors="replace") as file: #open file with the right encoding
        content = file.read()
    return content

def extractDocx(filePath):
    parser= docxParser.DocumentParser(filePath)
    content=''
    for _type, paragraph in parser.parse():
        content+=paragraph['text']
    return content

def extractPDF(filePath):
    reader=PyPDF2.PdfReader(filePath)
    content=''
    for page in reader.pages:
        text=page.extract_text()
        if text and text.strip(): #if page has a text layer
            content+=text
    return content