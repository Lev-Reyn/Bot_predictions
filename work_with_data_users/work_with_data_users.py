import os
from work_with_data_users.in_json import InJson
from random import choice
import csv


class WorkWithDataUsers(InJson):
    def __init__(self, telegram_id: str):
        self.telegram_id = telegram_id
        super().__init__(f'data_users/{self.telegram_id}user.json')

    def get_all_users(self):
        """получить все telegram_id юзеров"""
        users_json = os.listdir('data_users')  # названия файлов юзеров
        users_telegram_id = []
        for user in users_json:
            users_telegram_id.append(user.replace('user.json', ''))
        return users_telegram_id

    def add_prediction_in_user_file(self, prediction):
        """добавляет отправленное предсказание в файл юзера и возвращает обратно это же предсказание"""
        super().update_list([prediction])
        return prediction

    def get_prediction(self):
        """получить предсказание для этого пользователя (для каждого то, которого ещё человек не получал),
        ну и вызывает метод add_prediction_in_user_file"""
        super().__init__('data_predictions/predictions.json')
        predictions = super().reed_json()
        predictions: list
        super().__init__(f'data_users/{self.telegram_id}user.json')
        user_old_predictions = super().reed_json()
        for need_del in user_old_predictions:
            predictions.remove(need_del)
        if len(predictions) == 0:
            return 'на сегодня пиздец, нет у меня для тебя предсказания :('
        return self.add_prediction_in_user_file(choice(predictions))

    def get_info_about_users(self) -> list:
        """метод собирает информацию о пользователях бота, пока что просто их id и сколько они получили сообщений"""
        data_info_about_user_lst = []  # словарь, в котором ключи - это telegram_id, а значения - кол-во предсказаний
        data_info_about_users = os.listdir('data_users')
        for user in data_info_about_users:
            super().__init__(f'data_users/{user}')
            user_old_predictions = len(super().reed_json())  # количество отправленных предсказаний этому пользователю
            data_info_about_user_lst.append({
                'telegram_id': user[:-9],
                'count_predictions': user_old_predictions})
        return data_info_about_user_lst

    def create_csv_info_about_users(self, data_info_about_user_lst=None):
        """cоздаёт csv файл по списку словарей, если ничего не передали в метод, то собирает инфу о юзерах из
         get_info_about_users"""
        if not data_info_about_user_lst:
            data_info_about_user_lst = self.get_info_about_users()
        with open('data_info_about_user.csv', 'w') as csvfile:
            fieldnames = [str(key) for key in data_info_about_user_lst[0]]
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for user in data_info_about_user_lst:
                writer.writerow(user)



if __name__ == '__main__':
    os.chdir('../')  # поставить основную директорию другую (в данном случа я поставил bot_predictions
    # в качестве основной)
    dima = WorkWithDataUsers('664295561')
    print(dima.get_prediction())
