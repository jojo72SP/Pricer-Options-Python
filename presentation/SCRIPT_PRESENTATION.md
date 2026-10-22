# Script oral guide par le code — Pricer d'options (Joseph)

Chaque ecran suit le meme ordre : **cliquer sur le lien → montrer les lignes indiquees → donner l'explication juste dessous**. Les numeros de ligne correspondent a la version actuelle des fichiers. Prevoir environ 20 minutes avec la demo, a mesurer en repetition.

Le fil conducteur : **on suit le chemin d'un prix, du marche jusqu'au portefeuille.**

## 1. Presenter le projet

### Ecran 1.1

**Montrer : [README.md](../README.md) puis l'arborescence du dossier.**

**A dire :**

C'est un pricer d'options europeennes. Il recupere le prix spot en temps reel, calcule le prix par Black-Scholes et par Monte Carlo, donne les grecs, et permet de constituer un portefeuille d'options dont on voit le payoff global. L'interface est en Streamlit. Le projet est decoupe en cinq fichiers : les modeles dans Pricer, les donnees de marche dans assets et data_provider, le portefeuille dans book, et l'interface dans pricer_ui.

## 2. Donnees de marche

### Ecran 2.1

**Montrer : [assets.py](../assets.py) — le dictionnaire ASSETS.**

**A dire :**

Chaque sous-jacent a un nom, une devise et un ticker Yahoo Finance. Pour ajouter un actif, on ajoute une entree dans ce dictionnaire. Rien d'autre a changer.

### Ecran 2.2

**Montrer : [data_provider.py](../data_provider.py) — get_spot_price et get_all_prices.**

**A dire :**

`get_spot_price` interroge Yahoo Finance pour un ticker et renvoie le dernier prix. `get_all_prices` fait la meme chose pour tous les actifs du dictionnaire. Limite a connaitre : si Yahoo ne repond pas, l'interface passe en saisie manuelle du prix spot.

### Ecran 2.3

