# 필요한 라이브러리 로드
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs

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

fs.draw_chart(etf_df, left=ticker1, right='rsi')

fs.rsi(etf_df, w=14)

fs.indicator_to_signal(etf_df, factor='rsi', buy=20, sell=70)
fs.position(etf_df)
fs.evaluate(etf_df, cost=0.01)
fs.performance(etf_df, rf_rate=0.1)