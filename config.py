import os
from dotenv import load_dotenv
load_dotenv('.env')
from decouple import config

TOKEN = config('TOKEN')

TOKEN = os.environ.get('TOKEN')
# VIP_USER = os.environ.get('VIP_USER')
# ADMIN = os.environ.get('ADMIN')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
