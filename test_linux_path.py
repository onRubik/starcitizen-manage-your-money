import os
import platform


file_type = ['png', 'jpg', 'JPG', 'PNG']

def img_folder(file_type):
        # to review os type:
        print(os.name)
        print(platform.system())
        
        # The output of platform.system() is as follows:
        # Linux: Linux
        # Mac: Darwin
        # Windows: Windows
        
        file_path = []
        script_dir = os.path.dirname(__file__)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print('it went in')
        print(script_dir)
        # input_path = script_dir + '\\img\\'
        input_path = script_dir + '/img/'
        for path, dirs, files in os.walk(input_path):
            for filename in files:
                if filename.split('.')[-1] in file_type:
                    file_path.append(os.path.join(path, filename))

        return file_path


print(img_folder(file_type))