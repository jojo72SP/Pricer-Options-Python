# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm # pour distributon normale

#on commence par le market data

def get_market_data():
    return {
        'S0': 100,
        'K': 100,
        'T': 1,
        'r': 0.05,
        'q': 0,
        'sigma': 0.2
        }

#On price nos fonctions

def payoff(S, K, option_type):
    if option_type == "call":
        return max(S - K, 0)
    elif option_type == "put":
        return max(K - S, 0)

def normal_cdf(x):
    return norm.cdf(x)  #ditribution normale cumulative qui nous permet de savoir la proba qu'une valeur soit inférieure ou égale à x

#Black-Scholes

def black_scholes(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S/K) + (r - q + sigma**2/2) * T) / (sigma * np.sqrt(T)) # np.sqrt(T)) = Racine carré de T
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * np.exp(-q*T) * normal_cdf(d1) - K * np.exp(-r*T) * normal_cdf(d2)
    elif option_type == "put":
        return K * np.exp(-r*T) * normal_cdf(-d2) - S * np.exp(-q*T) * normal_cdf(-d1)

#monte carlo

def monte_carlo(S0, K, T, r, q, sigma, option_type, N_paths=10000, seed=2026):
    Z = norm.rvs(size=N_paths, random_state=seed)
    
    S_T = S0 * np.exp((r - q - sigma**2/2) * T + sigma * np.sqrt(T) * Z)
    
    payoffs = []
    for S in S_T:
        payoffs.append(payoff(S, K, option_type))
    discounted = np.array(payoffs) * np.exp(-r*T)
    
    prix = np.mean(discounted)
    erreur = np.std(discounted, ddof=1) / np.sqrt(N_paths)
    
    return prix, erreur

def longstaff_schwartz(S0, K, T, r, q, sigma, option_type, N_paths=10000, N_steps=50):
    dt = T / N_steps
    rng = np.random.default_rng(seed=2026)
    
    paths = np.empty((N_paths, N_steps + 1))
    paths[:, 0] = S0
    
    for t in range(1, N_steps + 1):
        z = rng.standard_normal(N_paths)
        paths[:, t] = paths[:, t-1] * np.exp(
            (r - q - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
    if option_type =="call":
        exercise_value = np.maximum(paths - K, 0)
    else:
        exercise_value = np.maximum(K - paths, 0)
        
    cashflow = exercise_value[:, -1].copy()
    
    for t in range(N_steps - 1, 0, -1):
        cashflow *= np.exp(-r*dt)
        
        possible = exercise_value[:, t] > 0
        
        if possible.sum() < 5:
            continue
        stock = paths[possible, T]
        future_value = cashflow[possible]
        
        x = stock / K
        
        A = np.column_stack((
            np.ones(len(x)), x, x**2, x**3))
        
        coefficients = np.linalg.lstsq(A, future_value, rcond=None)[0]
        
        continuation = A @ coefficients
        
        immediate = exercise_value[possible, t]
        
        should_exercise = immediate > continuation
        
        indices = np.where(possible)[0]
        cashflow[indices[should_exercise]] = immediate[should_exercise]
        
    prix = np.mean(cashflow * np.exp(-r*dt))
    
    return prix
#Grecs

def delta(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S/K) + (r - q + sigma**2/2) * T) / (sigma * np.sqrt(T))
    if option_type =="call":
        return np.exp(-q*T) * normal_cdf(d1)
    else:
        return -np.exp(-q*T) * normal_cdf(-d1)

def gamma(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S/K) + (r - q + sigma**2/2) * T) / (sigma * np.sqrt(T))
    return np.exp(-q*T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))

def vega(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S/K) + (r - q + sigma**2/2) * T) / (sigma * np.sqrt(T))
    return S * np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T)

def theta(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S/K) + (r - q + sigma**2/2) * T) / (sigma * np.sqrt(T))
    d2 = d1- sigma*np.sqrt(T)
    
    if option_type == "call":
        return (-S*np.exp(-q*T)*norm.pdf(d1)*sigma/(2*np.sqrt(T))
                - r*K*np.exp(-r*T)*normal_cdf(d2)
                + q*S*np.exp(-q*T)*normal_cdf(d1))
    else:  # put
        return (-S*np.exp(-q*T)*norm.pdf(d1)*sigma/(2*np.sqrt(T))
                + r*K*np.exp(-r*T)*normal_cdf(-d2)
                - q*S*np.exp(-q*T)*normal_cdf(-d1))
    
def rho(S, K, T, r, q, sigma, option_type):
    d2 = (np.log(S/K) + (r - q + sigma**2/2)*T) / (sigma*np.sqrt(T)) - sigma*np.sqrt(T)
    if option_type =="call":
        return K * T * np.exp(-r*T) * normal_cdf(d2)
    else:
        return -K * T * np.exp(-r*T) * normal_cdf(-d2)
    
def plot_greeks(S0, K, T, r, q, sigma, option_type):
    S_range = np.linspace(K * 0.7, K * 1.3, 100)
    
    deltas = [delta(S, K, T, r, q, sigma, option_type) for S in S_range]
    gammas = [gamma(S, K, T, r, q, sigma, option_type) for S in S_range]
    vegas = [vega(S, K, T, r, q, sigma, option_type) for S in S_range]
    thetas = [theta(S, K, T, r, q, sigma, option_type) for S in S_range]
    rhos = [rho(S, K, T, r, q, sigma, option_type) for S in S_range]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    #Delta
    axes[0, 0].plot(S_range, deltas, color="blue", linewidth=2)
    axes[0, 0].set_title("Delta", fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel("Prix de sous-jacent")
    axes[0, 0].grid(alpha=0.3)
    
    #Gamma
    axes[0, 1].plot(S_range, gammas, color="green", linewidth=2)
    axes[0, 1].set_title("Gamma", fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel("Prix de sous-jacent")
    axes[0, 1].grid(alpha=0.3)
    
    #Vega
    axes[0, 2].plot(S_range, vegas, color="red", linewidth=2)
    axes[0, 2].set_title("Vega", fontsize=12, fontweight='bold')
    axes[0, 2].set_xlabel("Prix de sous-jacent")
    axes[0, 2].grid(alpha=0.3)
    
    #Theta
    axes[1, 0].plot(S_range, thetas, color="orange", linewidth=2)
    axes[1, 0].set_title("Theta", fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel("Prix du sous-jacent")
    axes[1, 0].grid(alpha=0.3)
    
    #Rho
    axes[1, 1].plot(S_range, rhos, color="purple", linewidth=2)
    axes[1, 1].set_title("Rho", fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel("Prix du sous-jacent")
    axes[1, 1].grid(alpha=0.3)
    
    axes[1, 2].axis('off')
    info_text = f"""
    Greeks au prix actuel S0={S0}:
        
    Delta = {delta(S0, K, T, r, q, sigma, option_type):.4f}
    Gamma = {gamma(S0, K, T, r, q, sigma, option_type):.4f}
    Vega = {vega(S0, K, T, r, q, sigma, option_type):.4f}
    Rho = {rho(S0, K, T, r, q, sigma, option_type):.4f}
    """
    axes[1, 2].text(0.1, 0.5, info_text, fontsize=10, family='monospace',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    plt.show()
    

#Ensuite le payoff

def payoff_avec_prime(S_range, K, prime, option_side, option_type):
    payoffs = []
    
    for S in S_range:
        if option_type == "call":
            payoff_intr = max(S - K, 0)
        else:
            payoff_intr = max(K - S, 0)
            
        #payoff avec la prime maintenant
        if option_side == "acheteur":
            payoff = payoff_intr - prime
        else: payoff = -payoff_intr + prime
        
        payoffs.append(payoff)
    return np.array(payoffs)

def get_breakeven(K, prime, option_side, option_type):
    if option_type == "call":
        if option_side == "acheteur":
            return K + prime
        else:
            return K + prime
    else:
        if option_side == "acheteur":
            return K - prime
        else:
            return K - prime
        
        
def plot_payoff(S_range, payoffs, K, prime, option_side, option_type):
    breakeven = get_breakeven(K, prime, option_side, option_type)
    
    #Profit net (payoof-prime)
    payoff_intrinsic = np.array([max(S - K, 0) if option_type == "call" else max (K-S, 0)
                             for S in S_range])

    profit_net = payoff_intrinsic - prime

    #Graph du payoff instrinsèque
    
    plt.plot(S_range, payoff_intrinsic, label="Payoff", color="blue", linewidth=2)

    #Graph profit net
    plt.plot(S_range, profit_net, label="Profit net", color="green", linewidth=2, linestyle="--")
    plt.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    plt.axvline(x=K, color="gray", linestyle=":", alpha=0.5, label="Strike")
    plt.axvline(x=breakeven, color="red", linestyle="--", linewidth=2, label=f"Breakeven ({breakeven:.2f})")
    plt.scatter(breakeven, 0, color="red", zorder=5, s=100)
    plt.xlabel("Prix du sous-jacent à maturité (S_T")
    plt.ylabel("Payoff / Profit")
    plt.title(f"Payoff {option_side.upper()} {option_type.upper()} - Strike = {K}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(S_range, payoffs, label="Payoff", color="blue", linewidth=2)
    plt.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    plt.axvline(x=K, color="gray", linestyle="--", alpha=0.5, label="Strike")
    plt.axvline(x=breakeven, color="red", linestyle="--", linewidth=2, label=f"Breakeven ({breakeven:.2f})")
    
    plt.xlabel("Prix du sous-jacent à maturité (S_T)")
    plt.ylabel("Payoff")
    plt.title(f"Payoff {option_side.upper()} {option_type.upper()} - Strike = {K}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
def plot_comparaison(S0, K, T, r, q, sigma, option_type):
    strikes = np.linspace(80, 120, 15)
    prix_bs_list = []
    prix_mc_list = []
    
    for strike in strikes:
        prix_bs_list.append(black_scholes(S0, strike, T, r, q, sigma, option_type))
        prix_mc_list.append(monte_carlo(S0, strike, T, r, q, sigma, option_type, N_paths=5000))
        
    plt.figure(figsize=(10, 6))
    plt.plot(strikes, prix_bs_list, label="Black-Scholes", color="blue", linewidth=2)
    plt.plot(strikes, prix_mc_list, label="Monte Carlo", color="red", linestyle="--", linewidth=2)
    plt.xlabel("Strike")
    plt.ylabel("Prix du CALL")
    plt.title("Comparaisaon BS vs MC")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
def main():
    data = get_market_data()
    S0, K, T, r, q, sigma = data['S0'], data['K'], data['T'], data['r'], data['q'], data['sigma']
    
    option_type = "call"
    
    data = get_market_data()
    S0, K, T, r, q, sigma = data['S0'], data['K'], data['T'], data['r'], data['q'], data['sigma']
    
    prix_bs = black_scholes(S0, K, T, r, q, sigma, option_type)
    prix_mc, erreur = monte_carlo(S0, K, T, r, q, sigma, option_type, N_paths=10000)
    prix_ls = longstaff_schwartz(S0, K, T, r, q, sigma, option_type, N_paths=30000, N_steps=252)
    
    print("\n" + "="*50)
    print("    PRICER D'OPTIONS")
    print("="*50)
    print(f"Prix Monte Carlo: {prix_mc:.4f} +- {erreur:.4f}")
    print(f"Prix Black-Scholes : {prix_bs:.4f}")   
    print(f"Prix Logngstaff_Sch : {prix_ls:.4f}")
    print("="*50 + "\n")
    
    plot_greeks(S0, K, T, r, q, sigma, "call")
    
    S_range = np.linspace(K * 0.7, K * 1.3, 100)
    payoffs = payoff_avec_prime(S_range, K, prix_bs, "acheteur", "call")
    
    #Graphs
    plot_greeks(S0, K, T, r, q, sigma, option_type)
    plot_payoff(S_range, payoffs, K, prix_bs, "acheteur", option_type)
    plot_comparaison(S0, K, T, r, q, sigma, option_type)
    
if __name__ == "__main__":
    main()

