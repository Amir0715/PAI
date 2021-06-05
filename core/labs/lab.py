from abc import ABC, abstractmethod
import os

class Lab(ABC):
    @abstractmethod
    def run(self):
        pass
    
    @abstractmethod
    def gen_report(self, path, title, number, student_name):
        with open(path, 'w', encoding='utf-8' ) as file:
            file.write(
f'''
# Лабораторная работа №{number}

## Тема: {title}

|**Студент:**|*{student_name}*|
|------------|--------------|
|**Группа:** |*Б18-514*     |
''')
    
    def get_files(self, input_path):
        filelist = []
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if(file.endswith((".png", ".jpg", ".jpeg", ".bmp"))):
                    filelist.append(os.path.join(root,file))

        print(filelist)
        return filelist

    def create_dirs(self, dirnames):
        for dir in dirnames:
            if os.path.isdir(dir):
                os.removedirs(dir)
            os.makedirs(dir)
