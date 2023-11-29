from binance.client import Client
import time

dragons = {
    'aurora': ['eaDTIsQ5anTJQWNd8KdZqerFr2kQ2X0dioykKT9kU69XmZpWyBe8klnIx3rthRbv',
               'nvNDoRwI2qNt7Nl39x6PNXfjPRgpWRmAJ0ycl2AHuhtKUE8SEaksiIq3DItn2cBD'],
    'ember': ['JOTK7zZtvvvoBurTfK9AUY8MorNkkvwjTxZv31t8nAKX6XTc0ny0mUBMxVYPf3Hr',
              '4BEyXc9QI3SHnHxmG4hMnYXzsGjj734fjMUKmeRkGsdjtkN77ZZ0R6W4nGCszYto'],
    'skye': ['XXwcdAfQT5pfD5NsBN5c3L7M2LxluCahZ8lGKHQkupEK0fQylJOhxS6Jccmn5uAv',
            'D5tBtvqTsycyijQ4p9jedUxqTLDczG2atPWEzZlPCWs8yVjSeSPayBCTu0ojysEe'],
    'zephyr': ['cwVc89C12hJYqKY3ppLQXz0WRW8526tTC7nHA23vZT4XJdPXtdj8o3r7qOUo4BG0',
              'EAIQnX9sBqMsrAVOqGZj2gSwDmC7nKSg0PYIr8NVbNbXonv5L89F1aONfxXwepzN'],
    'blaze': ['yYQ3XQMgWNdNU02dDTkR0YOvex5lGCNmhaxVfrisoND3plTfqnyax2zG9ksTaihc',
              'C2TnLAzpfs71ioRwftSTN9apMck7igF4rgix9EryFOmeFpWNFT5GJPvs42cs2VAr'],
    'main': ['D42XlP55hbZQbqd9EisDE4JFhEwLeMDIe1PmBAQC16UBuEdwEIPAgPlqchAfdM2w',
             'TAtBlHMHBjSXXcDF1T0NL02MyXBAo7lyDCD9cRHEUQDQ2PKZuTVKEuyKdfgle0v9']

}

for i in dragons:

    api_key = dragons[i][0]
    api_secret = dragons[i][1]


    client = Client(api_key, api_secret)
    balances = client.get_account()['balances']
    futures_balance = client.futures_account_balance()
    print(i)
    for j in balances:
        if j['asset'] == 'USDT':
            print(j['free'])
    for j in futures_balance:
        if j['asset'] == 'USDT':
            print(j['balance'])
    print()