import os
from work_with_data_users.in_json import InJson, InJsonDict
# from in_json import InJson, InJsonDict
from random import choice
from datetime import datetime
import csv


class WorkWithDataUsers(InJson, InJsonDict):
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

    def add_info_about_user_statistics(self, username=None, full_name=None, work_or_stop=None, count_touch_help=None,
                                       count_touch_next_prediction=None, count_touch_start=None):
        """тестовый метод, который собирает статистику о пользователях (создаём json файлик, в котором будет инфа)
         структура:
            словарь со словарями (во внутренем словаре ключи - это данные об этом пользователе, так же и id там будет
            тоже )
        """

        InJsonDict.__init__(self, 'statistics/data_about_users_statistics.json')

        data_statistics = InJsonDict.reed_json(self)
        data_statistics: dict
        if not data_statistics.get(str(self.telegram_id)):
            data_statistics[str(self.telegram_id)] = {
                'telegram_id': str(self.telegram_id),
                'username': '',
                'full_name': '',
                'work_or_stop': '',
                'last_use_bot': '',
                'all_uses': [],
                'count_touch_help': 0,
                'count_touch_next_prediction': 0,
                'count_touch_start': 0,
                'predictions': []
            }
        if username:
            data_statistics[str(self.telegram_id)]['username'] = username
        if full_name:
            data_statistics[str(self.telegram_id)]['full_name'] = full_name
        if work_or_stop:
            data_statistics[str(self.telegram_id)]['work_or_stop'] = work_or_stop
        if count_touch_help:
            data_statistics[str(self.telegram_id)]['count_touch_help'] += 1
        if count_touch_next_prediction:
            data_statistics[str(self.telegram_id)]['count_touch_next_prediction'] += 1
        if count_touch_start:
            data_statistics[str(self.telegram_id)]['count_touch_start'] += 1

        # всегда проверяем время, так как это время последнего использования бота
        data_statistics[str(self.telegram_id)]['last_use_bot'] = f'{datetime.now().date()}  ' \
                                                            f'{str(datetime.now().time()).split(".")[0]}'

        # все тайминги использования бота сохраняем в all_uses
        data_statistics[str(self.telegram_id)]['all_uses'].append(data_statistics[str(self.telegram_id)]['last_use_bot'])

        super().__init__(f'data_users/{self.telegram_id}user.json')
        user_old_predictions = super().reed_json()  # все предсказания, которые отправлены этому юзеру
        # print(user_old_predictions)
        # print(data_statistics)
        data_statistics[str(self.telegram_id)]['predictions'] = user_old_predictions
        # print(data_statistics)
        InJsonDict.__init__(self, 'statistics/data_about_users_statistics.json')  # не понимаю зачем это делать, ибо в
        # начале метода было сделано, но без этого выдаёт ошибку

        InJsonDict.update_dict(self, data_statistics)  # закидываем данные в json


if __name__ == '__main__':
    os.chdir('../')  # поставить основную директорию другую (в данном случа я поставил bot_predictions
    # в качестве основной)
    # WorkWithDataUsers('664295561').add_info_about_user_statistics(count_touch_help=True)
    # WorkWithDataUsers('112345678').add_info_about_user_statistics(username='lv_rey', full_name='lev reyn')
