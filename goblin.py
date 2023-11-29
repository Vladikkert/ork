from binance.um_futures import UMFutures
from keys import dragons, TELEGRAM_TOKEN, TELEGRAM_CHANNEL
import time
import pickle
import threading
import shutil
import telebot



#Функция загрузки из файла
def load(file):
    with open(f'{file}.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

#Функция записи в файл
def dump(file, data):
    with open(f'{file}.pkl', 'wb') as f:
        pickle.dump(data, f)


dump('last_diamond', 'APTUSDT')
print(load('last_diamond'))