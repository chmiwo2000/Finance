# 한국은행 자료 받아오는 구간임
import pandas as pd
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import requests

key = "5H6P7H8QSOH3MNPO08UZ"
n = '100000'
date1 = '20100101'
date2 = '20230119'


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




# # 이제 위의 정의된 함수에 따라서 받아올 수 있는 값들을 정의한 자료 더미들을 만든다.
# # 연간으로 조회할 지표
# combination_ECOS = [['817Y002', 'D', '010190000', '']]


# # 위에서 검색한 리턴된 데이터 값을 다시 받아서 '엑셀'로 저장을 하기 위한 코드
# df_ecos_a = pd.DataFrame()
# df_ecos_a.to_excel('C:/Users/chmiw/Desktop/Programming/Finance/ECOS.xlsx', sheet_name='Sheet0')
# a = 1
#
# for i in combination_ECOS:
#     data = get_ECOS(key, n, date1, date2, i[0], i[1], i[2], i[3])
#     data["값"] = pd.to_numeric(data['값'])
#     df_ecos_a = df_ecos_a.append(data, ignore_index=True)
#     with pd.ExcelWriter('C:/Users/chmiw/Desktop/Programming/Finance/ECOS.xlsx', mode = 'a') as writer:
#         data.to_excel(writer, sheet_name=f'Sheet{a}')
#     a = a + 1
# print(df_ecos_a)


# # for문에서 오류가 날 경우를 대비한 검증용
# j = combination_ECOS[0]
# test_url = f"http://ecos.bok.or.kr/api/StatisticSearch/{key}/xml/kr/1/{n}/{j[0]}/{j[1]}/{date1}/{date2}/{j[2]}/{j[3]}"
# print(test_url)
# # 해당 URL을 클릭해서 정상적으로 페이지가 이동되는지 확인
# # 정상적으로 이동되었다면, 컬럼이 맞는지 확인하기 위해서 조작
# test_data = get_ECOS(key, n, date1, date2, j[0], j[1], j[2], j[3])
# test_data.head()

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

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

period = ['국고채(1년)', '국고채(2년)', '국고채(3년)', '국고채(5년)', '국고채(10년)']


y1 = rate_data[rate_data['세부항목명'] == '국고채(1년)'][['기간', '세부항목명', '값']]
y2 = rate_data[rate_data['세부항목명'] == '국고채(2년)'][['기간', '세부항목명', '값']]
y3 = rate_data[rate_data['세부항목명'] == '국고채(3년)'][['기간', '세부항목명', '값']]
y5 = rate_data[rate_data['세부항목명'] == '국고채(5년)'][['기간', '세부항목명', '값']]
y10 = rate_data[rate_data['세부항목명'] == '국고채(10년)'][['기간', '세부항목명', '값']]


y1.set_index(y1['기간'], append=False, inplace=True)
y2.set_index(y2['기간'], append=False, inplace=True)
y3.set_index(y3['기간'], append=False, inplace=True)
y5.set_index(y5['기간'], append=False, inplace=True)
y10.set_index(y10['기간'], append=False, inplace=True)

y1.drop('기간', axis=1, inplace=True)
y2.drop('기간', axis=1, inplace=True)
y3.drop('기간', axis=1, inplace=True)
y5.drop('기간', axis=1, inplace=True)
y10.drop('기간', axis=1, inplace=True)

y1.columns = ['세부항목명', period[0]+' 값']
y2.columns = ['세부항목명', period[1]+' 값']
y3.columns = ['세부항목명', period[2]+' 값']
y5.columns = ['세부항목명', period[3]+' 값']
y10.columns = ['세부항목명', period[4]+' 값']

y1.drop('세부항목명', axis=1, inplace=True)
y2.drop('세부항목명', axis=1, inplace=True)
y3.drop('세부항목명', axis=1, inplace=True)
y5.drop('세부항목명', axis=1, inplace=True)
y10.drop('세부항목명', axis=1, inplace=True)


y1 = y1.join(y2, how='left')
y1 = y1.join(y3, how='left')
y1 = y1.join(y5, how='left')
y1 = y1.join(y10, how='left')

