# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 16:43:26 2026

@author: willi
"""

import yfinance as yf
from assets import ASSETS


def get_spot_price(ticker):
    # Dernier cours du ticker.
    # currentPrice n'existe pas pour les indices (^GDAXI) ni les matieres premieres (BZ=F, GC=F),
    # donc on utilise fast_info, puis l'historique en secours.
    data = yf.Ticker(ticker)
    price = None
    try:
        price = data.fast_info['last_price']
    except Exception:
        price = None

    if price is None or price != price:  # price != price detecte un NaN
        try:
            hist = data.history(period="5d")
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
        except Exception:
            price = None

    if price is None:
        return None
    return float(price)


def get_all_prices():
    # Cours de tous les actifs du dictionnaire
    prices = {}
    for key, asset in ASSETS.items():
        prices[key] = get_spot_price(asset['ticker'])
    return prices
