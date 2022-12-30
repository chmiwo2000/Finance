# 필요한 라이브러리 로드
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs

# 시작날짜 및 종료일자 설정
start_date = '2019-01-01'
end_date = '2022-12-24'

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

# ETF채권 데이터와 시장금리 데이터 상관관계 확인

# 해당 데이터프레임의 인덱스명 확인
etf_df.index.names
rate_df.index.names
# 데이터 프레임 합치기
all_df = etf_df.join(rate_df, how='inner')
# 상관관계 출력
print(all_df.corr())

# 두 개의 데이터가 얼마나 유사한지 그래프로 표현
fs.draw_chart(all_df, left=ticker1, right=ticker2)

# 미국 공장 가동률 자료?
# yfinance에서 얻을 수 있는 자료들의 line up