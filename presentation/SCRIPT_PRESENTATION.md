# Script oral guidé par le code : Pricer d'options (Joseph)

Chaque écran suit le même ordre : **cliquer sur le lien → montrer les lignes indiquées → donner l'explication juste dessous**. Les numéros de ligne correspondent à la version actuelle des fichiers. Prévoir environ 25 minutes avec la démo, à mesurer en répétition.

Le fil conducteur : **on suit le chemin d'un prix, du marché jusqu'au portefeuille, puis on teste le modèle et on dit ce qu'il ne fait pas.**

Les valeurs notées « attendu » sont des calculs à la main avec les paramètres : S = K = 100, T = 1, r = 5 %, q = 0, sigma = 20 %. Elles servent de repère : pendant la démo, on vérifie que l'écran les retrouve.

## 1. Présenter le projet

### Écran 1.1

**Montrer : [README.md](../README.md) puis l'arborescence du dossier.**

**À dire :**

C'est un pricer d'options européennes. Il récupère le prix spot, calcule le prix par Black-Scholes et par Monte Carlo, donne les grecs, et permet de constituer un portefeuille dont on voit le payoff global. L'interface est en Streamlit. Le projet est découpé en cinq fichiers : les modèles dans Pricer, les données de marché dans assets et data_provider, le portefeuille dans book, et l'interface dans pricer_ui.

## 2. Données de marché

### Écran 2.1

**Montrer : [assets.py](../assets.py) : le dictionnaire ASSETS.**

**À dire :**

Chaque sous-jacent a un nom, une devise et un ticker Yahoo Finance. Pour ajouter un actif, on ajoute une entrée dans ce dictionnaire.

### Écran 2.2

**Montrer : [data_provider.py](../data_provider.py) : get_spot_price et get_all_prices.**

**À dire :**

`get_spot_price` interroge Yahoo Finance pour un ticker et renvoie le dernier cours. Pour les indices et les matières premières, il utilise `fast_info`, car `currentPrice` n'existe pas pour ces actifs. `get_all_prices` fait la même chose pour tous les actifs.

**Limite à dire clairement :** ces cours sont ceux de Yahoo Finance, gratuits et parfois différés. Ce n'est pas un flux temps réel de salle de marché.

### Écran 2.3

