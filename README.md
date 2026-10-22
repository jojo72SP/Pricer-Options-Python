# Pricer d'options - Black-Scholes, Monte Carlo, grecs et book

Pricer d'options europeennes sur plusieurs sous-jacents (actions, indice, matieres premieres),
avec calcul des grecs, graphique de payoff, comparaison Black-Scholes / Monte Carlo,
et gestion d'un portefeuille (book) avec payoff global.

Le guide de presentation, ecran par ecran, est dans [presentation/SCRIPT_PRESENTATION.md](presentation/SCRIPT_PRESENTATION.md).

## Structure

| Fichier | Role |
| --- | --- |
| Pricer.py | Black-Scholes, Monte Carlo, grecs, payoff, graphiques |
| assets.py | Dictionnaire des sous-jacents (nom, devise, ticker Yahoo Finance) |
| data_provider.py | Recuperation des prix spot en temps reel (yfinance) |
| book.py | Classe OptionBook : ajout, suppression, sauvegarde CSV, payoff global |
| pricer_ui.py | Interface Streamlit : menu PRICER, BOOK, PAYOFF GLOBAL, DELETE |
| presentation/SCRIPT_PRESENTATION.md | Script oral de presentation, lie au code |

## Installation

```
pip install -r requirements.txt
```

## Lancement

```
streamlit run pricer_ui.py
```

Depuis Anaconda Prompt, dans le dossier du projet.

## Limites connues

- Un seul pas de temps et une seule volatilite par option (pas de surface de volatilite).
- La volatilite est saisie, pas calibree sur les donnees de marche.
- Longstaff-Schwartz est present dans Pricer.py mais n'est pas valide : il n'est pas utilise dans l'interface.
- Le graphique de payoff de la page PRICER suit le sens choisi (achat ou vente) ; le payoff global du book tient compte de chaque ligne, achat ou vente.
