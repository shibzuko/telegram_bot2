import logging
import requests
import io
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from past.builtins import execfile
from api_vk import get_user_status, get_user_photos_saved, photo_list

from config import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def hello(message: types.Message):
    media_group = []
    chat_id = message.chat.id
    VK_ID = '223134565'
    if VK_ID.isdigit():
        vk_status = get_user_status(VK_ID)['text']
        get_user_photos_saved(VK_ID)
        await message.answer('Секундочку...')
        await bot.send_chat_action(chat_id, action=types.ChatActions.UPLOAD_PHOTO)
        for photo_url in photo_list:
            photo_content = download_photo(photo_url)
            photo_file = types.InputFile(io.BytesIO(photo_content), filename='photo.jpg')
            media_group.append(types.InputMediaPhoto(photo_file))
        await bot.send_chat_action(chat_id, action=types.ChatActions.UPLOAD_PHOTO)
        await message.answer('Крайние 10 сохраненок:')
        await bot.send_media_group(chat_id, media=media_group)
        await message.answer(f'Статус: "{vk_status}" \U0001F60E')


    else:
        await message.answer('Введите VK ID')


def download_photo(url):
    response = requests.get(url)
    return response.content





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
