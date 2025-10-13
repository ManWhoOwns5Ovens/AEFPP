import PyQt5.QtWidgets as gui
from PyQt5.QtCore import Qt as qt
import sys,os
import DatabaseOps as dbo
import FileProcessing as fp

def main():

    def addFile():
        try:
            filePath=gui.QFileDialog.getOpenFileName(
                window,
                'Select a file',
                '',
                'All Files (*);;Text Files (*.txt);;DOCX Files (*.docx);;PDF Files (*.pdf)'
            )
            fp.addFilesToDB(filePath[0])
            loadFullDatabase()
            errorLabel.hide()
        except:
            errorLabel.setText('Could not add a file.')
            errorLabel.show()

    def searchForFile():
        result=dbo.searchKeyTerm(searchBar.text())
        
        if len(result)==0:
            errorLabel.setText('Could not find keywords in the database.')
            errorLabel.show()
            loadFullDatabase()
        else:
            errorLabel.hide()
            loadDatabase(result)

    def loadFullDatabase():
        allData=dbo.findAll()
        loadDatabase(allData)

    def loadDatabase(data):
        table.setRowCount(0)
        table.setRowCount(len(data))
        for row,(name,path,frequency,id) in enumerate(data):
            temp=gui.QTableWidgetItem(name)
            temp.setData(qt.UserRole, id)
            table.setItem(row,0,temp)
            # hide id data for searches

            table.setItem(row,1,gui.QTableWidgetItem(str(frequency)))

            button=gui.QPushButton('Open File')
            button.clicked.connect(lambda _, p=path: openFile(p))
            table.setCellWidget(row,2,button)

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def openFile(p):
        os.startfile(p)

    def formatTextToDisplay(content,length):
        MAX_CHAR=900
        textToDisplay=content[0:MAX_CHAR]
        if length>MAX_CHAR:
            textToDisplay+='....'
        return textToDisplay

    def formatSize(size):
        units=['bytes','KB','MB','GB']
        count=0
        for unit in units:
            temp=size//1024
            if temp>0:
                size=temp
                count+=1
            else:
                break
        return str(size)+' '+units[count]

    def rowSelected(row,col):
        item=table.item(row,0).data(qt.UserRole)
        data=dbo.getDocData(item)
        data=data[0]   

        contentLabel.setText(formatTextToDisplay(data[0],data[3]))
        sizeLabel.setText('Size: '+formatSize(data[1]))
        dateLabel.setText('Creation Date: '+data[2].strftime('%d/%m/%Y'))
        charCountLabel.setText('Character Count: '+str(data[3]))
        wordCountLabel.setText('Word Count: '+str(data[4]))

    def setupResultsPanel():
        contentLabel=gui.QLabel()
        sizeLabel=gui.QLabel()
        dateLabel=gui.QLabel()
        charCountLabel=gui.QLabel()
        wordCountLabel=gui.QLabel()

        layoutResults.setSpacing(5)
        layoutResults.addWidget(contentLabel)
        layoutResults.addStretch()
        layoutResults.addWidget(sizeLabel)
        layoutResults.addWidget(dateLabel)
        layoutResults.addWidget(charCountLabel)
        layoutResults.addWidget(wordCountLabel)

        return (contentLabel,sizeLabel,dateLabel,charCountLabel,wordCountLabel)

    def setupSearch():
        searchBar=gui.QLineEdit()
        searchBar.setPlaceholderText('Search File...')
        searchBar.setMinimumSize(200,20)
        searchBar.textChanged.connect(searchForFile)
        errorLabel=gui.QLabel()
        errorLabel.setStyleSheet("color: red;")
        errorLabel.hide()

        return (searchBar,errorLabel)

    def showContextMenu(pos):
        index=table.indexAt(pos)
        row=index.row()
        print('Row: '+ str(row))
        menu=gui.QMenu()
        deleteAction=gui.QAction('Delete Entry', table)
        deleteAction.triggered.connect(lambda: deleteFile(row))

        menu.addAction(deleteAction)
        menu.exec_(table.viewport().mapToGlobal(pos))

    def deleteFile(row):
        item=table.item(row,0).data(qt.UserRole)
        dbo.dropEntry(item)
        loadFullDatabase()

    app=gui.QApplication(sys.argv)
    window=gui.QWidget()
    window.setWindowTitle('Agile e-Discovery File Processing Pipeline')

    layoutMain=gui.QHBoxLayout()
    layoutResults=gui.QVBoxLayout()
    layoutSearch=gui.QVBoxLayout()
    layoutInteractions=gui.QHBoxLayout()

    addFileButton=gui.QPushButton('Add File')
    addFileButton.clicked.connect(addFile)

    searchBar,errorLabel=setupSearch()

    table=gui.QTableWidget()
    table.setEditTriggers(gui.QTableWidget.NoEditTriggers)
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Name", "Frequency", ""])
    table.cellClicked.connect(rowSelected)

    table.setContextMenuPolicy(qt.CustomContextMenu)
    table.customContextMenuRequested.connect(lambda pos: showContextMenu(pos))

    loadFullDatabase()


    contentLabel,sizeLabel,dateLabel,charCountLabel,wordCountLabel=setupResultsPanel()

    layoutInteractions.addWidget(addFileButton)
    layoutInteractions.addWidget(searchBar)
    layoutSearch.addWidget(table)
    layoutSearch.addLayout(layoutInteractions)
    layoutSearch.addWidget(errorLabel)
    layoutMain.addLayout(layoutSearch)
    layoutMain.addLayout(layoutResults)

    window.setLayout(layoutMain)
    window.show()
    sys.exit(app.exec_())




