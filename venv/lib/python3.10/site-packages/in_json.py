import json
import os.path


class InJson:
    def __init__(self, name_file: str):
        """name_file - название файла, проверяет, если такого файла нет, то создаёт"""
        self.name_file = name_file
        if not os.path.exists(self.name_file):
            lst = []
            with open(self.name_file, 'w') as file:
                json.dump(lst, file, indent=4, ensure_ascii=False)

    def update_list(self, lst: list):
        """добавляет сожержимое lst в содержимое json файлика (а внутри него список должен быть)"""
        with open(self.name_file, 'r') as file:
            self.lst_past = json.load(file)
        self.lst_past += lst
        with open(self.name_file, 'w') as file:
            json.dump(self.lst_past, file, indent=4, ensure_ascii=False)

    def reed_json(self):
        """считывает данные из файлика
        можно в принципе посмотреть что в файлике через атрибут lst_paste,
        но если хотим обновить данные, то используем метод"""
        with open(self.name_file, 'r') as file:
            self.lst_paste = json.load(file)
        return self.lst_paste

    def update_number_page(self, number_page: int):
        with open('number_page.txt', 'w') as file:
            file.write(str(number_page))


if __name__ == '__main__':
    lol = InJson('suka.json')
    lol.update_number_page(6)
