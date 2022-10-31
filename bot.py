from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from config import token
from work_with_data_users.work_with_data_users import WorkWithDataUsers
import aioschedule


bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
import asyncio


@dp.message_handler(commands=['start'])
async def start_process_command(message: types.Message):
    """начало работы бота"""
    await message.delete()
    WorkWithDataUsers(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Привет, я предсказываю будущее, и если тебе не похуй, то забей'
                                                 ' хуй и раз в день получай эту хуйню, ведь это точно правдивые '
                                                 'предсказания!!!')


@dp.message_handler(commands=['send_prediction'])
async def start_process_command(message: types.Message):
    """отправляет всем зареганым предсказание"""
    print(message.text)
    for user_telegram_id in WorkWithDataUsers(message.from_user.id).get_all_users():
        try:
            await bot.send_message(user_telegram_id, WorkWithDataUsers(user_telegram_id).get_prediction())
        except BotBlocked:
            # нужно добавлять в список тех, кто остановил бота, и возможно потом удалять их, хз
            print(f'пользователь с telegram_id {user_telegram_id} остановил бота')


@dp.message_handler()
async def start_process_command_no_command():
    """отправляет всем зареганым предсказание"""
    for user_telegram_id in WorkWithDataUsers('664295561').get_all_users():
        try:
            await bot.send_message(user_telegram_id, WorkWithDataUsers(user_telegram_id).get_prediction())
        except BotBlocked:
            # нужно добавлять в список тех, кто остановил бота, и возможно потом удалять их, хз
            print(f'пользователь с telegram_id {user_telegram_id} остановил бота')


async def scheduler():
    aioschedule.every().day.at("11:14").do(start_process_command_no_command)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


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
