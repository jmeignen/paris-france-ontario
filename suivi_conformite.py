"""Tableau de suivi de conformité, France et Ontario.

Ce script relit les tables du notebook (donnees/exports/) et les fichiers bruts de l'ANJ,
puis écrit trois tables pour Power BI et un graphique :

- donnees/exports/suivi_indicateurs.csv : un indicateur par ligne, avec la règle, le seuil, la valeur et un statut ;
- donnees/exports/suivi_ontario_paris_mensuel.csv : la marge mensuelle des paris en Ontario et ses limites de contrôle ;
- donnees/exports/evenements_reglementaires.csv : les changements de règles datés, repris de VEILLE_REGLEMENTAIRE.md ;
- images/suivi_conformite.png.

Ce que le statut veut dire :
- « Au-dessus du plancher (niveau marché) » : la marge du marché respecte le plancher légal. Le plafond de reversement
  s'applique à chaque opérateur ; un chiffre agrégé ne prouve donc pas que chaque opérateur l'a respecté.
- « Pas de seuil légal : suivi » : aucune règle chiffrée trouvée, l'indicateur sert à repérer une évolution.
- « Écart à expliquer » : la valeur sort de sa plage habituelle. Ce n'est pas une infraction, c'est une question à poser.
- « Anomalie de données » : un contrôle de qualité a échoué ; elle est corrigée ou signalée dans le notebook.

Lancer depuis la racine du projet : python suivi_conformite.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

RACINE = Path(__file__).parent
EXPORTS = RACINE / "donnees" / "exports"
BRUTES = RACINE / "donnees" / "brutes"
IMAGES = RACINE / "images"

PLANCHER_FR = 0.15        # décret n° 2020-1349, art. 27 : reversement aux joueurs plafonné à 85 % des mises
FENETRE = 12              # mois de référence pour les limites de contrôle
K = 2                     # nombre d'écarts-types autour de la moyenne

lignes = []


def ajoute(indicateur, marche, periode, valeur, seuil, regle, source, statut, commentaire=""):
    lignes.append(dict(indicateur=indicateur, marche=marche, periode=str(periode), valeur=valeur, seuil=seuil,
                       regle=regle, source=source, statut=statut, commentaire=commentaire))


# 1. France : marge des paris sportifs en ligne face au plancher de 15 %
fr = pd.read_csv(EXPORTS / "france_paris_sportifs_annuel.csv")
for _, r in fr.iterrows():
    ajoute("Part des mises gardée par les opérateurs (paris sportifs)", "France", int(r.annee), round(r.taux_de_marge, 4),
           PLANCHER_FR, "Reversement aux joueurs plafonné à 85 % des mises sur l'année",
           "ANJ, Bilan du marché 2024, p. 8-9",
           "Au-dessus du plancher (niveau marché)" if r.taux_de_marge >= PLANCHER_FR else "Écart à expliquer")
# 2025 vient d'un autre document de l'ANJ : on ne le mélange pas avec la série précédente (voir le notebook).
marge_2025 = 1766 / 11517
ajoute("Part des mises gardée par les opérateurs (paris sportifs)", "France", 2025, round(marge_2025, 4), PLANCHER_FR,
       "Reversement aux joueurs plafonné à 85 % des mises sur l'année", "ANJ, Rapport annuel 2025, p. 16",
       "Au-dessus du plancher (niveau marché)" if marge_2025 >= PLANCHER_FR else "Écart à expliquer",
       "Série différente de 2019-2024 : l'ANJ publie deux valeurs pour 2024")

# 2. France : interdictions volontaires de jeu face au nombre de joueurs
iv = pd.read_csv(EXPORTS / "france_interdits_annuel.csv").set_index("annee")
croissance_iv = iv.loc[2024, "inscrits"] / iv.loc[2021, "inscrits"] - 1
croissance_joueurs = 3874 / 3730 - 1   # joueurs uniques en ligne, ANJ, Bilan du marché 2024, p. 17
ajoute("Personnes interdites de jeu, évolution 2021-2024", "France", "2021-2024", round(croissance_iv, 4), None,
       "Interdiction volontaire de jeu (au moins trois ans, en ligne et en casino)",
       "ANJ sur data.gouv.fr ; Bilan du marché 2024, p. 17",
       "Pas de seuil légal : suivi",
       f"Joueurs uniques en ligne sur la même période : {croissance_joueurs:+.0%}. L'interdiction couvre aussi les casinos physiques.")

# 3. Ontario : marge mensuelle des paris, avec limites de contrôle glissantes
prod = pd.read_csv(EXPORTS / "ontario_mensuel_produits.csv", parse_dates=["mois"])
paris = prod[prod.produit == "Paris"].sort_values("mois").set_index("mois")[["mises_m", "revenu_m"]]
paris["marge"] = paris.revenu_m / paris.mises_m
ref = paris["marge"].shift(1).rolling(FENETRE)          # les 12 mois précédents, sans le mois lui-même
paris["moyenne_12m"] = ref.mean()
paris["limite_basse"] = paris.moyenne_12m - K * ref.std()
paris["limite_haute"] = paris.moyenne_12m + K * ref.std()
paris["statut"] = "Pas assez d'historique"
ok = paris.moyenne_12m.notna()
paris.loc[ok, "statut"] = "Dans la plage habituelle"
paris.loc[ok & ((paris.marge < paris.limite_basse) | (paris.marge > paris.limite_haute)), "statut"] = "Écart à expliquer"
paris.reset_index().to_csv(EXPORTS / "suivi_ontario_paris_mensuel.csv", index=False)

ecarts = paris[paris.statut == "Écart à expliquer"]
dernier = paris.iloc[-1]
ajoute("Part des mises gardée par les opérateurs (paris), dernier mois", "Ontario", dernier.name.strftime("%Y-%m"),
       round(dernier.marge, 4), None, "Les normes de l'AGCO ne fixent aucun taux de retour aux joueurs (normes 2.15.2 et 4.05)",
       "iGaming Ontario, rapport mensuel (non audité)", dernier.statut if dernier.statut != "Dans la plage habituelle"
       else "Pas de seuil légal : suivi",
       f"{len(ecarts)} mois sur {ok.sum()} hors de la plage moyenne ± {K} écarts-types des {FENETRE} mois précédents")

# 4. Ontario : poids du casino dans le revenu
an = prod.assign(annee=prod.mois.dt.year).groupby(["annee", "produit"]).revenu_m.sum().unstack()
for annee in [2023, 2024, 2025]:
    part = an.loc[annee, "Casino"] / an.loc[annee].sum()
    ajoute("Part du casino dans le revenu des jeux en ligne", "Ontario", annee, round(part, 4), None,
           "Casino en ligne autorisé depuis l'ouverture du 4 avril 2022", "iGaming Ontario, rapport mensuel",
           "Pas de seuil légal : suivi")

# 5. Contrôles de qualité des données
mois_attendus = pd.date_range(paris.index.min(), paris.index.max(), freq="MS")
manquants = len(mois_attendus.difference(paris.index))
ajoute("Mois manquants dans la série iGO", "Ontario", f"{paris.index.min():%Y-%m} à {paris.index.max():%Y-%m}", manquants, 0,
       "Contrôle de qualité", "iGaming Ontario, rapport mensuel", "Contrôle réussi" if manquants == 0 else "Anomalie de données")

tot = pd.read_csv(EXPORTS / "ontario_mensuel.csv", parse_dates=["mois"]).set_index("mois")
somme = prod.groupby("mois")[["mises_m", "revenu_m"]].sum()
ecart_max = (tot.revenu_m - somme.revenu_m).abs().max()
ajoute("Écart maximal entre le total et la somme des produits (revenu, M$ CA)", "Ontario", "tous les mois",
       round(ecart_max, 2), None, "Contrôle de qualité", "iGaming Ontario, rapport mensuel",
       "Contrôle réussi" if ecart_max <= 1 else "Anomalie de données", "iGO arrondit ses chiffres : un écart de quelques dixièmes est attendu")

raw = pd.read_csv(BRUTES / "anj-donnees-sur-la-repartition-geographique-des-personnes-faisant-lobjet-dune-interdiction-volontaire-de-jeu-depuis-2023.csv",
                  sep=";", header=None, dtype=str, encoding="latin-1")
b = raw.iloc[3:, [3, 4]].dropna()
b.columns = ["code", "n"]
b["code"] = b.code.str.strip()
b["n"] = b.n.astype(int)
invalide = ~b.code.str.match(r"^(\d\d|2A|2B)$") | b.code.isin(["00", "96", "98"])
ajoute("Codes de département invalides (interdictions 2024)", "France", 2024, int(invalide.sum()), 0, "Contrôle de qualité",
       "ANJ sur data.gouv.fr", "Anomalie de données",
       f"{b[invalide].n.sum()} personnes concernées, écartées de l'analyse par département")
ajoute("Écart entre les deux PBJ 2024 des paris sportifs publiés par l'ANJ (M€)", "France", 2024, 1759 - 1599, 0,
       "Contrôle de qualité", "ANJ, Bilan du marché 2024 (p. 8-9) et Rapport annuel 2025 (p. 15)", "Anomalie de données",
       "1 759 M€ contre 1 599 M€, aucune explication : les séries ne sont jamais additionnées")

suivi = pd.DataFrame(lignes)
suivi.to_csv(EXPORTS / "suivi_indicateurs.csv", index=False)

# 6. Changements de règles datés (détail et sources dans VEILLE_REGLEMENTAIRE.md)
evenements = pd.DataFrame([
    ("2020-11-04", "France", "Décret 2020-1349 : reversement aux joueurs plafonné à 85 % des mises", "Légifrance"),
    ("2022-04-04", "Ontario", "Ouverture du marché en ligne aux opérateurs privés", "iGaming Ontario"),
    ("2024-02-28", "Ontario", "Interdiction des athlètes dans les publicités (norme 2.03)", "AGCO"),
    ("2025-05-12", "Ontario", "iGaming Ontario devient un organisme indépendant de l'AGCO", "Gowling WLG"),
    ("2025-06-01", "Ontario", "Normes 2.10 et 2.11 : surveillance en temps réel du jeu à risque (mois de publication)", "Gowling WLG"),
    ("2025-07-01", "France", "Contribution sociale sur les paris portée à 15 % du PBJ ; prélèvement de 15 % sur la publicité", "ANJ, Bilan 2024, p. 8"),
    ("2026-05-14", "Ontario", "Lancement de l'auto-exclusion centralisée (norme 2.14.1)", "AGCO"),
    ("2026-05-19", "France", "L'ANJ adopte la formule d'un algorithme de repérage des joueurs excessifs", "ANJ"),
], columns=["date", "marche", "evenement", "source"])
evenements.to_csv(EXPORTS / "evenements_reglementaires.csv", index=False)

# 7. Graphique
VERT, MOUTARDE, CORAIL, ARDOISE, PAPIER = "#0f4c5c", "#e9b44c", "#e4572e", "#5b6770", "#f4f1ea"
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [2.2, 1]}, facecolor=PAPIER)
for a in (a1, a2):
    a.set_facecolor(PAPIER)
    a.spines[["top", "right"]].set_visible(False)
a1.fill_between(paris.index, paris.limite_basse, paris.limite_haute, color=VERT, alpha=0.12, lw=0, label="Plage habituelle")
a1.plot(paris.index, paris.marge, color=VERT, lw=1.8, label="Marge du mois")
a1.scatter(ecarts.index, ecarts.marge, color=CORAIL, zorder=3, s=36, label="Écart à expliquer")
for _, e in evenements[evenements.marche == "Ontario"].iterrows():
    d = pd.Timestamp(e.date)
    if d >= paris.index.min():
        a1.axvline(d, color=ARDOISE, lw=0.8, ls=":")
a1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
a1.xaxis.set_major_locator(mdates.YearLocator())
a1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
a1.set_title("Ontario, paris : part des mises gardée chaque mois\n(pointillés : changements de règles)", loc="left", fontsize=11)
a1.legend(frameon=False, fontsize=9, loc="upper left")
fr_tout = suivi[(suivi.marche == "France") & suivi.indicateur.str.startswith("Part des mises")]
a2.bar(fr_tout.periode, fr_tout.valeur, color=[MOUTARDE] * (len(fr_tout) - 1) + ["#c99a3a"])
a2.axhline(PLANCHER_FR, color=CORAIL, lw=1.4)
a2.set_ylim(0, 0.2)
a2.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
a2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
a2.set_title("France, paris sportifs : part gardée par année\n(trait rouge : plancher légal ; 2025 : autre série)", loc="left", fontsize=11)
fig.tight_layout()
fig.savefig(IMAGES / "suivi_conformite.png", dpi=150, facecolor=PAPIER)

print(suivi[["marche", "periode", "indicateur", "valeur", "statut"]].to_string(index=False))
print("\nMois hors plage (Ontario) :")
print(ecarts[["marge", "limite_basse", "limite_haute"]].round(4).to_string())
