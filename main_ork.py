
from binance.um_futures import UMFutures
from keys import dragons, TELEGRAM_TOKEN, TELEGRAM_CHANNEL
import time
import pickle
import threading
import shutil
import telebot
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]', datefmt='%d/%m/%Y %I:%M:%S',
                    encoding = 'utf-8', filemode='w')

warlock = logging.getLogger(__name__)
handler = logging.FileHandler('warlock.log', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]')
handler.setFormatter(formatter)
warlock.addHandler(handler)

Wyverna = telebot.TeleBot(TELEGRAM_TOKEN, num_threads=1)

DEPOSIT = 100

client = UMFutures(key=dragons['aurora'][0],  secret=dragons['aurora'][1])

#Функция загрузки из файла
def load(file):
    with open(f'{file}.pkl', 'rb') as f:
        data = pickle.load(f)
    return data


#Функция записи в файл
def dump(file, data):
    with open(f'{file}.pkl', 'wb') as f:
        pickle.dump(data, f)


#Добываем золото и обогащаем его
def get_gold():
    gold = client.ticker_24hr_price_change()
    sorted_gold = sorted(gold, key=lambda x: float(x['priceChangePercent']), reverse=True)
    sorted_gold_10 = sorted_gold[:6]
    enriched_gold = [d['symbol'] for d in sorted_gold_10]
    #print(enriched_gold)
    return enriched_gold


#Находим алмаз
def find_diamond():
    # shutil.copyfile("enriched_gold.pkl", "enriched_gold_for_diamond.pkl")
    # with open('enriched_gold_for_diamond.pkl', 'rb') as f:
    #     container_for_enriched_gold = pickle.load(f)
    #
    # diamond_in_gold = {enriched_gold: 0 for enriched_gold in container_for_enriched_gold[0]}
    #
    # for i in range(1, len(container_for_enriched_gold)):
    #     for enriched_gold in container_for_enriched_gold[i]:
    #         try:
    #             diamond_in_gold[enriched_gold] += container_for_enriched_gold[i-1].index(enriched_gold) - container_for_enriched_gold[i].index(enriched_gold)
    #         except KeyError:
    #             diamond_in_gold[enriched_gold] = 5 - container_for_enriched_gold[i].index(enriched_gold)
    #             del diamond_in_gold[''.join(map(str, set(diamond_in_gold.keys()) - set(container_for_enriched_gold[i])))]
    #
    # diamond = max(diamond_in_gold, key=diamond_in_gold.get)
    #
    # return [diamond, diamond_in_gold[diamond]]
    container_for_enriched_gold = load('enriched_gold')

    diamond_in_gold = {enriched_gold: 0 for enriched_gold in container_for_enriched_gold[0]}

    for i in range(1, len(container_for_enriched_gold)):
        current_runners = set(container_for_enriched_gold[i])
        current_changes = set(diamond_in_gold)

        binance_add_new_crypto = current_runners - current_changes
        binance_del_crypto = current_changes - current_runners

        # print('runners', )
        # print('binance_add_new_crypto', binance_add_new_crypto, len(binance_add_new_crypto))
        # print('binance_del_crypto', binance_del_crypto, len(binance_del_crypto))
        if len(binance_add_new_crypto) > 0:
            for j in binance_add_new_crypto:
                diamond_in_gold[j] = 0
        if len(binance_del_crypto) > 0:
            for j in binance_del_crypto:
                del diamond_in_gold[j]
        for enriched_gold in container_for_enriched_gold[i]:
            if enriched_gold in container_for_enriched_gold[i - 1]:
                diamond_in_gold[enriched_gold] += container_for_enriched_gold[i - 1].index(enriched_gold) - container_for_enriched_gold[i].index(enriched_gold)

    diamond = max(diamond_in_gold, key=diamond_in_gold.get)

    return [diamond, diamond_in_gold[diamond]]


#Идем в атаку!
def orks_attack(symbol):
    # Получить информацию об обмене
    exchange_info = client.exchange_info()


    rounder = 0


    # Перебрать все пары торговли
    for symbol_info in exchange_info['symbols']:
        # Найти информацию для нашей криптовалюты
        if symbol_info['symbol'] == symbol:
            # Перебрать все ограничения
            for filter in symbol_info['filters']:
                # Найти ограничение LOT_SIZE
                if filter['filterType'] == 'LOT_SIZE':
                    # Вернуть минимальное количество
                    min_quantity = str(filter['minQty'])

                    if '.' in min_quantity:
                        num = min_quantity.split('.')[0]
                        if int(num) == 0:
                            rounder = len(min_quantity.split('.')[1])
                        else:
                            rounder = 0
                    else:
                        rounder = 0


    price = round(float(client.ticker_price(symbol)['price']), 5)

    volume = round(DEPOSIT/price, rounder)
    print(f"Trade volume: {volume}")

    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': volume,
    }

    response = client.new_order(**params)


####################################################################
####################################################################
####################################################################


def black_ork_work():
    count_wyverna = 320
    while True:

        #Добываем золото
        try:

            take_gold = get_gold()
        
        except Exception as e:
            warlock.critical('Добыча золота приостановилась мой вождь!')
            warlock.exception(e)
            time.sleep(60)
            continue


        #Сохраняем золото
        try:

            container_for_enriched_gold = load('enriched_gold')

            if len(container_for_enriched_gold) < 500:
                container_for_enriched_gold.append(take_gold)
                #print('Количество золота:', len(container_for_enriched_gold))
            else:
                container_for_enriched_gold.pop(0)
                container_for_enriched_gold.append(take_gold)

                #print('Количество золота:', len(container_for_enriched_gold)) 
                

            dump('enriched_gold', container_for_enriched_gold)
       
        except Exception as e:
            warlock.critical('золото не сохраняется!')
            warlock.exception(e)
            time.sleep(60)
            continue

        # Отправляем сообщение что орк работает
        if count_wyverna == 325:    
            try:
                warlock.info('Орки добывают руду!')
                Wyverna.send_message(TELEGRAM_CHANNEL, 'Орки добывают руду!')
                count_wyverna = 0
        
            except Exception as e:
                warlock.critical('Виверна приболела!')
                warlock.exception(e)
                time.sleep(60)
                continue

        count_wyverna += 1


        time.sleep(5)


def shaman_ork_work():
    while True:
        try:
            #shaman_ork_work()
            get_diamond = find_diamond()
            #print('Алмаз найден! Это:', get_diamond[0], 'Его сила равна:',  get_diamond[1])
        except:
            time.sleep(60)
            print("Проблемы c поиском алмазов!")
            continue

        if get_diamond[1] > 4:
            if get_diamond[0] != load('last_diamond'):
                
                try:
                    orks_attack(get_diamond[0])
                except Exception as e:
                    warlock.critical('Атака провалилась!')
                    warlock.exception(e)
                    time.sleep(60)
                    continue

                try:
                    Wyverna.send_message(TELEGRAM_CHANNEL, get_diamond)
                except Exception as e:
                    warlock.critical('Виверна не смогла доставить алмаз!')
                    warlock.exception(e)
                    time.sleep(60)
                    continue

                dump('last_diamond', get_diamond[0])


        time.sleep(5) 

####################################################################
####################################################################
####################################################################


if __name__ == "__main__":

    #Запускаем добычу золота чернорабочим орков
    black_ork_work = threading.Thread(target=black_ork_work)
    black_ork_work.start()

    #Запускаем поиск алмаза из добытого золота шаманом орков
    shaman_ork_work = threading.Thread(target=shaman_ork_work)
    shaman_ork_work.start()
