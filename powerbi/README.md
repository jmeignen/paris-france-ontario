# Tableau de bord Power BI

Cinq pages, construites sur les fichiers de `donnees/exports/` produits par le notebook et par `suivi_conformite.py` :

1. **Deux marchés** : part du revenu par produit en Ontario, revenu mensuel, et la part des mises gardée par les opérateurs de paris dans chaque marché.
2. **Les parieurs français** : densité de parieurs sportifs par département, face à la part des jeunes hommes.
3. **Interdictions de jeu** : évolution nationale et comparaison par département.
4. **Les grands matchs** : les 100 rencontres les plus pariées.
5. **Suivi de conformité** : chaque indicateur face à sa règle, la marge mensuelle ontarienne et sa plage habituelle, les changements de règles datés.

## Ouvrir le rapport

1. Ouvrir `paris_france_ontario.pbip` dans Power BI Desktop.
2. Si le dossier du projet n'est pas `\\Mac\Home\Desktop\Data\projets\1_sport\06_paris-france-ontario`, changer le paramètre **DataFolder** (Transformer les données › Gérer les paramètres).
3. Cliquer sur **Actualiser**, puis Fichier › Enregistrer sous si un fichier `.pbix` est nécessaire.

## Mesures principales (DAX)

```
Marge = DIVIDE([Revenu (M$ CA)], [Mises (M$ CA)])
Part du revenu = DIVIDE([Revenu (M$ CA)], CALCULATE([Revenu (M$ CA)], ALL(ontario_produits[produit])))
Densité de parieurs = DIVIDE(SUM(departements[parieurs]), SUM(departements[adultes]))
Interdits pour 100 000 = DIVIDE(SUM(interdits_dep[interdits_2024]), SUM(interdits_dep[adultes])) * 100000
```

Les tables ne sont pas reliées entre elles : chaque page lit sa propre source, pour ne jamais mélanger des définitions différentes (PBJ français, NAGGR ontarien).
