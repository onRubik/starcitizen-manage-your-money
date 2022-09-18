# Manage your money in star citizen
## Features
* take screenshots of renfining mining orders using tesseract-ocr
* convert images data into text using tesseract-ocr
* get prices for refined minerals using https://uexcorp.space/ API (review this page to get your API key)
* get the refined amount per order and share per players

# Python setup
Python version in use = 3.9.0

To list current requirement:
> pip freeze requirement.txt

To install packages in requirement.txt:
> pip install -r requirement.txt

Notice:
* tesseract-ocr needs to be installed in addition to requirement.txt
* for a Windows system is recommended to use a windows installer:
https://github.com/UB-Mannheim/tesseract/wiki
** for a Linux system it can be installed using apt:
> sudo apt install tesseract-ocr
* the current script version is is intended to work foremost in Windows 10

# Script usage
* save all images to add to an order in the img/ folder
* run model.py
* db.json will be updated with a new order each time model.py runs

# Further development
* when using the function pytesseract.image_to_string() for the current version, most likely it will ignore single digit inputs
* if this happens the quantities for each mineral will be shifted and needs to be updated manually
* to solve the previous issue, tuning for the images or using another solution rather than tesseract-ocr may be introduced
* input to read players names from an image also will be introduced
