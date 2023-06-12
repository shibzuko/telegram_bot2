from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///DataBase.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    user_name = Column(String)
    full_name = Column(String)
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'))
    message = Column(String)
    date_message = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="messages")


Base.metadata.create_all(engine)
