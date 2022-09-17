import pytesseract

image_path = 'test88.png'
image_to_text = pytesseract.image_to_string(image_path,config='--psm 11')
print(image_to_text)