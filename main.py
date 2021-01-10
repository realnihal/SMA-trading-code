import requests
from datetime import datetime
import matplotlib.pyplot as plt

# granularity: 60, 300, 900, 3600, 21600, 86400


def cbpGetHistoricRates(market='BTC-GBP', granularity=86400, iso8601start='', iso8601end=''):
    api = 'https://api.pro.coinbase.com/products/' + market + '/candles?granularity=' + \
        str(granularity) + '&start=' + iso8601start + '&end=' + iso8601end
    resp = requests.get(api)
    if resp.status_code != 200:
        raise Exception('GET ' + api + ' {}'.format(resp.status_code))
    data = {}
    for price in reversed(resp.json()):
        # time, low, high, open, close, volume
        iso8601 = datetime.fromtimestamp(price[0])
        timestamp = datetime.strftime(iso8601, "%d/%m/%Y %H:%M:%S")
        data[timestamp] = price[4]
    return data

# data: dictionary { 'dd/mm/yyy': price, 'dd/mm/yyyy': price, ... }
# num: number of values in the average calculation


def simpleMovingAverage(data, num):
    if not isinstance(data, dict):
        raise Exception('Dictionary input expected')
    if not isinstance(num, int):
        raise Exception('Integer input expected')
    if num < 5 or num > 200:
        raise Exception('Unusual numeric input detected')
    if (num > len(data)):
        raise Exception('Insufficient data for calculation')

    data_keys = list(data.keys())
    data_list = list(data.values())

    result = {}
    for x in range(len(data_list) - num + 1):
        series = data_list[x:x + num]
        result[data_keys[x + num - 1]] = round(sum(series) / num)

    return result


data = cbpGetHistoricRates('BTC-GBP', 86400)
sma20 = simpleMovingAverage(data, 20)
sma50 = simpleMovingAverage(data, 50)
sma200 = simpleMovingAverage(data, 200)


def csvResults():
    print('date,price,sma20,sma50,sma200')
    data_keys = list(data.keys())
    for key in data_keys:
        price = ''
        if key in data:
            price = str(data[key])

        sma20r = ''
        if key in sma20:
            sma20r = str(sma20[key])

        sma50r = ''
        if key in sma50:
            sma50r = str(sma50[key])

        sma200r = ''
        if key in sma200:
            sma200r = str(sma200[key])

        print(key + ',' + price + ',' + sma20r + ',' + sma50r + ',' + sma200r)


csvResults()

plt.plot(data.keys(),data.values())
plt.plot(sma20.keys(),sma20.values(),'r')
plt.plot(sma50.keys(),sma50.values(),'g')
plt.plot(sma200.keys(),sma200.values(),'y')
plt.show()