# Cadre juridique : deux façons d'ouvrir un marché

Cette note résume les règles qui éclairent les chiffres du projet, puis le cadre d'utilisation des données. Elle ne constitue pas un avis juridique.

## 1. La France : un marché ouvert, mais limité

| Point | Règle | Source |
|---|---|---|
| Ouverture | Loi n° 2010-476 du 12 mai 2010 : ouverture à la concurrence des paris sportifs, des paris hippiques et du poker en ligne, sur agrément | Loi du 12 mai 2010 |
| Casino en ligne | Non autorisé : les jeux de casino en ligne restent hors du périmètre ouvert par la loi de 2010 | Loi du 12 mai 2010 |
| Régulateur | Autorité nationale des jeux (ANJ), créée par l'ordonnance n° 2019-1015 du 2 octobre 2019, en remplacement de l'ARJEL | Ordonnance du 2 octobre 2019 |
| Reversement aux joueurs | Un opérateur de paris sportifs ou hippiques en ligne ne peut pas reverser plus de 85 % des mises sur une année civile (taux de retour aux joueurs, TRJ) | Décret n° 2020-1349 du 4 novembre 2020, art. 27 et 28 ; délibération de l'ANJ du 1er avril 2021 |
| Fiscalité 2025 | Au 1er juillet 2025, la contribution sociale sur les paris sportifs passe de 10,6 % à 15 % du PBJ, et un prélèvement de 15 % s'applique aux dépenses de publicité et de promotion des opérateurs (hors sponsoring sportif) | ANJ, *Bilan du marché 2024*, p. 8 (loi de financement de la sécurité sociale) |
| Protection des joueurs | Interdiction volontaire de jeu, d'au moins trois ans, valable en ligne et dans les casinos | ANJ |

**Ce que le plafond change, en clair :** sur 100 € misés dans l'année, l'opérateur doit garder au moins 15 €. Quelle que soit sa justification, la règle a un effet direct sur le prix du pari pour le joueur : à mise égale, il récupère moins qu'avec un opérateur non plafonné. Le projet observe une marge française toujours supérieure à 15 %, et une marge ontarienne entre 6 et 7 %.

## 2. L'Ontario : un marché ouvert à la concurrence, casino compris

| Point | Règle | Source |
|---|---|---|
| Base fédérale | Le Code criminel canadien réserve l'organisation des jeux d'argent aux provinces ; les paris sportifs sur un seul événement sont légaux depuis le 27 août 2021 | Loi sur les paris sportifs sécuritaires et réglementés (L.C. 2021, ch. 20) |
| Ouverture | Marché ouvert le 4 avril 2022 à des opérateurs privés, par contrat avec iGaming Ontario (iGO) | iGO |
| Régulateur | Commission des alcools et des jeux de l'Ontario (AGCO), qui fixe les *Registrar's Standards for Internet Gaming* | AGCO |
| Produits | Casino (machines à sous, jeux de table, bingo), paris (sport, esport, paris spéciaux, bourse de paris), poker entre joueurs | iGO, définitions du rapport mensuel |
| Publicité | Depuis le 28 février 2024, interdiction d'utiliser des athlètes, actifs ou retraités, dans les publicités, sauf pour promouvoir le jeu responsable (norme 2.03) | AGCO, annonce du 29 août 2023 |
| Reversement aux joueurs | Aucun plafond ni plancher : les normes de l'AGCO imposent d'afficher cotes et gains (norme 2.15.2) et de documenter l'avantage de l'opérateur (norme 4.05), sans fixer de taux | [AGCO, Registrar's Standards for Internet Gaming](https://agco.ca/en/book/export/html/245361) |

## 2 bis. L'offre illégale et ce que l'État prélève

| Point | France | Ontario |
|---|---|---|
| Offre illégale | Délit : trois ans d'emprisonnement et 90 000 € d'amende ; 100 000 € d'amende pour la publicité (loi du 12 mai 2010, art. 56 et 57). Blocage administratif par l'ANJ depuis 2022 : 1 688 URL bloquées en 2025 | Sites non agréés visés par l'AGCO ; mesure de la canalisation par sondage Ipsos |
| Prélèvement public | 59,3 % du produit brut des paris sportifs en ligne, toutes taxes et contributions, depuis le 1er juillet 2025 | La province est l'exploitant : iGaming Ontario conserve environ 20 % du revenu de jeu et verse un dividende à la province |
| Sources | ANJ, Rapport annuel 2025 (p. 45-47) ; Bilan du marché 2024 (p. 8) | iGaming Ontario, rapport annuel 2024-2025 ; AGCO et iGO, rapport Ipsos |

## 3. La comparaison, et ses limites

- **Deux définitions proches, pas identiques.** Le PBJ français (mises moins gains) et le NAGGR ontarien (mises en argent réel moins gains, hors mises de bonus) mesurent la même chose dans l'esprit, mais le traitement des bonus diffère : les comparaisons sont des ordres de grandeur.
- **Une règle, plusieurs causes.** Un écart de marge cohérent avec une règle ne prouve pas que la règle en est la cause. Pour le démontrer, il faudrait comparer avant et après une modification du plafond, ou des marchés comparables avec et sans plafond.

## 4. Le cadre d'utilisation des données

| Données | Statut |
|---|---|
| Jeux de données de l'ANJ sur data.gouv.fr | Données publiques, réutilisées avec citation de la source |
| Rapports de l'ANJ | Documents publics, chiffres cités avec la page |
| Rapport mensuel d'iGO | Publication publique ; iGO précise que les chiffres sont non audités et ne garantit pas leur exactitude |
| INSEE (Filosofi via data.gouv.fr) | Licence ODbL : citation de la source, partage à l'identique des bases dérivées |
| INSEE (estimations de population) | Réutilisation libre avec citation |

**Données personnelles :** aucune. Tous les chiffres sont agrégés (départements, mois, rencontres). Aucun scraping n'a été utilisé : les fichiers ont été téléchargés depuis les sites officiels.

**Ce qui est publié :** le code, le notebook exécuté, les fichiers sources (publics) et les tables dérivées, avec la mention de leurs sources. Les tables dérivées de Filosofi restent sous licence ODbL.
