from binance.um_futures import UMFutures
from keys import dragons, TELEGRAM_TOKEN, TELEGRAM_CHANNEL
import requests

DEPOSIT = 100

client = UMFutures(key=dragons['aurora'][0],  secret=dragons['aurora'][1])


def open_market_order(symbol):
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
    print(response)



open_market_order('1000SHIBUSDT')