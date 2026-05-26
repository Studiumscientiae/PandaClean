# 🐼  PANDACLEAN  🐼

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple)
![Pytest](https://img.shields.io/badge/Testing-Pytest-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

## PROJECT DESCRIPTION
- This project is a version 1 of a data cleaning tool built using python, pandas, openpyxl and tkinter.
- Tkinter is used for the GUI interface, Pandas for data processing, and Python for application logic.
- This version is built using procedural programming principles.

## FEATURES
- Support CSV and XLSX file processing.
- Help in dealing with duplicate values.
- Format and convert dataframe datatypes.

## APPLICATION PREVIEW
### Main Window
![PandaClean GUI](Application_preview/Main.png)
### Missing Value window
![PandaClean GUI](Application_preview/Missing.png)
### Formatting Window
![PandaClean GUI](Application_preview/Formatting.png)

## TECHNOLOGIES USED
- Python
- Tkinter
- OpenPyXL
- Pandas for data processing including data handling, data cleaning, data formatting and datatype conversions.

## REQUIREMENTS

- Python 3.10+
- Pandas
- OpenPyXL
- Tkinter
- Pytest

## PROJECT STRUCTURE
```text
PandaClean/
│
├── Application_preview/
│   ├── Formatting.png
│   ├── Main.png
│   └── Missing.png
│
├── cleaning/
│   ├── Datatype.py
│   ├── Duplicates.py
│   ├── Formatting.py
│   └── Missing.py
│
├── File_manager/
│   └── file_handler.py
│
├── gui/
│   ├── gui_datatype.py
│   ├── gui_duplicates.py
│   ├── gui_file_handler.py
│   ├── gui_formatting.py
│   ├── gui_missing.py
│   ├── main.py
│   ├── theme.py
│   └── tool_base.py
│
<<<<<<< HEAD
=======
├── tests/
│   ├── data/
│   │       └── sample_dataset.xlsx
│   ├── conftest.py
│   ├── test_datatype.py
│   ├── test_duplicates.py
│   ├── test_file_handler.py
│   ├── test_formatting.py     
│   └── test_missing.py
│       
>>>>>>> 96f0fa9 (Complete testing for data cleaning and file handling modules)
├── .gitignore
├── README.md
└── requirements.txt
```

## TESTING

This project uses Pytest for automated testing.

The test suite validates:
- Missing value handling
- Duplicate handling
- Datatype conversions
- Formatting operations
- File handling operations

Tests are organized module-wise inside the `tests/` directory.

### Run Tests

```bash
pytest
```

## INSTALLATION
- Install required packages
``` bash 
pip install -r requirements.txt
```

## HOW TO RUN 
- Run the following command 
```bash 
python gui/main.py
```

## FUTURE IMPROVEMENTS

- Add GUI improvements.
- Add visualization support.
- Add machine learning preprocessing.
- Support more file formats.
- Using OOPs replacing procedural programming.
- Refactor the project using Object-Oriented Programming (OOP).

## LICENSE
This project is licensed under the MIT License.

``` text 
MIT License

Copyright (c) 2026 PANDACLEAN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

