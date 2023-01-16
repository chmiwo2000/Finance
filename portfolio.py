# 한국은행 자료 받아오는 구간임
import pandas as pd
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import requests

key = "5H6P7H8QSOH3MNPO08UZ"
n = '100000'
date1 = '20100101'
date2 = '20221231'


def get_ECOS(key, n, date1, date2, item_code1, interval, item_code2, item_code3):
    url = f"http://ecos.bok.or.kr/api/StatisticSearch/{key}/xml/kr/1/{n}/{item_code1}/{interval}/{date1}/{date2}/{item_code2}/{item_code3}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'xml')
    item_list = soup.findAll('row')

    stat_code1 = []
    stat_code2 = []
    stat_code3 = []
    stat_name = []
    item_name1 = []
    item_name2 = []
    unit_name = []
    time = []
    value = []

    for item in item_list:
        stat_code1.append(item.find('STAT_CODE').text)
        stat_code2.append(item.find('ITEM_CODE1').text)
        stat_code3.append(item.find('ITEM_CODE2').text)
        stat_name.append(item.find('STAT_NAME').text)
        item_name1.append(item.find('ITEM_NAME1').text)
        item_name2.append(item.find('ITEM_NAME2').text)
        unit_name.append(item.find('UNIT_NAME').text)
        time.append(item.find('TIME').text)
        value.append(item.find('DATA_VALUE').text)

    data = pd.concat([pd.DataFrame(stat_code1),
                      pd.DataFrame(stat_code2),
                      pd.DataFrame(stat_code3),
                      pd.DataFrame(stat_name),
                      pd.DataFrame(item_name1),
                      pd.DataFrame(item_name2),
                      pd.DataFrame(time),
                      pd.DataFrame(value),
                      pd.DataFrame(unit_name)], axis = 1)
    data.columns = ['통계코드', '세부통계코드', '코드명', '항목명', '세부항목명', '계정명', '기간', '값', '단위']
    return data




# 이제 위의 정의된 함수에 따라서 받아올 수 있는 값들을 정의한 자료 더미들을 만든다.
# 연간으로 조회할 지표
combination_ECOS = [['817Y002', 'D', '010190000', '']]


# 위에서 검색한 리턴된 데이터 값을 다시 받아서 '엑셀'로 저장을 하기 위한 코드
df_ecos_a = pd.DataFrame()
df_ecos_a.to_excel('C:/Users/chmiw/Desktop/Programming/Finance/ECOS.xlsx', sheet_name='Sheet0')
a = 1

for i in combination_ECOS:
    data = get_ECOS(key, n, date1, date2, i[0], i[1], i[2], i[3])
    data["값"] = pd.to_numeric(data['값'])
    df_ecos_a = df_ecos_a.append(data, ignore_index=True)
    with pd.ExcelWriter('C:/Users/chmiw/Desktop/Programming/Finance/ECOS.xlsx', mode = 'a') as writer:
        data.to_excel(writer, sheet_name=f'Sheet{a}')
    a = a + 1
print(df_ecos_a)


# for문에서 오류가 날 경우를 대비한 검증용
j = combination_ECOS[0]
test_url = f"http://ecos.bok.or.kr/api/StatisticSearch/{key}/xml/kr/1/{n}/{j[0]}/{j[1]}/{date1}/{date2}/{j[2]}/{j[3]}"
print(test_url)
# 해당 URL을 클릭해서 정상적으로 페이지가 이동되는지 확인
# 정상적으로 이동되었다면, 컬럼이 맞는지 확인하기 위해서 조작
test_data = get_ECOS(key, n, date1, date2, j[0], j[1], j[2], j[3])
test_data.head()

