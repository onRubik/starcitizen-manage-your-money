# from typing import List
import cv2
import pytesseract
# import requests
from step import stepKey
from subprocess import run
import json
import os


class miningDb:
    def rewriteImage(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\excel\AppData\Local\Tesseract-OCR\tesseract.exe'
        img = cv2.imread('test5.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = pytesseract.image_to_string(img, lang='eng', config='--psm 11')
        print(data)


    def uexcorpReviewMinerals(self):
        store_key = stepKey()
        url = 'curl https://portal.uexcorp.space/api/all_prices -H "api_key: ' + str(store_key)
        output = str(run(url, shell=True, capture_output=True).stdout)

        if not output:
            print('curl command failed, minerals.json not updated')
        elif output:
            if os.path.exists('minerals.json'):
                print('updating minerals.json')
                os.remove('minerals.json')
                self.cleanMineralsFile(output)
            elif not os.path.exists('minerals.json'):
                print('creating new minerals.json')
                self.cleanMineralsFile(output)


    def cleanMineralsFile(self, output):
        with open('minerals.json', 'w') as f:
            json.dump(output, f)

        f = open('minerals.json')
        s = f.read().replace("\\", '')
        f.close()
        f = open('minerals.json', 'w')
        f.write(s)
        f.close()

        trim_file = open('minerals.json', 'r')
        data = trim_file.read()
        trim_file.close()
        data = data[3:-2]
        trim_f = open('minerals.json', 'w')
        trim_f.write(data)
        trim_f.close()


if __name__ == '__main__':
    testMiningDb = miningDb()
    # testMiningDb.rewriteImage()
    testMiningDb.uexcorpReviewMinerals()

# rewriteImage()