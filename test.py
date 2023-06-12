import time

from models import User, Message, session
def add_user(chat_id, username, fullname):
    if isinstance(username, str):
        username = username.lower()
    user = User(
        telegram_id=int(chat_id),
        user_name=username,
        full_name=fullname,
    )
    session.add(user)
    session.commit()

def add_new_message(message):
    chat_id = message.chat.id
    username = message.chat.username
    fullname = f'{message.chat.first_name} {message.chat.last_name}'
    user = session.query(User).filter_by(telegram_id=message.chat.id).first()
    if user is None:
        add_user(chat_id, username, fullname)
        user = session.query(User).filter_by(telegram_id=message.chat.id).first()

    new_message = Message(
        telegram_id=user.telegram_id,
        message=message.text,
        date_message=message.date,
    )
    session.add(new_message)
    session.commit()



def get_user_messages(identifier):
    # Проверяем, является ли `identifier` числовым значением (chat_id)
    if isinstance(identifier, int):
        user = session.query(User).filter_by(telegram_id=identifier).first()
    else:
        # Если `identifier` не является числовым значением, предполагаем, что это username
        user = session.query(User).filter_by(user_name=identifier.lower()).first()

    if user:
        messages = session.query(Message).filter_by(telegram_id=user.telegram_id).all()
        return messages
    else:
        return None

