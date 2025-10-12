class FileData:
    def __init__(self, path, name, size, date):
        self._path=path
        self._name=name
        self._size=size #stored in bytes
        self._creationDate=date
        self._md5=None
        self._sha256=None
        self._status="ingested"

    def getPath(self):
        return self._path
    def getName(self):
        return self._name
    def getSize(self):
        return self._size
    def getCreationDate(self):
        return self._creationDate
    def getMD5(self):
        return self._md5
    def getSHA256(self):
        return self._sha256
    def getStatus(self):
        return self._status

    def setStatus(self, status):
        self._status=status
    def setMD5Hash(self,hash):
        self._md5=hash
    def setSHA256Hash(self,hash):
        self._sha256=hash
    
class DocumentData:
    def __init__(self):
        self._rawContent=""
        self._normalisedContent=""
        self._charCount=0
        self._wordCount=0
        self._uniqueWordCount=0

        self._wordFreq=None

    def getNormalisedContent(self):
        return self._normalisedContent
    def getRawContent(self):
        return self._rawContent
    def getCharCount(self):
        return self._charCount
    def getWordCount(self):
        return self._wordCount
    def getUnique(self):
        return self._uniqueWordCount
    def getWordFreq(self):
        return self._wordFreq
    
    def setRawContent(self, content):
        self._rawContent=content
    def setNormalContent(self, content):
        self._normalisedContent=content
    def setCharCount(self, count):
        self._charCount=count
    def setWordCount(self, words):
        self._wordCount=words
    def setUniqueWordCount(self, words):
        self._uniqueWordCount=words
    def setWordFreq(self, wordFreq):
        self._wordFreq=wordFreq



    