y1.reset_index(inplace=True)


x1 = y1['기간'].to_list()
y1 = y1['국고채(1년) 값'].to_list()
print(type(x1))
print(type(y1))

# 각 데이터의 크기를 맞춰야 한다. 특히 길이 부분
len(x1)
len(y1)
len(y3)
len(y5)
len(y10)

plt.plot(x1, y1, label = '1year')
plt.plot(x1, y3, label = '3year')
plt.plot(x1, y5, label = '5year')
# plt.plot(x1, y10, label = '10year')
plt.xticks(ticks=x1, labels=x1, rotation=45)
plt.xlabel('DATE')
plt.ylabel('PERCENT')
plt.locator_params(axis='x', nbins=len(x1)/100)
plt.legend(loc='best', ncol=5)
plt.show()


plt.plot(y1.index, y1['국고채(1년) 값'])
plt.plot(y1.index, y1['국고채(2년) 값'])
plt.plot(y1.index, y1['국고채(3년) 값'])
plt.plot(y1.index, y1['국고채(5년) 값'])
plt.plot(y1.index, y1['국고채(10년) 값'])
plt.show()

# 필요한 라이브러리 로드
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs
import matplotlib.pyplot as plt
import openpyxl

# 시작날짜 및 종료일자 설정
start_date = '2010-10-31'
end_date = '2023-03-06'

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
all_df.corr()
all_df.corr().unstack()
s = all_df.corr().unstack()
all_df.corr().nlargest(1, 'TMF')


# 모든 종목에 대해서 상관관계를 파악하기 위해 데이터 프레임을 뽑고 거기에서 상관계수가 0.7 OR -0.7 이상 수준을 뽑아내기
# True 값을 행렬을 가져올 수는 없나?

# 추출된 상관관계에서 특정 수준 이상의 값을 추려서 result리스트에 append한 값을 출력
# 각 종목에 대한 주가를 기준으로 돌아가면서 상관관계를 나열해주는 함수
corr_df = all_df.corr()
corr_df



result = []
for i in range(0, 40, 1):
    tmp1 = corr_df.iloc[i][(corr_df.iloc[i] < -0.4) & (corr_df.iloc[i] > -0.6)]
    for j in range(0, tmp1.shape[0]):
        num1 = tmp1[j]
        tmpp = tmp1.index[j]
        result.append([tmpp] + [corr_df.index[i]] + [num1])
    tmp2 = corr_df.iloc[i][(corr_df.iloc[i] > 0.70) & (corr_df.iloc[i] < 0.9)]
    for k in range(0, tmp2.shape[0]):
        num2 = tmp2[k]
        tmpp2 = tmp2.index[k]
        result.append([tmpp2] + [corr_df.index[i]] + [num2])
result

del_result = []
for i in range(0, len(result)):
    if result[i][2] == 1.0:
        del_result.append(result[i])
    else:
        pass
del_result

fin_result = []
for i in range(0, len(result)):
    if result[i] in del_result:
        pass
    else:
        fin_result.append(result[i])

a = list(map(str, fin_result[0]))
a.sort()



fin_result_sorted = []
for i in range(0, len(fin_result)):
    fin_result_sorted.append(list(map(str, fin_result[i])))


for i in range(0, len(fin_result_sorted)):
    fin_result_sorted[i].sort()

sii = []
for value in fin_result_sorted:
    if value not in sii:
        sii.append(value)

sii_df = pd.DataFrame(sii)
sii_df.to_excel('sii.xlsx')
# 최종적으로 이렇게 나오게 됨
# [['-0.9534323539983318', 'TMF', '^TYX'], ['0.9913533386317084', '^DJI', '^GSPC'], ['0.9734604159581298', '^DJI', '^IXIC'], ['0.989413290264967', '^GSPC', '^IXIC']]


# 한국 주식을 가져오는데, 필요한 라이브러리를 설치하고 실행하기
import FinanceDataReader as fdr
from pykrx import stock
import pandas_datareader.data as pdr
import yfinance as yf
import pandas as pd

stocks = fdr.StockListing('KRX')
stocks.head(5)
stocks['Code'][0]

