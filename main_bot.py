# Import the necessary modules
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from os import getenv                  #Позволяет получать значения переменных окружения
from dotenv import load_dotenv         #Предоставляет функцию загрузки переменных окружения из файла .env
load_dotenv()                          #Эта функция загружает значения переменных окружения фвйла .env в текущую среду
BOT_TOKEN = getenv('MY_API_TOKEN_1')   #Получаем значения переменной окружения с именем 'MY_API_TOKEN_1


# Set up logging / Настроить ведение журнала
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token=BOT_TOKEN)

# Create a dispatcher instance / Создаёт экземпляр диспетчера
dp = Dispatcher(bot)

# Define a message handler that echoes back messages / Определите обработчик сообщений, который повторяет сообщения
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f'Ассаламу алейкум, {message.chat.first_name} {message.chat.last_name} '
                         f'\nСейчас: {message.date}')

# Start the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
