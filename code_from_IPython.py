# IPython log file

get_ipython().system(u'dir /on ')
import cPickle
buying = cPickle.load(open('brokers_buying.dict'))
len(buying)
buying['WEALTH']
brokers = buying.keys()
brokers
buying['WEALTH  ']
selling = cPickle.load(open('brokers_selling.dict'))
selling['WEALTH  ']
def getTotalVolume(data):
    vol = 0
    for entry in data:
        vol += entry[2]
    return vol
getTotalVolume(selling['WEALTH  '])
getTotalVolume(buying['WEALTH  '])
brokers_volume_summary = {}
for b in brokers:
    brokers_volume_summary[b] = getTotalVolume(buying[b]) - getTotalVolume(selling[b])
    
brokers_volume_summary = {}
for b in brokers:
    try:
        buy = getTotalVolume(buying[b])
    except KeyError:
        buy = 0
    try:
        sell = getTotalVolume(selling[b])
    except KeyError:
        sell = 0
    brokers_volume_summary[b] = buy - sell
    
brokers_volume_summary
volume_broker = []
for b in brokers_volume_summary:
    volume_broker.append(brokers_volume_summary[b], b)
    
volume_broker = []
for b in brokers_volume_summary:
    volume_broker.append((brokers_volume_summary[b], b))
    
volume_broker.sort()
volume_broker
def getTotalPriceTimesVolume(data):
    for entry in data:
        try: priceTimesVolume += entry[1]*entry[2]
        except: priceTimesVolume = entry[1]*entry[2]
    return priceTimesVolume
getTotalPriceTimesVolume(buying['WEALTH  '])
getTotalPriceTimesVolume(selling['WEALTH  '])
def getAverageBuyingPrice(br):
    return getTotalPriceTimesVolume(buying[br])/getTotalVolume(buying[br])
def getAverageSellingPrice(br):
    return getTotalPriceTimesVolume(selling[br])/getTotalVolume(selling[br])
getAverageSellingPrice(buying['WEALTH  '])
getAverageSellingPrice('WEALTH  ')
getAverageBuyingPrice('WEALTH  ')
brokers_volume_average_sell_buy = {}
for b in brokers_volume_summary:
    try: aveSell = getAverageSellingPrice(b)
    except: aveSell = 0
    try: aveBuy = getAverageBuyingPrice(b)
    except: aveBuy = 0
    brokers_volume_average_sell_buy[b] = [brokers_volume_summary[b], aveSell, aveBuy]
    
brokers_volume_average_sell_buy
get_ipython().magic(u'logstart')
sum(buying.values())
sum(map(lambda x: x[2], buying.values()))
sum(map(lambda x: x[2], buying.values()))
buying['WEALTH  ']
sum(map(lambda x: getTotalVolume(x), buying.keys()))
sum(map(lambda x: getTotalVolume(buying[x]), buying.keys()))
buying
buying.values()
price_volume = {}
for d in buying.values():
    for dd in d:
        t, pr, vl = dd
        try: price_volume[pr] += vl
        except KeyError: price_volume[pr] = vl
        
price_volume
volume_price = []
for p in price_volume:
    volume_price.append((price_volume[p], p))
    
volume_price
sorted(volume_price)
get_ipython().magic(u'logstat')
get_ipython().magic(u'log')
get_ipython().magic(u'logstate')
exit()