start_date = '2018-01-01'
end_date = '2023-03-06'

df_fdr = fdr.DataReader('005930', start=start_date, end=end_date)
df_fdr['Code']

ticker6 = stocks['Symbol'][0]
name6 = stocks['Name'][0]
test6_df = fdr.DataReader(ticker6, start=start_date, end=end_date)
_sr = test6_df['Close']
test6_df = pd.DataFrame(_sr)
test6_df.rename(columns={'Close':name6}, inplace=True)
test6_df.head(3)

ticker7 = stocks['Symbol'][1]
name7 = stocks['Name'][1]
test7_df = fdr.DataReader(ticker7, start=start_date, end=end_date)
_sr = test7_df['Close']
test7_df = pd.DataFrame(_sr)
test7_df.rename(columns={'Close':name7}, inplace=True)
test7_df.head(3)

ticker8 = stocks['Code'][2]
name8 = stocks['Name'][2]
test8_df = fdr.DataReader(ticker8, start=start_date, end=end_date)
_sr = test8_df['Close']
test8_df = pd.DataFrame(_sr)
test8_df.rename(columns={'Close':name8}, inplace=True)
test8_df.head(3)

ticker9 = stocks['Code'][3]
name9 = stocks['Name'][3]
test9_df = fdr.DataReader(ticker9, start=start_date, end=end_date)
_sr = test9_df['Close']
test9_df = pd.DataFrame(_sr)
test9_df.rename(columns={'Close':name9}, inplace=True)
test9_df.head(3)

ticker10 = stocks['Code'][4]
name10 = stocks['Name'][4]
test10_df = fdr.DataReader(ticker10, start=start_date, end=end_date)
_sr = test10_df['Close']
test10_df = pd.DataFrame(_sr)
test10_df.rename(columns={'Close':name10}, inplace=True)
test10_df.head(3)

all_df = test6_df.join(test7_df, how='inner')
all_df = all_df.join(test8_df, how='inner')
all_df = all_df.join(test9_df, how='inner')
all_df = all_df.join(test10_df, how='inner')
all_df.head()

all_df.corr()


# for문으로 구하는 함수 작성
# ETF자료 뽑기만 하면 될 것 같다. ETF로 해보자

stocks = fdr.StockListing('ETF/KR')
stocks.head(5)
stocks['Symbol'][0]


start_date = '2020-01-01'
end_date = '2023-02-04'
all_df = []


for i in range(0, len(stocks), 1):
    if i == 0:
        ticker = stocks['Symbol'][i]
        name = stocks['Name'][i]
        _df = fdr.DataReader(ticker, start=start_date, end=end_date)
        _sr = _df['Close']
        _df = pd.DataFrame(_sr)
        _df.rename(columns={'Close':name}, inplace=True)
    elif i == 1:
        ticker = stocks['Symbol'][i]
        name = stocks['Name'][i]
        t_df = fdr.DataReader(ticker, start=start_date, end=end_date)
        t_sr = t_df['Close']
        t_df = pd.DataFrame(t_sr)
        t_df.rename(columns={'Close':name}, inplace=True)
        all_df = _df.join(t_df, how = 'inner')
    else:
        ticker = stocks['Symbol'][i]
        name = stocks['Name'][i]
        te_df = fdr.DataReader(ticker, start=start_date, end=end_date)
        te_sr = te_df['Close']
        te_df = pd.DataFrame(te_sr)
        te_df.rename(columns={'Close':name}, inplace=True)
        if te_df.empty == True:
            pass
        else:
            all_df = all_df.join(te_df, how = 'outer')

all_df.dropna(axis=1, inplace=True)

all_df
all_df.corr()

# ETF 자료를 뽑는 방법 / 네이버 api 활용
import requests
import json
from pandas import json_normalize

url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
json_data = json.loads(requests.get(url).text)
df = json_normalize(json_data['result']['etfItemList'])
df
stocks = df.iloc[:, [0, 2]]
stocks.rename(columns={'itemcode':'Symbol', 'itemname':'Name'}, inplace=True)
stocks



fdr.DataReader('287320', start=start_date, end=end_date)
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