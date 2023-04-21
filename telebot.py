import telepot
import datetime

#telebot setting---------------
#https://api.telegram.org/bot5140303453:AAFw6eiUEMp_d9-Yb0RtecSpAIL8N5CS-wg/getUpdates
token='your token'
receiver_id='your receiver id'
bot = telepot.Bot(token)


#binance api setting--------------
from binance.client import Client
import pandas as pd

#binance api management
api_key="SU2jkWq1BCYkSH4e66lMO5Gy9ZCby6JNzsuywDpAblVow9KG8cXEJFwHptMmqVj8"
api_secret="Yd1e4PYbxBl44OZpXpeiiZANEKiza9Joc8gXJ6rXYSU4MUSRRJPCfju8vuSJoq2V"

client=Client(api_key,api_secret)


#interval setting then print the output----------------
# import time
# def sleeptime(hour,min,sec):
#     return hour*3600 + min*60 + sec


#price alert function-------------
def price_alert(asset,start,end,timeframe,change):
    df= pd.DataFrame(client.get_historical_klines(asset, timeframe,start,end))

    df=df.iloc[:,:5]
    df.columns=["Time","Open","High","Low","Close"]

    #df=df.set_index("Date")
    #df.index=pd.to_datetime(df.index,unit="ms")

    df=df.astype("float")
    df['Change%'] = df['Close'].pct_change()*100
    df['Change%'][1] =round( df['Change%'][1],2 ) 

    if (df['Change%'][1]>change or df['Change%'][1]<-change):
        df = df.drop(columns=['Open'])
        #setting TW tiemzone   have benn changed to utc so need to be changed to origin
        result = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

        result_1=result- datetime.timedelta(hours=1) 
        result_2=result- datetime.timedelta(hours=2) 

        df['Time'][0]=result_2.strftime("%H"+':00')
        df['Time'][1]=result_1.strftime("%H"+':00')
        df=df.set_index("Time")
        
        return str(df)
    return 

#time setting UTC an hour and two hours ago -----------
import datetime
gmt=datetime.datetime.now(datetime.timezone.utc)
gmt_minus3=gmt- datetime.timedelta(hours=3) 
gmt_minus1=gmt- datetime.timedelta(hours=1)



#parameter setting------------
import pandas as pd
#asset=["BTCUSDT",'ETHUSDT','BNBUSDT']
start=str(gmt_minus3)
end=str(gmt_minus1)
timeframe="1h"
change=3


#get all crypto-------------- 
exchange_info = client.get_exchange_info()

asset=[]
for s in exchange_info['symbols']:
    if ((s['symbol'] not in asset) and  (s['quoteAsset']=='USDT')):
        asset.append(s['symbol'])

# all crypto list
# second_forcypto = sleeptime(24,0,0)
# while 1==1:
#     time.sleep(second_forcypto)
#     exchange_info = client.get_exchange_info()
#     asset=[]
#     for s in exchange_info['symbols']:
#         if ((s['symbol'] not in asset) and  (s['quoteAsset']=='USDT')):
#             asset.append(s['symbol'])


#send message
#second_forprice = sleeptime(1,0,0)


bot.sendMessage(receiver_id, '-----------------------start') 

for symbol in asset:

    try:
        bot.sendMessage(receiver_id, symbol+' 1 hour change\n'+price_alert(symbol,start,end,timeframe,change)) # send a activation message to telegram receiver id

    except Exception:
    #except:
        #bot.sendMessage(receiver_id, 'error: '+symbol) 
        pass
bot.sendMessage(receiver_id, '-----------------------end') 
  
#  time.sleep(second_forprice)


# git push heroku master

#heroku run bash
#ls
#python telebot.py
#exit

#heroku ps -a telebot-binance
