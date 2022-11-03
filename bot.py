from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from aiogram.types import InputFile  # для того, что бы отправлять файлы
from config import token
from work_with_data_users.work_with_data_users import WorkWithDataUsers
import aioschedule
import asyncio
from mytime.mytime import MyTime  # класс для подсчёта времени до следующего предсказания
from work_with_data_users.in_json import InJsonDict, InZIP

bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

time_predications = '10:14'  # время отправления предсказания


@dp.message_handler(commands=['start'])
async def start_process_command(message: types.Message):
    """начало работы бота
    (доработать так, что бы собиралась информация о пользователях бота (full_name, username, is_premium и т.д.)"""
    await message.delete()
    WorkWithDataUsers(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           f"{message.from_user.full_name}, это бот хмельных вечеров, но в телеге я буду дневным 😱, "
                           f"в общем, я предсказываю будущее, каждое утро ты будешь получать от меня сообщение, они "
                           f"тебя могут испугать, так что осторожней"
                           f" и если не подпишешься на https://vk.com/bomji.sarapul" + ", то ты БОМЖ... или СОМЖ")
    WorkWithDataUsers(message.from_user.id).add_info_about_user_statistics(count_touch_start=True,
                                                                           username=message.from_user.username,
                                                                           full_name=message.from_user.full_name,
                                                                           work_or_stop='+')


@dp.message_handler(commands=['send_prediction'])
async def send_predictions_process_command(message: types.Message):
    """отправляет всем зареганым предсказание

    для того, что бы запустилась эта команда, необходимо, что бы в сообщении было слово гейоргий"""
    if 'гейоргий' not in message.text:
        return None
    # print(message.text)
    for user_telegram_id in WorkWithDataUsers(message.from_user.id).get_all_users():
        try:
            await bot.send_message(user_telegram_id, WorkWithDataUsers(user_telegram_id).get_prediction())
            WorkWithDataUsers(user_telegram_id).add_info_about_user_statistics(work_or_stop='+')
        except BotBlocked:
            # нужно добавлять в список тех, кто остановил бота, и возможно потом удалять их, хз
            WorkWithDataUsers(user_telegram_id).add_info_about_user_statistics(work_or_stop='-')
            print(f'пользователь с telegram_id {user_telegram_id} остановил бота')


@dp.message_handler(commands=['help'])
async def help_process_command(message: types.Message):
    WorkWithDataUsers(message.from_user.id).add_info_about_user_statistics(count_touch_help=True,
                                                                           username=message.from_user.username,
                                                                           full_name=message.from_user.full_name,
                                                                           work_or_stop='+')
    await bot.send_message(message.from_user.id, f'{message.from_user.full_name}, помощи нет, хмель единственный твой'
                                                 f' выход https://vk.com/bomji.sarapul')


@dp.message_handler(commands=['next_prediction'])
async def next_prediction_process_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'следующее предсказание '
                           f'будет через {MyTime(time_predications).next_prediction_declensions_func()}🙊 '
                           f'но помни, что бывают неожиданные предсказания 👺')
    WorkWithDataUsers(message.from_user.id).add_info_about_user_statistics(count_touch_next_prediction=True,
                                                                           username=message.from_user.username,
                                                                           full_name=message.from_user.full_name,
                                                                           work_or_stop='+')


@dp.message_handler(commands=['get_info_about_users'])
async def get_info_about_users_process_command(message: types.Message):
    """получить информацию о пользователях:
     количество пользователей
     их telegram_id
     count_predictions
     может потом ещё, что добавить можно будет, дополнительно проверка пароля будет так же

     для того, что бы запустилась эта команда, необходимо, что бы в сообщении было слово гейоргий
     """
    if 'гейоргий' not in message.text:
        return None
    WorkWithDataUsers(message.from_user.id).get_real_users()
    await bot.send_message(message.from_user.id,
                           f'number of users real {WorkWithDataUsers(message.from_user.id).get_real_users()}')
    await bot.send_message(message.from_user.id,
                           f'number of users all {len(WorkWithDataUsers(message.from_user.id).get_info_about_users())}')
    WorkWithDataUsers(message.from_user.id).create_csv_info_about_users()
    path = 'data_info_about_user.csv'
    await message.answer_document(InputFile(path))


@dp.message_handler(commands=['get_statistics_about_users'])
async def get_statistics_about_users_process_command(message: types.Message):
    """получить статистику о юзерах """
    if 'гейоргий' not in message.text:
        return None
    await bot.send_message(message.from_user.id, 'два вида статистики, в json формате и csv')
    await message.answer_document(InputFile('data_users/statistics/data_about_users_statistics.json'))

    InJsonDict('data_users/statistics/data_about_users_statistics.json').json_in_csv(
        'data_users/statistics/data_about_users_statistics.csv',
        key_one=str(message.from_user.id))
    await message.answer_document(InputFile('data_users/statistics/data_about_users_statistics.csv'))


@dp.message_handler(commands=['get_zipfile_sent_predictions_users'])
async def get_zipfile_sent_predictions_users_process_command(message: types.Message):
    """получить zipfile отправленных сообщений юзерам"""
    if 'гейоргий' not in message.text:
        return None
    # закидываем в zip файл все файлы из data_users/sent_predictions_users
    InZIP('data_users/sent_predictions_users.zip').create_zip('data_users/sent_predictions_users')
    await message.answer_document(InputFile('data_users/sent_predictions_users.zip'))


# @dp.message_handler()
async def timer_no_command():
    """отправляет всем зареганым предсказание"""
    print('pizda')
    for user_telegram_id in WorkWithDataUsers('664295561').get_all_users():
        try:
            await bot.send_message(user_telegram_id, WorkWithDataUsers(user_telegram_id).get_prediction())
            WorkWithDataUsers(user_telegram_id).add_info_about_user_statistics(work_or_stop='+')

        except BotBlocked:
            # нужно добавлять в список тех, кто остановил бота, и возможно потом удалять их, хз
            print(f'пользователь с telegram_id {user_telegram_id} остановил бота')
            WorkWithDataUsers(user_telegram_id).add_info_about_user_statistics(work_or_stop='-')


async def scheduler():
    aioschedule.every().day.at(time_predications).do(timer_no_command)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    # executor.start_polling(dp)
    # executor.start_polling(dp, skip_updates=True, on_startup=scheduler)
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)

# async def scheduler(m):
#     """позволяет запустить функцию в определённое время"""
#     aioschedule.every().day.at("11:08").do(start_process_command_no_command)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)



# доработать get_info_about_users, что бы считало только количество тех, кто не заблокировал бота
# создать команду, которая позволяет добавлять новые предсказания в бота удалённо
# создать команду админскую, которая рассказывает о всех командах в боте
