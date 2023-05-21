# Import the necessary modules
import logging
import pytz                            # Библиотека для работы с часовым поясом
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from os import getenv                  #Позволяет получать значения переменных окружения
from dotenv import load_dotenv         #Предоставляет функцию загрузки переменных окружения из файла .env


# Импорт модулей для работы с базой данных

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
    message_id = Column(Integer)
    user_id = Column(Integer)
    is_bot = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    language_code = Column(String)
    is_premium = Column(Integer)
    text = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

# messages = session.query(Message).all()
# for message in messages:
#     print(f"(message_id: {message.id}, user_id: {message.user_id}, "
#           f"is_bot: {message.is_bot}, first_name: {message.first_name}, last_name: {message.last_name}, "
#           f"username: {message.username}, language_code: {message.language_code}, "
#           f"is_premium: {message.is_premium}, text: {message.text}, date: {message.date})")


load_dotenv()                          #Эта функция загружает значения переменных окружения фвйла .env в текущую среду
BOT_TOKEN = getenv('MY_API_TOKEN_1')   #Получаем значения переменной окружения с именем 'MY_API_TOKEN_1

# Set up logging / Настроить ведение журнала
logging.basicConfig(level=logging.INFO)
# Create a bot instance
bot = Bot(token=BOT_TOKEN)
# Create a dispatcher instance / Создаёт экземпляр диспетчера
dp = Dispatcher(bot)

current_time = datetime.now(pytz.timezone('Europe/Moscow'))
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')


# Define a message handler that echoes back messages / Определите обработчик сообщений, который повторяет сообщения
@dp.message_handler()
async def echo(message: types.Message):
    # Добавление сохранения сообщений в базу данных
    new_message = Message(
        message_id=message.chat.id,
        user_id=message.from_user.id,
        is_bot=message.from_user.is_bot,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_premium=message.from_user.is_premium,
        text=message.text,
        date=message.date
    )

    # print(f"user_id: {new_message.user_id}, first_name: {new_message.first_name}, "
    #       f"last_name: {new_message.last_name}, username: {new_message.username}, text: {new_message.text}")

    session.add(new_message)
    session.commit()
    # Вывод сообщения пользователю
    await message.answer(f'Ассаламу алейкум, {message.chat.first_name} {message.chat.last_name} '
                         f'\nСейчас: {formatted_time}')



# Start the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
