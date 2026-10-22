# -*- coding: utf-8 -*-
"""
book.py - Gestion du portefeuille d'options
"""

import os
import numpy as np
import pandas as pd

COLUMNS = ["sous_jacent", "sens", "type", "K", "T", "prix", "quantite"]
SIGNE = {"achat": 1, "vente": -1}


class OptionBook:
    def __init__(self, filename="option_book.csv"):
        self.filename = filename
        self.options = self.load_from_csv()

    def add_option(self, option_data):
        """Ajoute une option. option_data doit contenir toutes les COLUMNS."""
        for col in COLUMNS:
            if col not in option_data:
                raise ValueError("Colonne manquante : " + col)
        if option_data["sens"] not in SIGNE:
            raise ValueError("sens doit valoir 'achat' ou 'vente'")

        new_row = pd.DataFrame([option_data])[COLUMNS]
        self.options = pd.concat([self.options, new_row], ignore_index=True)
        self.options = self.options.sort_values("T").reset_index(drop=True)
        print("Option ajoutee : " + str(option_data["sous_jacent"]))

    def remove_option(self, index):
        """Supprime une option par index. Renvoie True si la suppression a eu lieu."""
        if 0 <= index < len(self.options):
            self.options = self.options.drop(index).reset_index(drop=True)
            return True
        return False

    def save_to_csv(self):
        """Sauvegarde le book en CSV"""
        self.options.to_csv(self.filename, index=False)
        print("Book sauvegarde : " + self.filename)

    def load_from_csv(self):
        """Charge le book depuis CSV, ou un book vide si le fichier est absent ou incompatible"""
        if not os.path.exists(self.filename):
            return pd.DataFrame(columns=COLUMNS)
        df = pd.read_csv(self.filename)
        if list(df.columns) != COLUMNS:
            print("Fichier CSV incompatible, book reinitialise")
            return pd.DataFrame(columns=COLUMNS)
        return df

    def get_total_payoff(self, S_range):
        """Payoff global net de primes, signe selon achat ou vente"""
        S_range = np.asarray(S_range, dtype=float)
        total = np.zeros(len(S_range))
        for _, row in self.options.iterrows():
            if row["type"] == "call":
                intrinseque = np.maximum(S_range - row["K"], 0)
            else:
                intrinseque = np.maximum(row["K"] - S_range, 0)
            signe = SIGNE[row["sens"]]
            total += signe * (intrinseque - row["prix"]) * row["quantite"]
        return total
