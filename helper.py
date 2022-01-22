import re
from bs4 import BeautifulSoup
import requests
import dataframe_image as dfi
import pandas as pd
from settings import config
from datetime import datetime
import pytz


# tickers = ['BABA', 'FB', 'NIO', 'PLTR', 'ALPP', 'CRSP', 'FCEL', 'IDEX', 'SKLZ']
# tickers = ['BABA', 'FB']


def download_tickers_data(tickers):
    dict_df = {ticker: None for ticker in tickers}
    for ticker in tickers:
        page = requests.get(config.url_yahoo + ticker, headers=config.headers_yahoo)
        soup = BeautifulSoup(page.text, 'lxml')
        last = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
        change = soup.find('fin-streamer',
                           {'class': 'Fw(500) Pstart(8px) Fz(24px)', 'data-field': 'regularMarketChange'}).text
        pct_change = soup.find('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)',
                                                'data-field': 'regularMarketChangePercent'}).text
        pct_change = re.sub('[()%]', '', pct_change)
        dict_df[ticker] = [last, change, pct_change]

    df = pd.DataFrame(dict_df, index=['Last', 'Change', 'Change, %']).T
    df['temp'] = pd.to_numeric(df['Change, %'])
    df = df.sort_values(by='temp', ascending=False).drop(columns=['temp'])
    df = df.style.applymap(
        lambda x: 'color: red' if x[0] == '-' else (
            'color: green' if x[0] == '+' else (
                'color: grey' if x[0] == '0' else 'color: black')))
    # df = df.style.applymap(pick_color)
    dfi.export(df, 'test.png')


def download_premarket_data(tickers):
    dict_df = {ticker: None for ticker in tickers}
    for ticker in tickers:
        try:
            page = requests.get(config.url_yahoo + ticker, headers=config.headers_yahoo)
            soup = BeautifulSoup(page.text, 'lxml')
            last = soup.find('fin-streamer', {'data-field': 'preMarketPrice'}).text
            change = soup.find('fin-streamer', {'class': 'Mstart(4px) D(ib) Fz(24px)'}).text
            pct_change = soup.find('fin-streamer', {'class': 'Mstart(4px) D(ib) Fz(24px)',
                                                    'data-field': 'preMarketChangePercent'}).text
            pct_change = re.sub('[()%]', '', pct_change)
            dict_df[ticker] = [last, change, pct_change]
        except Exception as e:
            print(ticker, e)
    df = pd.DataFrame(dict_df, index=['Last', 'Change', 'Change, %']).T
    df['temp'] = pd.to_numeric(df['Change, %'])
    df = df.sort_values(by='temp', ascending=False).drop(columns=['temp'])
    df = df.dropna()
    df = df.style.applymap(
        lambda x: 'color: red' if x[0] == '-' else (
            'color: green' if x[0] == '+' else (
                'color: grey' if x[0] == '0' else 'color: black')))
    # df = df.style.applymap(pick_color)
    dfi.export(df, 'test.png')


def download_after_hours_data(tickers):
    dict_df = {ticker: None for ticker in tickers}
    for ticker in tickers:
        page = requests.get(config.url_yahoo + ticker, headers=config.headers_yahoo)
        soup = BeautifulSoup(page.text, 'lxml')
        last = soup.find('fin-streamer', {'data-field': 'postMarketPrice'}).text
        change = soup.find('fin-streamer', {'data-field': 'postMarketChange'}).text
        pct_change = soup.find('fin-streamer', {'data-field': 'postMarketChangePercent'}).text
        pct_change = re.sub('[()%]', '', pct_change)
        dict_df[ticker] = [last, change, pct_change]
    df = pd.DataFrame(dict_df, index=['Last', 'Change', 'Change, %']).T
    df['temp'] = pd.to_numeric(df['Change, %'])
    df = df.sort_values(by='temp', ascending=False).drop(columns=['temp'])
    df = df.style.applymap(
        lambda x: 'color: red' if x[0] == '-' else (
            'color: green' if x[0] == '+' else (
                'color: grey' if x[0] == '0' else 'color: black')))
    # df = df.style.applymap(pick_color)
    dfi.export(df, 'test.png')


def download_ticker_stats(ticker):
    data = {}
    page = requests.get(config.url_yahoo_analysis + ticker, headers=config.headers_yahoo)
    # print(config.url_yahoo_analysis + ticker)
    soup = BeautifulSoup(page.text, 'lxml')
    # print(soup)
    # rating = soup.find_all('div', {'class': 'Pos(r) T(5px) Miw(100px) Fz(s) Fw(500) D(ib) C($primaryColor)Ta(c) Translate3d($half3dTranslate)'})
    rating = soup.find('financialData', {'profitMargins': 'raw'})
    return rating


def market_time():
    markets = ['nyse', 'nasdaq', 'otc']
    dt_ny = str(datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M'))
    session = requests.Session()
    r = session.get(config.url_polygon + 'marketstatus/now', headers=config.headers_polygon).json()
    result = f'{dt_ny}, market: {r["market"]}\n'
    for market in markets:
        result += f'\t{market.title()}: {r["exchanges"][market].title()}\n'
    return result
