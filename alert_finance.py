import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs
import matplotlib.pyplot as plt
import openpyxl
import telegram
import asyncio
import time
import datetime
import schedule

CHAT_ID = '5701817724'

import asyncio

async def alarm_TMF():
    import telegram
    CHAT_ID = '5701817724'
    token = '6104850765:AAEW-6O9zQh91XAsDBsk9BYlE8Gkp6XsfK8'
    bot = telegram.Bot(token = token)
    async with bot:
        await bot.send_message(CHAT_ID, '현재 TMF가 5% 하락한 상태 입니다.')

asyncio.run(alarm_TMF())


schedule.every(5).seconds.do(asyncio.run(alarm_TMF()))

while True:
    schedule.run_pending()
    time.sleep(1)

# 시작날짜 및 종료일자 설정
x = datetime.datetime.now()
x.year
x.month
x.day
x.hour
x.minute
x.second


datetime.MINYEAR
datetime.MAXYEAR
datetime.UTC
datetime.datetime.now()

# 미국 +20년물 채권 ETF 데이터 로드
ticker1 = 'TMF'
etf_df = yf.download(ticker1, start=start_date, end=end_date)
_sr = etf_df['Close']
etf_df = pd.DataFrame(_sr)
etf_df.rename(columns={'Close':ticker1}, inplace=True)
etf_df.tail(3)

a = etf_df.iloc[-1, ]
a
if float(a) >= 8.5:
    asyncio.run(alarm_TMF())
else:
    pass


