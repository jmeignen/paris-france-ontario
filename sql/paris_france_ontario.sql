-- Parier en France, parier en Ontario : les mêmes questions en SQL (MySQL 8)
-- Tables chargées depuis donnees/exports/ (LOAD DATA ou import de l'assistant MySQL Workbench)

CREATE TABLE ontario_mensuel_produits (
    mois      DATE        NOT NULL,
    produit   VARCHAR(10) NOT NULL,          -- Casino, Paris, Poker
    mises_m   DECIMAL(10,1),                 -- millions de dollars canadiens
    revenu_m  DECIMAL(10,1),
    PRIMARY KEY (mois, produit)
);

CREATE TABLE france_departements (
    dep                 VARCHAR(20) PRIMARY KEY,
    departement         VARCHAR(60),
    parieurs            INT,
    adultes             INT,
    niveau_vie          DECIMAL(8,0),
    pauvrete            DECIMAL(4,1),
    part_hommes_20_34   DECIMAL(6,4)
);

CREATE TABLE france_interdits_departements (
    dep               VARCHAR(20) PRIMARY KEY,
    adultes           INT,
    interdits_2023    INT,
    interdits_2024    INT
);

-- 1. Revenu et marge par produit et par année civile en Ontario
SELECT YEAR(mois) AS annee, produit,
       SUM(mises_m) AS mises_m, SUM(revenu_m) AS revenu_m,
       ROUND(SUM(revenu_m) / SUM(mises_m), 3) AS taux_de_marge
FROM ontario_mensuel_produits
GROUP BY YEAR(mois), produit
ORDER BY annee, produit;

-- 2. Part de chaque produit dans les mises du mois, et évolution sur un an (fonctions de fenêtre)
WITH parts AS (
    SELECT mois, produit,
           mises_m / SUM(mises_m) OVER (PARTITION BY mois) AS part_mises
    FROM ontario_mensuel_produits
)
SELECT mois, produit, ROUND(part_mises, 3) AS part_mises,
       ROUND(part_mises - LAG(part_mises, 12) OVER (PARTITION BY produit ORDER BY mois), 3) AS ecart_sur_un_an
FROM parts
WHERE produit = 'Paris'
ORDER BY mois;

-- 3. Les 12 mois avant et après l'interdiction des athlètes dans les publicités (28 février 2024)
SELECT produit,
       SUM(CASE WHEN mois BETWEEN '2023-03-01' AND '2024-02-01' THEN mises_m END) AS mises_avant,
       SUM(CASE WHEN mois BETWEEN '2024-03-01' AND '2025-02-01' THEN mises_m END) AS mises_apres
FROM ontario_mensuel_produits
GROUP BY produit;

-- 4. Classement des départements par densité de parieurs sportifs
SELECT departement,
       ROUND(100 * parieurs / adultes, 1) AS densite_pct,
       RANK() OVER (ORDER BY parieurs / adultes DESC) AS rang
FROM france_departements
WHERE dep NOT LIKE '97%'
ORDER BY rang
LIMIT 10;

-- 5. Densité moyenne de parieurs par quart de la part des jeunes hommes
SELECT quart, COUNT(*) AS departements,
       ROUND(100 * SUM(parieurs) / SUM(adultes), 2) AS densite_pct
FROM (
    SELECT parieurs, adultes, NTILE(4) OVER (ORDER BY part_hommes_20_34) AS quart
    FROM france_departements
    WHERE part_hommes_20_34 IS NOT NULL
) q
GROUP BY quart
ORDER BY quart;

-- 6. Interdits pour 100 000 adultes et hausse 2023-2024, par département
SELECT dep,
       ROUND(100000 * interdits_2024 / adultes, 0) AS interdits_pour_100k,
       ROUND(100 * (interdits_2024 / interdits_2023 - 1), 0) AS hausse_pct
FROM france_interdits_departements
ORDER BY interdits_pour_100k DESC
LIMIT 10;
