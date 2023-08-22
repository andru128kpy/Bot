import logging
from asyncio import exceptions

import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from search import Exercise
import time

API_TOKEN = '6429432065:AAF_x119p7JPvpEK1hsE6j1vp2RKPALkllY'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

counter = 0
day_of_the_week = ["Понедельник-тяжёлая", "Понедельник-тяжёлая", "Пятница-средняя(лёгкая по ситуации)"]

exercise_1 = Exercise("Жим гантелей", ["10", "12.5", "15"], day_of_the_week)
exercise_2 = Exercise("Махм гантелями", ["10", "12.5", "15"], day_of_the_week)
exercise_3 = Exercise("Тяга вернего блока", ["50", "57", "63.5"], day_of_the_week)
exercise_4 = Exercise("тяга на спину", ["25", "30", "35"], day_of_the_week)
exercise_5 = Exercise("Жим ногами", ["50", "60", "80"], day_of_the_week)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    buttons = [
        InlineKeyboardButton(exercise_1.day_the_week[0], callback_data='button4'),
        InlineKeyboardButton(exercise_1.day_the_week[1], callback_data='button5'),
        InlineKeyboardButton(exercise_1.day_the_week[2], callback_data='button6')
    ]
    keyboard = InlineKeyboardMarkup()
    for button_1 in buttons:
        keyboard.add(button_1)


    await message.answer("День недели", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ['button4', 'button5', 'button6'])
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    buttons = [
        InlineKeyboardButton(exercise_1.name, callback_data=f'{exercise_1.name}'),
        InlineKeyboardButton(exercise_2.name, callback_data=f'{exercise_2.name}'),
        InlineKeyboardButton(exercise_3.name, callback_data=f'{exercise_3.name}'),
        InlineKeyboardButton(exercise_4.name, callback_data=f'{exercise_4.name}'),
        InlineKeyboardButton(exercise_5.name, callback_data=f'{exercise_5.name}')
    ]

    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)

    await bot.send_message(callback_query.from_user.id, "Программа тренеровки", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in [f'{exercise_1.name}', f'{exercise_2.name}'])
async def exercise_call_handling_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    buttons = [
        InlineKeyboardButton(exercise_1.weight[0], callback_data="button1"),
        InlineKeyboardButton(exercise_1.weight[1], callback_data="button2"),
        InlineKeyboardButton(exercise_1.weight[2], callback_data="button3")
    ]
    keybord = InlineKeyboardMarkup()
    for button in buttons:
        keybord.add(button)
    await bot.send_message(callback_query.from_user.id, f"'{callback_query.data}'", reply_markup=keybord)

@dp.callback_query_handler(lambda c: c.data in ["button1", "button2", "button3"])
async def reads_approach_call(callback_query: types.CallbackQuery):

    a_1 = InlineKeyboardButton("1", callback_data="button_a")
    a_2 = InlineKeyboardButton("2", callback_data="button_b")
    a_3 = InlineKeyboardButton("3", callback_data="button_c")
    a_4 = InlineKeyboardButton("4", callback_data="button_d")
    keyboard = InlineKeyboardMarkup()
    keyboard.add(a_1, a_2, a_3, a_4)
    await bot.send_message(callback_query.from_user.id, 'Подходы', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ["button_a", "button_b", "button_c", "button_d"])
async def rest_time_countdown(callback_query: types.CallbackQuery):
    global counter
    await bot.answer_callback_query(callback_query.id)

    sec = 0
    c = await bot.send_message(callback_query.from_user.id, f'Прошло {sec}')

    while sec <= 180:
        try:
            time.sleep(1)
            sec += 1
            await bot.edit_message_text(f"Прошло {sec}", chat_id=callback_query.from_user.id, message_id=c.message_id)
        except aiogram.utils.exceptions.MessageToEditNotFound:
            pass
        if sec == 180:
            a = await bot.send_message(callback_query.from_user.id, 'Вермя отдыха закончилось')
            time.sleep(1)
            await bot.delete_message(callback_query.from_user.id, message_id=c.message_id)
            time.sleep(2)
            await bot.delete_message(callback_query.from_user.id, message_id=a.message_id)
    counter += 1
    await bot.answer_callback_query(callback_query.id)
    if counter == 4:
        time.sleep(2)
        counter = 0
        await bot.send_message(callback_query.from_user.id, "Вы закончили упражнение перейдите к следующему")



@dp.callback_query_handler(lambda c: c.data in exercise_3.name)
async def reads_the_thrust_of_the_upper_block(callback_query: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(exercise_3.weight[0], callback_data="50"),
        InlineKeyboardButton(exercise_3.weight[1], callback_data="57"),
        InlineKeyboardButton(exercise_3.weight[2], callback_data="63.5")
    ]
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)
    await bot.send_message(callback_query.from_user.id, "Тяга верхнего блока", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in exercise_4.name)
async def reads_the_pressing_of_the_thrust_on_the_back(callback_query: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(exercise_4.weight[0], callback_data="25"),
        InlineKeyboardButton(exercise_4.weight[1], callback_data="30"),
        InlineKeyboardButton(exercise_4.weight[2], callback_data="35")
    ]
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)
    await bot.send_message(callback_query.from_user.id, "Тяга на спину", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in exercise_5.name)
async def reads_pressing_leg_press(callback_query: types.CallbackQuery):
    buttons = [
        InlineKeyboardButton(exercise_5.weight[0], callback_data="50"),
        InlineKeyboardButton(exercise_5.weight[1], callback_data="60"),
        InlineKeyboardButton(exercise_5.weight[2], callback_data="80")
    ]
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)
    await bot.send_message(callback_query.from_user.id, "Жим ногами", reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)








