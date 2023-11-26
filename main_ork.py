
from binance.um_futures import UMFutures
from keys import dragons, TELEGRAM_TOKEN, TELEGRAM_CHANNEL
import time
import pickle
import threading
import shutil
import telebot
client = UMFutures(key=dragons['main'][0],  secret=dragons['main'][1])
StBot = telebot.TeleBot(TELEGRAM_TOKEN, num_threads=1)

#Добываем золото и обогащаем его
def get_gold():
    gold = client.ticker_24hr_price_change()
    sorted_gold = sorted(gold, key=lambda x: float(x['priceChangePercent']), reverse=True)
    sorted_gold_10 = sorted_gold[:6]
    enriched_gold = [d['symbol'] for d in sorted_gold_10]
    print(enriched_gold)
    return enriched_gold

#Создаем контейнер для обогащенного золота
def container_for_enriched_gold_create():
    container_for_enriched_gold = []

    with open('enriched_gold.pkl', 'wb') as f:
        pickle.dump(container_for_enriched_gold, f)

#Заставляем орка таскать золото в казну
def black_ork_work():
    take_gold = get_gold()

    with open('enriched_gold.pkl', 'rb') as f:
        container_for_enriched_gold = pickle.load(f)


    if len(container_for_enriched_gold) < 2:
        container_for_enriched_gold.append(take_gold)
    else:
        container_for_enriched_gold.pop(0)
        container_for_enriched_gold.append(take_gold)

    with open('enriched_gold.pkl', 'wb') as f:
        pickle.dump(container_for_enriched_gold, f)


##########################################################

#Проверяем чернорабочего работает ли он еще
def black_ork_check():
    with open('enriched_gold.pkl', 'rb') as f:
        container_for_enriched_gold = pickle.load(f)

    print(container_for_enriched_gold)  # выводит []


#Создаем чернорабочего и заставляем его работать пока не сдохнет
def create_black_ork_and_start_work():
    container_for_enriched_gold_create()
    while True:
        black_ork_work()
        black_ork_check()
        time.sleep(5)


#Берем готового чернорабочего и заставляем его работать пока не сдохнет
#Основная
def continue_black_ork_work():
    while True:
        try:
            black_ork_work()
        except Exception as m:
            print('Черный орк не хочет работать!', m)
        try:
            black_ork_check()
        except:
            print('Черный орк не хочет чтобы на него смотрели!')
        time.sleep(5)


####################################################################
####################################################################
####################################################################

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

    with open('enriched_gold.pkl', 'rb') as f:
         container_for_enriched_gold = pickle.load(f)

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


#Создаем контейнер для алмаза
def container_for_diamonds_create():
    container_for_diamonds = []
    with open('diamonds.pkl', 'wb') as f:
        pickle.dump(container_for_diamonds, f)


#Заставляем шамана таскать алмазы вождю
def shaman_ork_work():
    get_diamond = find_diamond()

    with open('diamonds.pkl', 'rb') as f:
        container_for_diamonds = pickle.load(f)


    if len(container_for_diamonds) < 2:
        container_for_diamonds.append(get_diamond)
    else:
        container_for_diamonds.pop(0)
        container_for_diamonds.append(get_diamond)

    with open('diamonds.pkl', 'wb') as f:
        pickle.dump(container_for_diamonds, f)


##########################################################

#Проверяем шамана работает ли он еще
def shaman_ork_check():
    with open('diamonds.pkl', 'rb') as f:
        container_for_diamonds = pickle.load(f)

    print(container_for_diamonds)  # выводит []


#Создаем шамана и заставляем его работать пока не сдохнет
def create_shaman_ork_and_start_work():
    try:
        container_for_diamonds_create()
    except:
        print('Не можем создать контейнер для алмаза')
    while True:
        try:
            shaman_ork_work()
        except:
            print('Шаман не хочет работать')
        try:
            shaman_ork_check()
        except:
            print('Шаман не хочет чтобы на него смотрели')
        time.sleep(5)

#Берем готового шамана и заставляем его работать пока не сдохнет
#Основная
def continue_shaman_ork_work():
    while True:
        try:
            shaman_ork_work()
        except:
            print('Шаман не хочет работать')
        try:
            shaman_ork_check()
        except:
            print('Шаман не хочет чтобы на него смотрели')
        time.sleep(5)


####################################################################
####################################################################
####################################################################
#Тестовый чернорабочий!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def continue_black_ork_work_test():
    while True:
        #black_ork_work()

        with lock:
            take_gold = get_gold()

            # gold = client.ticker_24hr_price_change(None)
            # print(gold[0]['priceChange'])
            # sorted_gold = sorted(gold, key=lambda x: float(x['priceChangePercent']), reverse=True)
            # sorted_gold_10 = sorted_gold[:15]
            # enriched_gold = [d['symbol'] for d in sorted_gold_10]

            #take_gold = enriched_gold


            with open('enriched_gold.pkl', 'rb') as f:
                container_for_enriched_gold = pickle.load(f)

            if len(container_for_enriched_gold) < 500:
                container_for_enriched_gold.append(take_gold)
                print('Количество золота:', len(container_for_enriched_gold))
            else:
                container_for_enriched_gold.pop(0)
                container_for_enriched_gold.append(take_gold)

                print('Количество золота:', len(container_for_enriched_gold))  # выводит []

            with open('enriched_gold.pkl', 'wb') as f:
                pickle.dump(container_for_enriched_gold, f)

        time.sleep(5)

####################################################################
####################################################################
####################################################################
#Тестовый шаман!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def continue_shaman_ork_work_test():
    while True:
        #shaman_ork_work()
        with lock:
            get_diamond = find_diamond()
            print('Алмаз найден! Это:', get_diamond[0], 'Его сила равна:',  get_diamond[1])

            if get_diamond[1] > 4:

                    StBot.send_message(TELEGRAM_CHANNEL, get_diamond)



                ##########################################

                #shaman_ork_check()


        time.sleep(5)

####################################################################
####################################################################
####################################################################
#Телеграмм грифон



if __name__ == "__main__":
    a = 1
    if a == 1:
        #Запускаем добычу золота чернорабочим орков
        ############ Если хотим пересоздать орка, то target=create_black_ork_and_start_work()
        ### Если хотим продолжить таскать золото, то target=continue_black_ork_work()
        lock = threading.Lock()
        black_ork_work = threading.Thread(target=continue_black_ork_work_test)
        black_ork_work.start()
        #Запускаем поиск алмаза из добытого золота шаманом орков
        ############ Если хотим пересоздать орка, то target=create_shaman_ork_and_start_work()
        ### Если хотим продолжить таскать золото, то target=continue_shaman_ork_work()
        shaman_ork_work = threading.Thread(target=continue_shaman_ork_work_test)
        shaman_ork_work.start()
    else:
        #Если надо перезапустить даймонд
        diamond = [] 
        with open('diamonds.pkl', 'wb') as f:
            pickle.dump(diamond, f)
        with open('diamonds.pkl', 'rb') as f:
            container_for_diamonds = pickle.load(f)
        print(container_for_diamonds)

