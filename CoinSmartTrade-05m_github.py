import pandas as pd
#import python-binance
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from IPython.display import display
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics as sts
from plyer import notification
import time


api_key = 'your api key'
api_secret = 'your secret code'
client = Client(api_key, api_secret)
data_coins = client.get_all_tickers()
#print(data_coins)

data_coins_all = pd.json_normalize(data_coins)
all_symbols = data_coins_all['symbol']
all_USDT_pairs = all_symbols[all_symbols.str.endswith('USDT')] ##342 pairs currently
all_USDT_pairs = all_USDT_pairs.reset_index()
all_USDT_pairs = all_USDT_pairs['symbol']



def find_relevant_pairs():
    Not_trading_pairs = ['AAVEDOWNUSDT','AAVEUPUSDT','BCCUSDT','VENUSDT','PAXUSDT','BCHABCUSDT','BCHSVUSDT','USDSUSDT','USDSBUSDT','ERDUSDT','NPXSUSDT','STORMUSDT','HCUSDT','MCOUSDT','BULLUSDT','BEARUSDT','ETHBULLUSDT','ETHBEARUSDT','EOSBULLUSDT','EOSBEARUSDT','XRPBULLUSDT','XRPBEARUSDT','STRATUSDT','BNBBULLUSDT','BNBBEARUSDT','XZCUSDT','LENDUSDT','BKRWUSDT','DAIUSDT']
    all_USDT_pairs_trading = all_USDT_pairs
    for i in Not_trading_pairs:
        indexx = pd.Index(all_USDT_pairs_trading).get_loc(i)
        #print(indexx)
        all_USDT_pairs_trading = all_USDT_pairs_trading.drop(index = indexx)
        all_USDT_pairs_trading = all_USDT_pairs_trading.reset_index()
        all_USDT_pairs_trading = all_USDT_pairs_trading['symbol']

    
    #print(all_USDT_pairs_trading.to_string())
    return all_USDT_pairs_trading


relevant_pairs = find_relevant_pairs()
#prices = client.get_all_tickers()
#prices1 = pd.json_normalize(prices)

#print(plot_dataa.iloc[672])

def trigger():
    
    iteration = 1
    
    while True:
        j = 0
        for j in range(0, len(relevant_pairs)):
            title = relevant_pairs.iloc[j] + ' Coin is Rising'
            message = 'Hurry! Hurry! First condition of this pair is satisfied, look into the chart quickly.'
            ## Setting up start time and end time
            end_time1 = datetime.today()  # Get timezone naive now
            end_timestamp1 = int(end_time1.timestamp()*1000)
            start_time1 = end_time1 - timedelta(hours=83, minutes=0) #getting data for last 3 days   83hours
            start_timestamp1 = int(start_time1.timestamp()*1000)
            data1 = client.get_klines(symbol = relevant_pairs.iloc[j], interval ='5m', startTime = start_timestamp1, endTime = end_timestamp1, limit = 1000)
            data_formated1 = pd.DataFrame(data1, columns = ['Open time','Open','High','Low','Close','Volume','Close Time','Quote Asset Volume','Number of Trades','junk1','junk2','junk3'])
            volume_data1 = data_formated1[['Volume']]
            #print(volume_data1.to_string())
            #print(volume_data1.str.len())
            


            end_time2 = start_time1  # Get timezone naive now
            end_timestamp2 = int(end_time2.timestamp()*1000)
            start_time2 = end_time2 - timedelta(hours=83, minutes=0) #getting data for last 3 days   83hours
            start_timestamp2 = int(start_time2.timestamp()*1000)
            data2 = client.get_klines(symbol = relevant_pairs.iloc[j], interval ='5m', startTime = start_timestamp2, endTime = end_timestamp2, limit = 1000)
            data_formated2 = pd.DataFrame(data2, columns = ['Open time','Open','High','Low','Close','Volume','Close Time','Quote Asset Volume','Number of Trades','junk1','junk2','junk3'])
            volume_data2 = data_formated2[['Volume']]
            #print(volume_data2.to_string())
            #print(volume_data2.str.len())

            
            volume_data = pd.concat([volume_data2, volume_data1], ignore_index = True)
            #print(volume_data.to_string())
            #print(volume_data.str.len())
            #break
            
            volume_data = volume_data.astype(float).round(decimals=0)
            volume_data = volume_data.astype(int)
            #print(volume_data)
            ## Get current value(latest)
            latest_volume = volume_data['Volume'].iloc[-1]
            ##plot data
            plot_data = pd.Series(volume_data['Volume'])
            plot_dataa = plot_data.sort_values(ascending = True)
            mean = int(sts.mean(plot_dataa))
            std = int(sts.stdev(plot_dataa))
            #median = sts.median(plot_dataa)
            threshold_volume = int(mean+2*std)  # verified it, will work fine
            #threshold_volume = min(plot_dataa)
            print(relevant_pairs.iloc[j])
            print('mean : ', mean)
            print('std : ', std)
            #print('median : ', median)
            print('max : ',max(plot_dataa))
            print('min : ',min(plot_dataa))
            print('threshold : ',threshold_volume)
            print('latest volume : ', latest_volume)
            print('#####')
            if latest_volume >= threshold_volume:
                notification.notify(title = title, message = message, app_icon = None, timeout=20, toast = False)
                
        #break
        print(iteration)
        print('#############')
        iteration = iteration + 1    





        

        #time.sleep(20)
        

trigger()

            
            
        

##Plot normal distribution data
#plt.plot(plot_dataa, norm.pdf(plot_dataa, mean, std))
#plt.show()


















