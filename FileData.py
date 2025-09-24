class FileData:

    def __init__(self, path, name, size, date):
        self._path=path
        self._name=name
        self._size=size #stored in bytes
        self._creationDate=date

        self._rawContent=""
        self._normalisedContent=""
        self._charCount=0
        self._wordCount=0
        self._uniqueWordCount=0

    def getPath(self):
        return self._path
    def getNormalisedContent(self):
        return self._normalisedContent
    

    def setRawContent(self, newContent):
        self._rawContent=newContent
    def setNormalContent(self, newContent):
        self._normalisedContent=newContent
    def setWordCount(self, newWords):
        print(newWords)
        self._wordCount=newWords
    def setUniqueWordCount(self, newWords):
        print(newWords)
        self._uniqueWordCount=newWords
    