import cv2
import pytesseract

# step file allocates the API key. Suggested file template to store the key (substitute <your_api_key> with the correct string):
# notice: be sure to override the github traking for the file 'step' using .gitignore (it is already included in this project). Saving the API key as a environment variable is also recommended.
# # def stepKey():
# #     apiKey = '<your_api_key>'
# #     return apiKey
from step import stepKey

from subprocess import run
import json
import os
from typing import List
import uuid
import platform
import datetime


class miningDb:
    def __init__(self, file_type: List[str], players: List[str]):
        self.file_type = file_type
        self.players = players


    # notice: os.path.dirname(__file__) is intended to be used for a windows OS
    def img_folder(self):
        os_type = platform.system()
        file_path = []
        if os_type == 'Windows':
            script_dir = os.path.dirname(__file__)
            input_path = script_dir + '\\img\\'
        elif os_type == 'Linux':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            input_path = script_dir + '/img/'
        for path, dirs, files in os.walk(input_path):
            for filename in files:
                if filename.split('.')[-1] in self.file_type:
                    file_path.append(os.path.join(path, filename))

        return file_path, os_type

    
    def rewriteImage(self):
        read_data = ''
        read_file = self.img_folder()[0]
        os_type = self.img_folder()[1]
        # for windows:
        # substitute <user_name> with the correct user folder
        if os_type == 'Windows':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Users\<user_name>\AppData\Local\Tesseract-OCR\tesseract.exe'

        for x in read_file:
            img = cv2.imread(x)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            data = pytesseract.image_to_string(img, lang='eng', config='--psm 11')
            read_data = read_data + data

        split_list = read_data.splitlines()
        return split_list


    def cleanInput(self):
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        raw_list = self.rewriteImage()
        list_str = []
        list_int = []
        clean_list = []
        for i, x in enumerate(raw_list):
            if not x:
                continue
            elif x[0] not in numbers:
                list_str.append(x)
            elif x[0] in numbers:
                list_int.append(int(x))

        list_str_len = len(list_str)
        list_int_len = len(list_int)
        if list_str_len != list_int_len:
            print('warning! unmatch between minerals and quantity')

        max_len = max(list_str_len, list_int_len)
        if list_str_len < max_len:
            for i in range(max_len - list_str_len):
                list_str.append('null')
        if list_int_len < max_len:
            for i in range(max_len - list_int_len):
                list_int.append(0)

        for i in range(max_len):
            if list_str[i] and list_int[i]:
                inner_list = [list_str[i], list_int[i]]
            elif (not list_str[i]) and list_int[i]:
                inner_list = ['null', list_int[i]]
            elif list_str[i] and (not list_int[i]):
                inner_list = [list_str[i], 'null']

            clean_list.append(inner_list)

        return clean_list


    def addOrder(self):
        data = self.cleanInput()
        sell_amount = 0

        with open('db.json', 'r+') as json_db:
            json_data = json.load(json_db)
            unique_id = uuid.uuid4()
            with open('minerals.json') as json_minerals:
                minerals_data = json.load(json_minerals)
                for x in data:
                    refined_material = x[0].replace(' (RAW)', '')
                    refined_material = refined_material.replace(' (ORE)', '')
                    if minerals_data.get(refined_material) != None:
                        price = minerals_data.get(refined_material)
                        if x[1] != 'null':
                            product = x[1] * price
                        elif x[1] == 'null':
                            product = 0 * price
                    elif minerals_data.get(refined_material) == None:
                        price = 0
                        if x[1] != 'null':
                            product = x[1] * price
                        elif x[1] == 'null':
                            product = 0 * price
                    sell_amount = sell_amount + product

            ct = datetime.datetime.now()
            unique_id = str(unique_id)
            append_data = {unique_id: {"date": str(ct), "players": self.players, "order": data, "sell_amount": sell_amount, "share_per_player": sell_amount/(len(self.players))}}
            json_data["orders"].update(append_data)
            json_db.seek(0)
            json.dump(json_data, json_db, indent = 4)
            print('finished order update')


    def uexcorpReviewMinerals(self):
        store_key = stepKey()
        url = 'curl https://portal.uexcorp.space/api/commodities -H "api_key: ' + str(store_key)
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
            f.close()

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

        keep_keys = ['data', 'name', 'trade_price_sell']
        with open('minerals.json') as f_del:
            d = json.loads(f_del.read())
            new_data = {k: v for k, v in d.items() if k == 'data'}
            new_dict = {}
            for x in new_data['data']:
                x = {k: v for k, v in x.items() if k in keep_keys}
                get_key = x.get('name')
                upper_key = get_key.upper()
                new_dict[upper_key] = x.get('trade_price_sell')
            
        with open('minerals.json', 'w') as out_f:
            json.dump(new_dict, out_f)
            f.close()
        