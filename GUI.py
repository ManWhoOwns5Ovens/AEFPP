import PyQt5.QtWidgets as gui
import sys,os
import DatabaseOps as dbo
import FileProcessing as fp

def searchForFile():
    result=dbo.searchKeyTerm(searchBar.text())
    labelSearchResult.setText(str(result))
    layoutSearch.addWidget(labelSearchResult)

def addFile():
    filePath=gui.QFileDialog.getOpenFileName(
        window,
        'Select a file (txt,docx,pdf)',
        '',
        'All Files (*);;Text Files (*.txt);;DOCX Files (*.docx);;PDF Files (*.pdf)'
    )
    if filePath:
        fp.addFilesToDB(filePath[0])


app=gui.QApplication(sys.argv)
window=gui.QWidget()
window.setWindowTitle('Agile e-Discovery File Processing Pipeline')

layoutMain=gui.QHBoxLayout()
layoutFunc=gui.QHBoxLayout()
layoutResults=gui.QVBoxLayout()
layoutSearch=gui.QVBoxLayout()

addFileButton=gui.QPushButton('Add File')
addFileButton.clicked.connect(addFile)

searchBar=gui.QLineEdit()
searchBar.setPlaceholderText('Search File...')
labelSearchResult=gui.QLabel('')
searchBar.textChanged.connect(searchForFile)

table=gui.QTableWidget()
table.setColumnCount(3)
table.setHorizontalHeaderLabels(["Name", "Frequency of Word", ""])
layoutSearch.addWidget(table)
allData=dbo.findAll()
for row,(name,frequency,path) in enumerate(allData):
    table.setItem(row,0,gui.QTableWidgetItem(name))
    table.setItem(row, 1, gui.QTableWidgetItem(frequency))

    button=gui.QPushButton('Open File')
    def openFile(p):
        os.startfile(p)
    button.clicked.connect(lambda _, p=path: openFile(p))


layoutFunc.addWidget(addFileButton)
layoutFunc.addWidget(searchBar)
layoutSearch.addLayout(layoutFunc)
layoutMain.addLayout(layoutSearch)
layoutMain.addLayout(layoutResults)

window.setLayout(layoutMain)
window.show()

sys.exit(app.exec_())




