import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs
import matplotlib.pyplot as plt
import openpyxl

import telegram

bot = telegram.Bot(token ='6104850765:AAEW-6O9zQh91XAsDBsk9BYlE8Gkp6XsfK8')
chat_id = '5701817724'
updates = bot.getUpdates()

text = 'TMF매수 신호 입니다.'

bot.send_message(chat_id=chat_id, text=text)


import asyncio

async def main():
    bot = telegram.Bot('6104850765:AAEW-6O9zQh91XAsDBsk9BYlE8Gkp6XsfK8')
    async with bot:
        print(await bot.get_me())

if __name__ == '__main__':
    asyncio.run(main())


    token = '6104850765:AAEW-6O9zQh91XAsDBsk9BYlE8Gkp6XsfK8'
    bot = telegram.Bot(token = token)
    await bot.send_message(chat_id, '매수 타이밍 입니다.')

asyncio.run(main())


# 시작날짜 및 종료일자 설정
start_date = '2022-03-10'
end_date = '2023-02-10'

# 미국 +20년물 채권 ETF 데이터 로드
ticker1 = 'TMF'
etf_df = yf.download(ticker1, start=start_date, end=end_date)
_sr = etf_df['Close']
etf_df = pd.DataFrame(_sr)
etf_df.rename(columns={'Close':ticker1}, inplace=True)
etf_df.tail(3)

a = etf_df.iloc[-1, ]
if float(a) <= 8.5:
