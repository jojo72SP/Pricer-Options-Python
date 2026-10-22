# -*- coding: utf-8 -*-
"""
book.py - Gestion du portefeuille d'options
"""

import pandas as pd
import os
import numpy as np

class OptionBook:
    def __init__(self, filename='option_book.csv'):
        self.filename = filename
        self.options = self.load_from_csv() if os.path.exists(filename) else pd.DataFrame()
    
    def add_option(self, option_data):
        """Ajoute une option au book"""
        new_row = pd.DataFrame([option_data])
        self.options = pd.concat([self.options, new_row], ignore_index=True)
        print(f"Option ajoutee : {option_data['sous_jacent']}")
    
    def remove_option(self, index):
        """Supprime une option par index"""
        if index < len(self.options):
            self.options = self.options.drop(index).reset_index(drop=True)
            print(f"Option {index} supprimee")
        else:
            print("Index invalide")
    
    def display_book(self):
        """Affiche le book"""
        if self.options.empty:
            print("Book vide")
            return None
        else:
            print(self.options.to_string(index=True))  # Console
            return self.options  # Streamlit
    
    def save_to_csv(self):
        """Sauvegarde le book en CSV"""
        self.options.to_csv(self.filename, index=False)
        print(f"Book sauvegarde : {self.filename}")
    
    def load_from_csv(self):
        """Charge le book depuis CSV"""
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        return pd.DataFrame()
    
    def get_total_payoff(self, S_range):
        """Calcule le payoff global du portefeuille"""
        payoff_total = [0] * len(S_range)
        for idx, row in self.options.iterrows():
            for i, S in enumerate(S_range):
                if row['type'] == 'call':
                    payoff = max(S - row['K'], 0)
                else:
                    payoff = max(row['K'] - S, 0)
                payoff_total[i] += (payoff - row['prix']) * row['quantite']
        return payoff_total


# ===== UTILISATION =====
if __name__ == "__main__":
    book = OptionBook()
    book.add_option({'sous_jacent': 'DAX', 'type': 'call', 'K': 100, 'prix': 10, 'quantité': 1})
    book.display_book()
    book.save_to_csv()
    
    S_range = np.linspace(80, 120, 100)
    payoff = book.get_total_payoff(S_range)