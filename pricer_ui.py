# -*- coding: utf-8 -*-
"""
pricer_ui.py - Interface Streamlit du pricer
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Pricer import (
    black_scholes, monte_carlo, delta, gamma, vega, theta, rho,
    payoff_avec_prime, get_breakeven, plot_payoff, plot_comparaison, plot_greeks
)
from assets import ASSETS
from data_provider import get_all_prices
from book import OptionBook

st.set_page_config(page_title="Option Pricer", layout="wide")
st.title("Option Pricer - Black-Scholes & Monte Carlo")

# Initialiser le book en session_state
if 'book' not in st.session_state:
    st.session_state.book = OptionBook()

# Menu principal
st.sidebar.header("Menu Principal")
menu = st.sidebar.selectbox("Commande", ["PRICER", "BOOK", "PAYOFF GLOBAL", "DELETE"])

if menu == "PRICER":
    st.sidebar.header("Parametres")

    # Choisir l'actif
    actif = st.sidebar.selectbox("Actif", list(ASSETS.keys()))

    # Recuperer le prix spot reel
    try:
        prices = get_all_prices()
        S0 = prices[actif]
        st.sidebar.write(f"Prix spot reel : {S0:.2f}")
    except Exception:
        S0 = st.sidebar.slider("Prix actuel (S0)", 50, 200, 100)

    option_type = st.sidebar.selectbox("Type d'option", ["call", "put"])
    sens = st.sidebar.selectbox("Sens de la position", ["achat", "vente"])
    quantite = st.sidebar.number_input("Quantite", min_value=1, value=1)
    K = st.sidebar.slider("Strike (K)", 50, 200, 100)
    T = st.sidebar.slider("Maturite (ans)", 0.1, 5.0, 1.0)
    r = st.sidebar.slider("Taux sans risque (r)", 0.0, 0.1, 0.05)
    sigma = st.sidebar.slider("Volatilite (vol)", 0.05, 0.5, 0.20)
    q = st.sidebar.slider("Dividend Yield (q)", 0.0, 0.1, 0.0)
    N_paths = st.sidebar.number_input("Nombre de chemins MC", 1000, 100000, 10000)

    # PRICING
    prix_bs = black_scholes(S0, K, T, r, q, sigma, option_type)
    prix_mc, erreur = monte_carlo(S0, K, T, r, q, sigma, option_type, N_paths=N_paths, seed=2026)

    # AFFICHAGE
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prix BS", f"{prix_bs:.4f}")
    with col2:
        st.metric("Prix MC", f"{prix_mc:.4f} +- {erreur:.4f}")
    with col3:
        st.metric("Ecart", f"{abs(prix_bs - prix_mc):.4f}")

    # Graphs
    st.subheader("Greeks")
    plot_greeks(S0, K, T, r, q, sigma, option_type)
    st.pyplot(plt.gcf())

    st.subheader("Payoff")
    S_range = np.linspace(K * 0.7, K * 1.3, 100)
    payoffs = payoff_avec_prime(S_range, K, prix_bs, "acheteur", option_type)
    plot_payoff(S_range, payoffs, K, prix_bs, "acheteur", option_type)
    st.pyplot(plt.gcf())

    st.subheader("Comparaison BS vs MC")
    plot_comparaison(S0, K, T, r, q, sigma, option_type)
    st.pyplot(plt.gcf())

    # Ajouter au book
    if st.button("Ajouter au Book"):
        st.session_state.book.add_option({
            'sous_jacent': actif,
            'sens': sens,
            'type': option_type,
            'K': K,
            'T': T,
            'prix': prix_bs,
            'quantite': quantite,
        })
        st.success("Option ajoutee au Book")

elif menu == "BOOK":
    st.subheader("Portefeuille d'Options")

    if st.session_state.book.options.empty:
        st.warning("Book vide")
    else:
        st.dataframe(st.session_state.book.options)

        if st.button("Sauvegarder le Book"):
            st.session_state.book.save_to_csv()
            st.success("Book sauvegarde")

elif menu == "PAYOFF GLOBAL":
    if not st.session_state.book.options.empty:
        S_range = np.linspace(0, 200, 200)
        payoff = st.session_state.book.get_total_payoff(S_range)

        plt.figure(figsize=(10, 6))
        plt.plot(S_range, payoff, linewidth=2)
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.xlabel("Prix du sous-jacent")
        plt.ylabel("Payoff Global")
        plt.title("Payoff Global du Portefeuille")
        plt.grid(True, alpha=0.3)
        st.pyplot(plt.gcf())
    else:
        st.warning("Book vide")

elif menu == "DELETE":
    if not st.session_state.book.options.empty:
        index = st.number_input("Index a supprimer", min_value=0,
                                max_value=len(st.session_state.book.options) - 1, value=0)
        if st.button("Supprimer"):
            if st.session_state.book.remove_option(int(index)):
                st.success("Option supprimee")
            else:
                st.error("Index invalide")
    else:
        st.warning("Book vide")
