import logging
import requests
import io
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from past.builtins import execfile
from api_vk import get_user_status, get_user_photos_saved
from config import TOKEN, VK_ID, VIP_USER


# Создание клавиатуры
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
b1 = types.KeyboardButton('Помощь')
b2 = types.KeyboardButton('Сохры')
b3 = types.KeyboardButton('Статус')
b4 = types.KeyboardButton('Аватарка')
b5 = types.KeyboardButton('Ещё одна')
keyboard.add(b1, b2, b3, b4, b5)


help_text = """
/start - запуск бота, вызыв клавиатуры\n
/get_save_photo - оправит тебе созраненки\n
/help - ну эта команда для глупеньких\n
ну ара сытыми дальше и так все понятно..
"""


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



def download_photo(url):
    response = requests.get(url)
    return response.content

@dp.message_handler(commands='start')
async def start(message: types.Message):
    chat_id = message.chat.id
    if str(chat_id) == VIP_USER:
        await bot.send_message(chat_id, f'Чего желает самая прекрасная девушка на свете?🦭', reply_markup=keyboard)
    else:
        await bot.send_message(chat_id, f'Че надо?🗿', reply_markup=keyboard)


@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer(f'{help_text}')
    await message.delete()

@dp.message_handler(commands='get_save_photo')
async def get_save_photo(message: types.Message):
    media_group = []
    chat_id = message.chat.id
    if VK_ID.isdigit():
        photo_list = get_user_photos_saved(VK_ID)
        await message.answer('Секундочку...🐌')
        await bot.send_chat_action(chat_id, action=types.ChatActions.UPLOAD_PHOTO) # Сообщает юзеру об отправке фото
        for photo_url in photo_list:
            photo_content = download_photo(photo_url)
            photo_file = types.InputFile(io.BytesIO(photo_content), filename='photo.jpg')
            media_group.append(types.InputMediaPhoto(photo_file))
        await bot.send_chat_action(chat_id, action=types.ChatActions.UPLOAD_PHOTO) # Сообщает юзеру об отправке фото
        await message.answer('Крайние 10 сохраненок:')
        await bot.send_media_group(chat_id, media=media_group)
    await message.delete()


@dp.message_handler(commands='get_status')
async def get_status(message: types.Message):
    vk_status = get_user_status(VK_ID)['text']
    await message.answer(f'Статус: "{vk_status}" \U0001F60E')
    await message.delete()

@dp.message_handler(commands='get_avatar')
async def get_avatar(message: types.Message):

    await message.answer(f'Потом приходи')
    await message.delete()

@dp.message_handler(commands='mems')
async def mems(message: types.Message):
    await message.answer(f'Отстань.')
    await message.delete()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    if message.text == 'Помощь':
        await help(message)
    elif message.text == 'Сохры':
        await get_save_photo(message)
    elif message.text == 'Статус':
        await  get_status(message)
    elif message.text == 'Аватарка':
        await get_avatar(message)
    elif message.text == 'Ещё одна':
        await mems(message)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
