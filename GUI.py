import PyQt5.QtWidgets as gui
import sys,os
import DatabaseOps as dbo
import FileProcessing as fp



def addFile():
    try:
        filePath=gui.QFileDialog.getOpenFileName(
            window,
            'Select a file',
            '',
            'All Files (*);;Text Files (*.txt);;DOCX Files (*.docx);;PDF Files (*.pdf)'
        )
        if filePath:
            fp.addFilesToDB(filePath[0])
        loadFullDatabase()
    except:
        pass

def searchForFile():
    result=dbo.searchKeyTerm(searchBar.text())
    loadDatabase(result)

def loadFullDatabase():
    allData=dbo.findAll()
    loadDatabase(allData)

def loadDatabase(data):
    table.setRowCount(0)
    table.setRowCount(len(data))
    for row,(name,path,frequency) in enumerate(data):
        table.setItem(row,0,gui.QTableWidgetItem(name))
        table.setItem(row,1,gui.QTableWidgetItem(str(frequency)))

        button=gui.QPushButton('Open File')
        button.clicked.connect(lambda _, p=path: openFile(p))
        table.setCellWidget(row,2,button)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()

def openFile(p):
    os.startfile(p)


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
searchBar.textChanged.connect(searchForFile)

table=gui.QTableWidget()
table.setEditTriggers(gui.QTableWidget.NoEditTriggers)
table.setColumnCount(3)
table.setHorizontalHeaderLabels(["Name", "Frequency", ""])
loadFullDatabase()


layoutSearch.addWidget(table)
layoutFunc.addWidget(addFileButton)
layoutFunc.addWidget(searchBar)
layoutSearch.addLayout(layoutFunc)
layoutMain.addLayout(layoutSearch)
layoutMain.addLayout(layoutResults)

window.setLayout(layoutMain)
window.show()

sys.exit(app.exec_())