# ECOS 홈페이지 내 통계코드 검색에서 확인
# ['902Y015', 'A', 'KOR', ''],
# ['901Y027', 'A', 'I61E', 'I28A'],
# ['731Y004', 'A', '0000001', '0000100'],
# ['801Y002', 'A', '401000A', ''],
# ['901Y054', 'A', 'MO3AB', 'AB'],
# ['901Y054', 'A', 'MO3AA', 'AB'],
# ['902Y002', 'A', '3010101', ''],
# ['722Y001', 'A', '0101000', ''],
# ['121Y006', 'A', 'BECBLA0202', '']


# 특정 기간 동안 국고채(1, 2, 3, 5, 10, 20, 30, 50년)금리 일별 자료 뽑아서 그래프로 표현
rate_ECOS = [
    ['817Y002', 'D', '010190000', ''],
    ['817Y002', 'D', '010195000', ''],
    ['817Y002', 'D', '010200000', ''],
    ['817Y002', 'D', '010200001', ''],
    ['817Y002', 'D', '010210000', ''],
    ['817Y002', 'D', '010220000', ''],
    ['817Y002', 'D', '010230000', ''],
    ['817Y002', 'D', '010240000', '']
]
rate_data = pd.DataFrame()

for k in rate_ECOS:
    data = get_ECOS(key, n, date1, date2, k[0], k[1], k[2], k[3])
    data['값'] = pd.to_numeric(data['값'])
    rate_data = pd.concat([rate_data, data[['기간', '세부항목명', '값']]])
    print(data['세부항목명'][0])


# 각 자료를 뽑아서 년도수 별로 그림 그리는 것까지는 확인함
# 이제 남은 단계는 각 년도수에 대한 레이블을 추가하고 앞의 일자를 공유해서 concat을 통해
# 열로 붙여나가는 것이다. 기간을 통일하고, 열 방향으로 데이터를 뻗게해서 그래프로 그려낸다.

import matplotlib.pyplot as plt

x = rate_data[rate_data['세부항목명'] == '국고채(1년)']['기간']
y1 = rate_data[rate_data['세부항목명'] == '국고채(1년)']['값']
y1 = rate_data[rate_data['세부항목명'] == '국고채(1년)']['값']
y2 = rate_data[rate_data['세부항목명'] == '국고채(2년)']['값']
y3 = rate_data[rate_data['세부항목명'] == '국고채(3년)']['값']
y5 = rate_data[rate_data['세부항목명'] == '국고채(5년)']['값']
y10 = rate_data[rate_data['세부항목명'] == '국고채(10년)']['값']
plt.plot(y1)
plt.plot(y2)
plt.plot(y3)
plt.plot(y5)
plt.plot(y10)
plt.show()




# 필요한 라이브러리 로드
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs
import matplotlib.pyplot as plt


# 시작날짜 및 종료일자 설정
start_date = '2010-10-31'
end_date = '2023-01-09'

# 미국 +20년물 채권 ETF 데이터 로드
ticker1 = 'TMF'
etf_df = yf.download(ticker1, start=start_date, end=end_date)
_sr = etf_df['Close']
etf_df = pd.DataFrame(_sr)
etf_df.rename(columns={'Close':ticker1}, inplace=True)
etf_df.head(3)

# 미국 30년물 시장금리 데이터 로드
ticker2 = '^TYX'
rate_df = yf.download(ticker2, start=start_date, end=end_date)
_sr = rate_df['Close']
rate_df = pd.DataFrame(_sr)
rate_df.rename(columns={'Close':ticker2}, inplace=True)
rate_df.head(3)

# 미국 나스닥 데이터 로드
ticker3 = '^IXIC'
nas_df = yf.download(ticker3, start=start_date, end=end_date)
_sr = nas_df['Close']
nas_df = pd.DataFrame(_sr)
nas_df.rename(columns={'Close':ticker3}, inplace=True)
nas_df.head(3)

# 미국 s&p500 데이터 로드
ticker4 = '^GSPC'
snp_df = yf.download(ticker4, start=start_date, end=end_date)
_sr = snp_df['Close']
snp_df = pd.DataFrame(_sr)
snp_df.rename(columns={'Close':ticker4}, inplace=True)
snp_df.head(3)

