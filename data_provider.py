# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:43:26 2026

@author: willi
"""

import yfinance as yf
from assets import ASSETS

def get_spot_price(ticker):
    #récupération du prix spot réel
    data = yf.Ticker(ticker)
    price = data.info.get('currentPrice')
    return price

def get_all_prices():
    #récupération des prix du dictionnaire
    prices = {}
    for key, asset in ASSETS.items():
        prices[key] = get_spot_price(asset['ticker'])
    return prices
