# Automated e-Discovery File Processing Pipeline (A-EFPP)
This is a lightweight document analysis and discovery system made for fun and to help search my university documents.

The current system validates and processes text-based files (.txt,.docx,.pdf), extracting searchable text and computing metadata for deduplication and integrity verification, it then stores processed files in an SQLite database.

## Prerequisites
Before running the project, ensure you have the following installed:
- Windows 10 or newer
- x64 architecture
- ~120MB disk space

## Running the Project
- Download the newest Release zip file
- Unzip the files
- Navigate to Release/dist
- Open main.exe

## Usage Instructions
- Click the 'Add File' button to add files (supported types: .txt, .docx, .pdf) - unsupported file types will be rejected
- Enter keywords in the searchbar. The app will alter the display of the files based on the frequency of the keywords in the added files to return the most relevant.
- Right-click and navigate to 'Delete File' to remove files from the table.
- Next to each file entry should exist an 'Open File' button that allows the access to the file in your system's default app.

## Known Issues and Progress Map
- Large File Size due to Pyinstaller
- The system does not drop file entries with invalid file paths

