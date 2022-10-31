import os
from work_with_data_users.in_json import InJson
from random import choice


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


if __name__ == '__main__':
    os.chdir('../')  # поставить основную директорию другую (в данном случа я поставил bot_predictions
    # в качестве основной)
    dima = WorkWithDataUsers('664295561')
    print(dima.get_prediction())