**Montrer : [Pricer.py, lignes 14 a 22](../Pricer.py#L14-L22) — get_market_data.**

**A dire :**

Ce sont des valeurs de reference pour tester le modele hors ligne. L'interface, elle, utilise le prix spot reel.

## 3. Black-Scholes

### Ecran 3.1

**Montrer : [Pricer.py, lignes 32 a 35](../Pricer.py#L32-L35) — normal_cdf.**

**A dire :**

`normal_cdf` est la fonction de repartition de la loi normale centree reduite. Elle donne la probabilite qu'une variable normale soit inferieure ou egale a x. Black-Scholes en a besoin pour calculer les probabilites d'exercice.

### Ecran 3.2

**Montrer : [Pricer.py, lignes 37 a 43](../Pricer.py#L37-L43) — black_scholes.**

**A dire :**

Premiere ligne : d1 et d2, les deux variables de la formule. Ensuite, le prix d'un call est le spot actualisé avec le dividende, moins le strike actualisé avec le taux. Le put suit la meme logique. C'est un prix ferme : une seule formule, pas de simulation.

## 4. Monte Carlo

### Ecran 4.1

**Montrer : [Pricer.py, lignes 47 a 60](../Pricer.py#L47-L60) — monte_carlo.**

**A dire :**

On tire N chemins de prix avec une loi lognormale. Pour chaque chemin, on calcule le payoff a maturité, puis on actualise et on moyenne. La fonction renvoie aussi l'erreur standard : elle mesure la precision du resultat. La graine `seed=2026` rend le tirage reproductible d'une execution a l'autre.

### Ecran 4.2

**A dire (sans montrer le code) :**

Longstaff-Schwartz est aussi dans le fichier, pour les options americaines. Il n'est pas valide pour l'instant, donc je ne le montre pas aujourd'hui.

## 5. Les grecs

### Ecran 5.1

**Montrer : [Pricer.py, lignes 111 a 116](../Pricer.py#L111-L116) — delta.**

**A dire :**

Pour rappel: Le delta est la sensibilité du prix au spot. Pour un call, il est situé entre 0 et 1 : une option proche de la monnaie bouge presque comme le sous-jacent. Les autres grecs suivent la meme structure, avec la meme variable d1.

### Ecran 5.2

**Montrer : [Pricer.py, lignes 118 a 144](../Pricer.py#L118-L144) — gamma, vega, theta, rho.**

**A dire :**

Le Gamma mesure la courbure du prix par rapport au spot. Le Vega mesure la sensibilité a la volatilité. le theta mesure combien ton option perd de valeur chaque jour qui passe, toutes choses égales par ailleurs. Le Rho mesure la sensibilité aux taux. On les calcule une fois, a partir de d1 et d2.

### Ecran 5.3

**Montrer : [Pricer.py, lignes 146 a 155](../Pricer.py#L146-L155) — plot_greeks.**

**A dire :**

Les cinq grecs sont tracés sur une grille de spots, de 70 % a 130 % du strike. Le graphique montre comment chaque grec change quand le marche bouge.

## 6. Payoff et point mort

### Ecran 6.1

**Montrer : [Pricer.py, lignes 204 a 219](../Pricer.py#L204-L219) — payoff_avec_prime.**

**A dire :**

Le payoff intrinsèque d'un call est max(S - K, 0), celui d'un put max(K - S, 0). La prime est retirée pour l'acheteur, et ajoutée pour le vendeur, qui a le signe inverse.

### Ecran 6.2

**Montrer : [Pricer.py, lignes 221 a 231](../Pricer.py#L221-L231) — get_breakeven.**

**A dire :**

Le point mort est le spot a partir duquel la position est gagnante a maturité. Pour un call acheteur, c'est le strike plus la prime. Pour un put acheteur, c'est le strike moins la prime.

### Ecran 6.3

**Montrer : [Pricer.py, lignes 234 a 259](../Pricer.py#L234-L259) — plot_payoff.**

**A dire :**

Le graphique montre le payoff intrinsèque en bleu et le profit net, prime deduite, en vert pointillé. Le trait rouge marque le point mort.

## 7. Le book

### Ecran 7.1

**Montrer : [book.py, lignes 10 a 19](../book.py#L10-L19) — la classe OptionBook et add_option.**

**A dire :**

Ici le book est la classe qui garde les options dans un tableau pandas. `add_option` ajoute une ligne avec le sous-jacent, le type, le strike, la maturité, la prime et la quantité.

### Ecran 7.2

**Montrer : [book.py, lignes 38 a 47](../book.py#L38-L47) — save_to_csv et load_from_csv.**

**A dire :**

Le book est sauvegarde dans un fichier CSV, et relu au lancement. Le fichier n'est pas publie sur GitHub : il contient des positions personnelles.

### Ecran 7.3

**Montrer : [book.py, lignes 49 a 59](../book.py#L49-L59) — get_total_payoff.**

**A dire :**

Pour chaque ligne du book, on calcule le payoff intrinseque sur la grille de spots, on retire la prime, puis on multiplie par la quantite. On additionne toutes les lignes : c'est le payoff global. Limite a connaitre : le book ne distingue pas encore achat et vente.

## 8. L'interface Streamlit

### Ecran 8.1

**Montrer : [pricer_ui.py, lignes 29 a 50](../pricer_ui.py#L29-L50) — menu PRICER et parametres.**

**A dire :**

Le menu lateral choisit la page. En mode PRICER, on choisit l'actif, puis les parametres : type, strike, maturite, taux, volatilite, dividende, nombre de chemins. Le prix spot est celui recupere en temps reel.

### Ecran 8.2

**Montrer : [pricer_ui.py, lignes 51 a 62](../pricer_ui.py#L51-L62) — calcul et affichage des prix.**

**A dire :**

A chaque changement d'un parametre, Streamlit relance le script. Black-Scholes et Monte Carlo sont calculés, puis affichés cote a cote avec l'ecart entre les deux.

### Ecran 8.3

**Montrer : [pricer_ui.py, lignes 79 a 91](../pricer_ui.py#L79-L91) — bouton Ajouter au Book.**

**A dire :**

Le bouton envoie l'option au book, avec le prix Black-Scholes comme prime. Le book est garde en memoire pendant la session.

### Ecran 8.4

**Montrer : [pricer_ui.py, lignes 93 a 104](../pricer_ui.py#L93-L104) — page BOOK.**

**A dire :**

La page BOOK affiche le tableau et permet de sauvegarder en CSV. Si le book est vide, un message le signale.

### Ecran 8.5

**Montrer : [pricer_ui.py, lignes 106 a 120](../pricer_ui.py#L106-L120) — page PAYOFF GLOBAL.**

**A dire :**

Le graphique montre le payoff global du portefeuille sur une grille de spots de 0 a 200. C'est le gain ou la perte total, toutes positions confondues.

### Ecran 8.6

**Montrer : [pricer_ui.py, lignes 122 a 129](../pricer_ui.py#L122-L129) — page DELETE.**

**A dire :**

On choisit l'index d'une ligne, puis on la supprime. Les index sont ceux affiches dans le tableau BOOK.

## 9. Demo

### Ecran 9.1

**Montrer : le terminal Anaconda Prompt.**

```
cd C:\Users\willi\.spyder-py3
streamlit run pricer_ui.py
```

**A dire :**

Je lance l'interface. Je choisis TTE, je garde les parametres par defaut, je regarde les prix Black-Scholes et Monte Carlo. J'ajoute l'option au book, je passe en BOOK, puis en PAYOFF GLOBAL.

**Avant la demo : verifier que yfinance repond. Sinon, dire qu'on passe en saisie manuelle du spot.**

## 10. Conclure

### Ecran 10.1

**Montrer : [pricer_ui.py, lignes 75 a 77](../pricer_ui.py#L75-L77) — comparaison BS vs MC, puis le graphique de comparaison.**

**A dire :**

Les deux methodes donnent des prix proches. Monte Carlo converge vers Black-Scholes quand le nombre de chemins augmente, et l'erreur standard indique la precision. Les limites sont connues : une volatilite saisie et non calibree, pas d'options americaines validees, et un book sans distinction achat et vente. Les prochaines etapes : valider Longstaff-Schwartz, calibrer la volatilite sur les donnees de marche, et ajouter le sens de la position au book.
