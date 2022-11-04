from work_with_data_users.in_json import InJsonDict
import os


class Admin(InJsonDict):
    """большинство админских вещей будет именно здесь"""

    def __init__(self, file_admins: str):
        """считываем файл имён админов и их id
            args:
                file_admins - путь до файла, где записаны админы и их id
        """
        super().__init__(file_admins)
        self.admins_telegram_id = super().reed_json()

    def check_id(self, telegram_id):
        """проверяет есть ли telegram_id в базе данных (проверят, этот id принадлежит ли какому-нибудь админу"""
        return str(telegram_id) in self.admins_telegram_id

    def __setitem__(self, telegram_id, name_admin):
        """добавить нового админа или изменить имя админа по id | exz[telegram_id] = name_admin
        (по ключу добавить новое значение)
        """
        if isinstance(telegram_id, int):
            telegram_id = str(telegram_id)
        if not isinstance(telegram_id, str):
            raise ValueError('The telegram_id must be type int or str')
        if not isinstance(name_admin, str):
            raise ValueError('The nama_admin must be type str')
        self.admins_telegram_id[telegram_id] = name_admin

    def __getitem__(self, telegram_id):
        """получить по ключу (telegram_id) значение (name_admin | имя админа)"""
        if isinstance(telegram_id, int):
            telegram_id = str(telegram_id)
        if not isinstance(telegram_id, str):
            raise ValueError('The telegram_id must be type str or int')
        return self.admins_telegram_id[telegram_id]

    def write_admins_telegram_id(self):
        """перезаписывает все данные в json файл, который был узказан при инициализцаии экземпляра file_admins"""
        super().write_dict(self.admins_telegram_id)

    def __str__(self):
        return str(self.admins_telegram_id)

    def delete_admin(self, telegram_id):
        """удаляет админа по telegram_id"""
        del self.admins_telegram_id[str(telegram_id)]


if __name__ == '__main__':
    os.chdir('../')
    # a = Admin('admin/admins_telegram_id.json')
    m = Admin('admin/admins_telegram_id.json')
    m['678906789'] = 'Lolik'
    print(m)
    m.delete_admin(678906789)
    print(m)
    m.write_admins_telegram_id()
    # m.update_admins_telegram_id()

    # print(m[432344])
