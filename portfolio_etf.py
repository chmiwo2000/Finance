# 한국 주식을 가져오는데, 필요한 라이브러리를 설치하고 실행하기
import FinanceDataReader as fdr
from pykrx import stock
import pandas_datareader.data as pdr
import yfinance as yf
import pandas as pd


# 한국 시장에 등록된 ETF 자료 추출
stocks = fdr.StockListing('ETF/KR')
stocks.head(5)

# 정상적으로 추출되었는지 확인
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

# 각 종목에 대한 주가를 기준으로 돌아가면서 상관관계를 나열해주는 함수
corr_df = all_df.corr()
len(corr_df)

# 추출된 상관관계에 대해서 정해진 범위 내에서 추출하게 만드는 함수
result = []
for i in range(0, len(corr_df), 1):
    tmp1 = corr_df.iloc[i][(corr_df.iloc[i] < -0.5) & (corr_df.iloc[i] > -0.6)]
    for j in range(0, tmp1.shape[0]):
        num1 = tmp1[j]
        tmpp = tmp1.index[j]
        result.append([tmpp] + [corr_df.index[i]] + [num1])
    tmp2 = corr_df.iloc[i][(corr_df.iloc[i] > 0.2) & (corr_df.iloc[i] < 0.5)]
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