**Montrer : [Pricer.py, lignes 14 à 22](../Pricer.py#L14-L22) : get_market_data.**

**À dire :**

Ce sont des valeurs de référence pour tester le modèle hors ligne. L'interface utilise le cours réel.

## 3. Black-Scholes

### Écran 3.1

**Montrer : [Pricer.py, lignes 32 à 35](../Pricer.py#L32-L35) : normal_cdf.**

**À dire :**

`normal_cdf` donne la probabilité qu'une variable normale centrée réduite soit inférieure ou égale à x. Black-Scholes s'en sert pour les probabilités d'exercice.

### Écran 3.2

**Montrer : [Pricer.py, lignes 37 à 43](../Pricer.py#L37-L43) : black_scholes.**

**À dire :**

Première ligne : d1 et d2, les deux variables de la formule. Ensuite, le prix d'un call est le spot actualisé avec le dividende, moins le strike actualisé avec le taux. Le put suit la même logique. C'est un prix ferme : une seule formule, pas de simulation.

### Écran 3.3 : Vérification chiffrée

**Montrer : l'écran de l'application, avec S = K = 100, call, sigma 20 %, T = 1, r = 5 %.**

**À dire :**

Le prix Black-Scholes doit donner **10,4506** (attendu). Je le vérifie à la main avec les tables de la loi normale : c'est le même nombre. Pour un call à la monnaie, à un an, c'est un ordre de grandeur cohérent : environ 10 % du spot.

**Attention à la démo :** le champ Strike est pré-rempli avec le cours spot arrondi, donc une option à la monnaie sur l'actif choisi. Il reste modifiable : voir la section 8 pour le DAX, le pétrole et l'or.

## 4. Monte Carlo

### Écran 4.1

**Montrer : [Pricer.py, lignes 47 à 60](../Pricer.py#L47-L60) : monte_carlo.**

**À dire :**

On tire N chemins de prix avec une loi lognormale. Pour chaque chemin, on calcule le payoff à maturité, puis on actualise et on moyenne. La fonction renvoie aussi l'erreur standard : elle mesure la précision du résultat. La graine `seed=2026` rend le tirage reproductible d'une exécution à l'autre.

### Écran 4.2 : Convergence

**Montrer : l'application, call à la monnaie. Passer le nombre de chemins de 1 000 à 10 000 puis à 100 000.**

**À dire :**

Avec 10 000 trajectoires, le résultat validé est **10,4650 plus ou moins 0,1483** (attendu : 10,4506 pour Black-Scholes, donc à l'intérieur de l'erreur). Quand on multiplie N par 10, l'erreur est divisée par racine de 10, soit environ 3. Le prix converge vers Black-Scholes, mais lentement : c'est le compromis de la méthode.

La graine `seed=2026` rend le résultat reproductible : deux lancements donnent le même chiffre.

### Écran 4.3 : Longstaff-Schwartz (sans montrer le code)

**À dire :**

Longstaff-Schwartz est aussi dans le fichier, pour les options américaines qu'on peut exercer avant l'échéance. Il n'est pas validé pour l'instant : je ne le montre pas aujourd'hui.

## 5. Put et call : la parité

### Écran 5.1 : Parité call-put

**Montrer : l'application, même jeu de paramètres, une fois en call, une fois en put.**

**À dire :**

Pour un put à la monnaie, on attend **5,5735** (attendu). Une relation doit toujours être vraie pour des options européennes sans dividende : call moins put égale spot moins strike actualisé.

Calcul : 10,4506 - 5,5735 = 4,8771, et 100 - 100 x e^(-0,05) = 4,8771. Les deux cotes sont égales. C'est la vérification la plus simple qu'un pricer doit passer.

## 6. Les grecs

### Écran 6.1 : Delta

**Montrer : [Pricer.py, lignes 111 à 116](../Pricer.py#L111-L116) : delta.**

**À dire :**

Le delta est la sensibilité du prix au spot : si le sous-jacent monte de 1, le prix change d'environ delta. Pour un call à la monnaie, on attend **0,637** (attendu). Pour le put, **-0,363** : il baisse quand le spot monte. Le delta du put est le delta du call moins 1.

### Écran 6.2 : Gamma, vega, thêta, rho

**Montrer : [Pricer.py, lignes 118 à 144](../Pricer.py#L118-L144) : gamma, vega, theta, rho.**

**À dire :**

- **Gamma** : la vitesse de variation du delta. À la monnaie, environ **0,019** (attendu). Il est maximal à la monnaie et se réduit quand l'option s'éloigne.
- **Vega** : la sensibilité à la volatilité. À la monnaie, environ **37,5** (attendu), soit **0,375** pour une hausse d'un point de volatilité. Le vega est le même pour le call et le put.
- **Thêta** : la perte de valeur quand le temps passe. Pour le call à la monnaie, environ **-6,4 par an**, soit environ **-0,018 par jour**. Le thêta est négatif pour l'acheteur.
- **Rho** : la sensibilité au taux. Pour le call à la monnaie, environ **+53**. Pour le put, environ **-42**. Le call gagne quand les taux montent, le put perd.

### Écran 6.3 : Lire les graphiques

**Montrer : [Pricer.py, lignes 146 à 155](../Pricer.py#L146-L155) : plot_greeks, puis l'application.**

**À dire :**

Les cinq grecs sont tracés sur des spots de 70 % à 130 % du strike. On voit que le delta passe de 0 à 1, que le gamma et le vega culminent autour du strike, et que le thêta est toujours négatif pour un achat. L'encadré en bas à droite donne les valeurs au cours actuel.

## 7. Sensibilités : que se passe-t-il si on change un paramètre

**Montrer : l'application. Changer un seul paramètre à la fois, noter le prix du call et du put.**

**À dire :** on change un paramètre à la fois. Le sens de variation vient de la théorie, la taille de l'effet vient des grecs.

| Paramètre augmenté | Call | Put | Pourquoi |
| --- | --- | --- | --- |
| Volatilité (sigma) | monte | monte | Plus d'incertitude, plus d'option. Vega positif. |
| Maturité (T) | monte en général | monte en général | Plus de temps pour que le marché bouge. |
| Taux (r) | monte | baisse | Le strike est actualisé moins fortement. Rho du call positif, du put négatif. |
| Strike (K) | baisse | monte | Le call est plus cher quand il est plus facile à exercer. |
| Spot (S) | monte | baisse | Delta du call positif, du put négatif. |
| Dividende (q) | baisse | monte | Le dividende fait baisser le cours attendu. |

**Chiffres à montrer :** une hausse de volatilité de 1 point augmente le call à la monnaie d'environ 0,375. Une hausse de spot de 1 euro augmente le call d'environ 0,64.

## 8. Autres sous-jacents

### Écran 8.1 : Action, indice, matière première

**Montrer : l'application, avec le menu Actif : TTE, DAX, BRENT, OR.**

**À dire :**

Le modèle est le même pour toutes les classes d'actifs : seul le spot change. Une action et un indice se pricent comme un titre sans dividende ou avec un dividende. Le pétrole et l'or sont traités comme des actifs sans rendement.

**Ce qu'il faut dire honnêtement :**

- Le prix d'un DAX est de l'ordre de 20 000 points : le strike doit être dans le même ordre de grandeur. Le champ Strike est pré-rempli avec le cours spot de l'actif choisi, donc il suit le bon ordre de grandeur sans toucher au curseur. Si le spot change, le Strike est recalculé.
- Le Brent et l'or sont cotés en dollars : le pricer ne convertit pas la devise. Le payoff global du book n'est pas converti en euros non plus.
- La volatilité est saisie à la main : elle n'est pas calibrée sur le marché. Pour le DAX, la volatilité implicite du marché existe (indice VSTOXX), mais le pricer ne la récupère pas encore.

## 9. Payoff, point mort et book

### Écran 9.1 : Point mort

**Montrer : [Pricer.py, lignes 204 à 231](../Pricer.py#L204-L231) : payoff_avec_prime et get_breakeven.**

**À dire :**

Le payoff intrinsèque d'un call est max(S - K, 0). On retire la prime pour obtenir le profit net. Le point mort, pour un call acheteur, est le strike plus la prime : 100 + 10,45 = 110,45 pour un call à 10,45 de prime.

### Écran 9.2 : Graphique du payoff

**Montrer : [Pricer.py, lignes 234 à 259](../Pricer.py#L234-L259) : plot_payoff.**

**À dire :**

En bleu, le payoff intrinsèque. En vert pointillé, le profit net. Le trait rouge marque le point mort. Le graphique suit le sens choisi dans la barre latérale. Pour une vente, les courbes sont inversées : le vendeur gagne quand l'acheteur perd.

### Écran 9.3 : Le book

**Montrer : [book.py, lignes 14 à 30](../book.py#L14-L30) : OptionBook et add_option.**

**À dire :**

Le book garde les options dans un tableau pandas. Chaque ligne a un sous-jacent, un sens (achat ou vente), un type, un strike, une maturité, une prime et une quantité. Si une colonne manque, l'ajout est refusé.

### Écran 9.4 : Payoff global

**Montrer : [book.py, lignes 54 à 65](../book.py#L54-L65) : get_total_payoff, puis [pricer_ui.py, lignes 122 à 136](../pricer_ui.py#L122-L136).**

**À dire :**

Pour chaque ligne, on calcule le payoff intrinsèque sur une grille de spots, on retire la prime, on multiplie par la quantité. Pour une vente, le signe est inversé. On additionne toutes les lignes : c'est le payoff global. Un achat de call et une vente de put donnent deux courbes qui se compensent en partie.

### Écran 9.5 : Sauvegarde et suppression

**Montrer : [book.py, lignes 39 à 52](../book.py#L39-L52) : save_to_csv et load_from_csv, puis [pricer_ui.py, lignes 138 à 148](../pricer_ui.py#L138-L148) : page DELETE.**

**À dire :**

Le book est sauvegardé en CSV et relu au lancement. Il contient des positions personnelles : le fichier n'est pas publié sur GitHub. On supprime une ligne par son index, celui du tableau BOOK.

## 10. Démo

### Écran 10.1

**Montrer : le terminal Anaconda Prompt.**

```
cd C:\Users\willi\.spyder-py3
streamlit run pricer_ui.py
```

**À dire :**

Je lance l'interface. Je prends un call à la monnaie sur TTE, avec K égal au cours affiché. Je note le prix Black-Scholes et le prix Monte Carlo. Je passe le put : je vérifie la parité. J'ajoute un achat de call, puis une vente de put au book, et je regarde le payoff global.

**Avant la démo :**
- vérifier que yfinance répond (le cours doit s'afficher dans la barre latérale) ;
- sinon, dire qu'on passe sur un spot saisi à la main ;
- avoir le tableau de la section 5 et de la section 7 sous les yeux.

## 11. Conclure : limites et améliorations

### Écran 11.1 : Ce que le projet fait

**Montrer : la page PRICER, puis la page PAYOFF GLOBAL.**

**À dire :**

Le pricer calcule des prix européens, les vérifie par deux méthodes, donne les grecs, et gère un portefeuille avec un payoff global. Les résultats sont cohérents : la parité call-put est respectée, Monte Carlo converge vers Black-Scholes.

### Écran 11.2 : Limites

**À dire :**

- **Une seule volatilité** par option, saisie à la main. Un desk utilise une surface de volatilité, calibrée sur les options cotées.
- **Un taux unique** et plat. Un desk utilise une courbe de taux (swaps ou OIS) pour chaque maturité.
- **Pas de dividendes discrets** : le dividende est un taux continu. Les dividendes réels sont des montants à des dates précises.
- **Européen seulement** : Longstaff-Schwartz n'est pas validé.
- **Monte Carlo lent** : la boucle est en Python pur, pas vectorisée.
- **Données gratuites** : Yahoo Finance, sans garantie de temps réel.
- **Pas de devise** : le book ne convertit pas en euros.
- **Pas de tests automatisés**, pas de validation sur des cotations réelles.
- **Le book n'est pas un vrai livre de positions** : pas de date de transaction, pas de valorisation dans le temps, pas de P&L historique.

### Écran 11.3 : Améliorations, par ordre de priorité

**À dire :**

1. Convertir le payoff global en euros avec le taux de change du jour.
2. Valider Longstaff-Schwartz sur un cas connu, puis le comparer à un arbre binomial.
3. Calibrer la volatilité sur les options cotées, ou au minimum sur la volatilité implicite du marché.
4. Ajouter des tests automatisés : parité call-put, prix à sigma nul, convergence Monte Carlo.
5. Vectoriser le Monte Carlo avec numpy pour gagner en vitesse.
6. Ajouter la date de transaction au book et un suivi de la valeur dans le temps.

### Écran 11.4 : Comparaison avec les pricers de salle de marché

**À dire :**

Un pricer de salle de marché ne se compare pas directement à ce projet : il fait la même chose à une autre échelle et avec d'autres exigences.

| Aspect | Ce projet | Salle de marché |
| --- | --- | --- |
| Données de marché | Yahoo Finance, gratuit | Flux professionnel, temps réel, historique contrôlé |
| Volatilité | Saisie à la main, plate | Surface calibrée par strike et maturité |
| Taux | Un taux unique | Courbes de taux par devise |
| Types d'options | Européennes | Américaines, barrières, exotiques |
| Calcul des grecs | Formules fermées | Bump-and-revalue, différentiation automatique |
| Vitesse | Python, boucles | C++ ou code vectorisé, parallèle |
| Contrôle | Aucun test | Validation de modèle, tests de non-régression, audit |
| Risque | Payoff à maturité | VaR, scénarios de stress, P&L quotidien |
| Positions | Un fichier CSV | Système de transactions relié à la comptabilité |

**Phrase à retenir :** le projet montre que je comprends la mécanique du pricing et des grecs. Un pricer de salle de marché montre en plus comment on sait qu'un prix est juste, et comment on gère le risque quand le modèle se trompe.
