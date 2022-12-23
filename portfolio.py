import pandas_datareader as pdr
import pandas as pd
import yfinance as yf
import numpy as np
import finterstellar as fs

ticker1 = 'TMF'
etf_df = yf.download(ticker1, start='2020-01-01', end='2022-12-18')
_sr = etf_df['Close']
etf_df = pd.DataFrame(_sr)
etf_df.rename(columns={'Close':ticker1}, inplace=True)
etf_df.head(3)


ticker2 = '^TYX'
rate_df = yf.download(ticker2, start='2020-01-01', end='2022-12-18')
_sr = rate_df['Close']
rate_df = pd.DataFrame(_sr)
rate_df.rename(columns={'Close':ticker2}, inplace=True)
rate_df.head(3)