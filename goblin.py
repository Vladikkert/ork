from binance.client import Client
import pandas as pd
import talib

# Замените "YOUR_API_KEY" и "YOUR_SECRET_KEY" на свои
client = Client("YOUR_API_KEY", "YOUR_SECRET_KEY")

# Получаем исторические данные по тикеру
candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1DAY)

# Делаем из данных DataFrame
df = pd.DataFrame(candles, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
df['date'] = pd.to_datetime(df['date'], unit='ms')  # меняем формат даты
df.set_index('date', inplace=True)  # делаем дату индексом

# Конвертируем столбцы со строковых значений в числовые
df['open'] = pd.to_numeric(df['open'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['close'] = pd.to_numeric(df['close'])

# Вычисляем ATR с помощью TA-Lib
df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)

print(df.tail())