# 미국 다우존스 데이터 로드
ticker5 = '^DJI'
dow_df = yf.download(ticker5, start=start_date, end=end_date)
_sr = dow_df['Close']
dow_df = pd.DataFrame(_sr)
dow_df.rename(columns={'Close':ticker5}, inplace=True)
dow_df.head(3)

# ETF채권 데이터와 시장금리 데이터 상관관계 확인

# 해당 데이터프레임의 인덱스명 확인
etf_df.index.names
rate_df.index.names
nas_df.index.names
snp_df.index.names
dow_df.index.names

# 데이터 프레임 합치기
all_df = etf_df.join(rate_df, how='inner')
all_df = all_df.join(nas_df, how='inner')
all_df = all_df.join(snp_df, how='inner')
all_df = all_df.join(dow_df, how='inner')
all_df.head()

# 상관관계 출력
print(all_df.corr())

# 두 개의 데이터가 얼마나 유사한지 그래프로 표현
fs.draw_chart(all_df, left=ticker2, right=ticker3)

# 미국 공장 가동률 자료?
# yfinance에서 얻을 수 있는 자료들의 line up
# 즉 시장 금리는 가끔 폭삭 주저 앉아버릴때가 오는데 그 시점에 무슨 일이 있었길래 시장 금리가 훅 떨어졌는가를 알 필요가 있다.
# 시장금리의 형성 원인이 무엇인지 부터 시작해서 알아보아야 한다.

import matplotlib.pyplot as plt
plt.plot(etf_df['rsi'])
fs.rsi(etf_df, w=14)

fs.draw_chart(etf_df, left=ticker1, right='rsi')

etf_df.head()

fs.indicator_to_signal(etf_df, factor='rsi', buy=20, sell=70)
fs.position(etf_df)
fs.evaluate(etf_df, cost=0.01)
fs.performance(etf_df, rf_rate=0.1)

# 여기서 나온 RSI를 MA로 평탄화 시킨다면?

etf_df.head(3)
etf_df['rsi'].head(15)
_sr = etf_df['rsi']
_df = pd.DataFrame(_sr[13:])
_df['MA_3'] = _df['rsi'].rolling(window=3).mean()
_df['MA_20'] = _df['rsi'].rolling(window=20).mean()
_df['MA_30'] = _df['rsi'].rolling(window=30).mean()
_df['MA_40'] = _df['rsi'].rolling(window=40).mean()
_df
fs.draw_chart(_df, left=ticker1, right='MA_40')
etf_rsi_df = etf_df['rsi']

etf_df
MA_40 = _df['MA_40']
RSI = etf_df['rsi']
TMF = etf_df['TMF']
type(MA_40)

plt.plot(MA_40)
plt.plot(RSI)
plt.plot(TMF)
plt.show()


# 원래는 investpy가 되어야 하지만, 현재 상황에 따라서 되지 않고 있음
# github 공식 사이트를 통해서 다시 알려줄 것 같음
import investpy as ip
df = ip.get_stocks("south korea")
df.head()
df = ip.get_stock_historical_data(stock='066570',
                             country='south korea',
                             from_date='01/01/2022',
                             to_date='31/12/2022')

ip.stocks.get_stock_dividends('001770', 'south korea')

import telegram

TELEGRAM_TOKEN = #카카오톡 확인
CHAT_ID = #카카오톡 확인

bot = telegram.Bot(token=TELEGRAM_TOKEN)
updates = bot.getUpdates()

for update in updates:
    print(update.message)

import asyncio
async def main():
    token = TELEGRAM_TOKEN
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(CHAT_ID, '매수 타이밍 입니다.')

# --------
async def chat_id():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updates = await bot.getUpdates()
    print(updates)

asyncio.run(chat_id())
asyncio.run(main())
