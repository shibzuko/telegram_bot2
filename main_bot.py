# Import the necessary modules
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from os import getenv                  #Позволяет получать значения переменных окружения
from dotenv import load_dotenv         #Предоставляет функцию загрузки переменных окружения из файла .env


# Импорт модулей для работы с базой данных

from aiogram.contrib.fsm_storage.memory import MemoryStorage   # Импорт модуля для хранения состояний
from aiogram.dispatcher import FSMContext                      # Импорт модуля для работы с контекстом конечного автомата
from aiogram.dispatcher.filters import Command                 # Импорт модуля для фильтрации команд
from aiogram.dispatcher import filters                         # Импорт модуля для фильтрации сообщений
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # Импорт модулей для работы с клавиатурой
from sqlalchemy import create_engine, Column, Integer, String, DateTime  # Импорт модулей для работы с базой данных
from sqlalchemy.ext.declarative import declarative_base        # Импорт модуля для объявления таблицы
from sqlalchemy.orm import sessionmaker                        # Импорт модуля для работы с сессиями базы данных
from datetime import datetime                                  # Импорт модуля для работы с датой и временем


# Добавление объявления базы данных и создание таблицы сообщений

Base = declarative_base()
engine = create_engine('sqlite:///DataBase.db')  # Создание базы данных SQLite
Session = sessionmaker(bind=engine)
session = Session()

class Message(Base):
    __tablename__ = 'messages'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    user_id = Column(Integer)
    text = Column(String)
    date = Column(DateTime, default=datetime.utcnow)


# Подключение к базе данных и создание таблицы

Base.metadata.create_all(engine)

# messages = session.query(Message).all()
# for message in messages:
#     print(message.chat_id, message.date, message.user_id, message.id, message.text)


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
    # Добавление сохранения сообщений в базу данных
    new_message = Message(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        text=message.text,
        date=message.date
    )
    session.add(new_message)
    session.commit()
    # Вывод сообщения пользователю
    await message.answer(f'Ассаламу алейкум, {message.chat.first_name} {message.chat.last_name} '
                         f'\nСейчас: {message.date}')

# Start the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
