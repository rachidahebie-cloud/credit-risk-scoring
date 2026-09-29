-- Q1 : Vue d'ensemble du portefeuille
SELECT
    COUNT(*)                                   AS nb_clients,
    SUM(SeriousDlqin2yrs)                      AS nb_defauts,
    ROUND(100.0 * AVG(SeriousDlqin2yrs), 2)    AS taux_defaut_pct
FROM credit;

-- Q2 : Taux de defaut par tranche d'age
SELECT
    CASE
        WHEN age < 30 THEN '1. moins de 30'
        WHEN age < 40 THEN '2. 30-39'
        WHEN age < 50 THEN '3. 40-49'
        WHEN age < 60 THEN '4. 50-59'
        WHEN age < 70 THEN '5. 60-69'
        ELSE '6. 70 et plus'
    END AS tranche_age,
    COUNT(*)                                   AS nb_clients,
    SUM(SeriousDlqin2yrs)                      AS nb_defauts,
    ROUND(100.0 * AVG(SeriousDlqin2yrs), 2)    AS taux_defaut_pct
FROM credit
GROUP BY tranche_age
ORDER BY tranche_age;

-- Q3 : Taux de defaut par tranche de revenu, compare au taux global (CTE)
WITH stats_globales AS (
    SELECT AVG(SeriousDlqin2yrs) AS taux_global
    FROM credit
),
segments AS (
    SELECT
        CASE
            WHEN MonthlyIncome < 2500 THEN '1. moins de 2500'
            WHEN MonthlyIncome < 5000 THEN '2. 2500-4999'
            WHEN MonthlyIncome < 8000 THEN '3. 5000-7999'
            ELSE '4. 8000 et plus'
        END AS tranche_revenu,
        COUNT(*)                 AS nb_clients,
        AVG(SeriousDlqin2yrs)    AS taux_defaut
    FROM credit
    GROUP BY tranche_revenu
)
SELECT
    s.tranche_revenu,
    s.nb_clients,
    ROUND(100.0 * s.taux_defaut, 2)          AS taux_defaut_pct,
    ROUND(s.taux_defaut / g.taux_global, 2)  AS ratio_vs_global
FROM segments s
CROSS JOIN stats_globales g
ORDER BY s.tranche_revenu;

-- Q4 : Taux de defaut par decile d'utilisation du credit renouvelable (NTILE)
WITH deciles AS (
    SELECT
        SeriousDlqin2yrs,
        NTILE(10) OVER (ORDER BY RevolvingUtilizationOfUnsecuredLines) AS decile
    FROM credit
)
SELECT
    decile,
    COUNT(*)                                   AS nb_clients,
    ROUND(100.0 * AVG(SeriousDlqin2yrs), 2)    AS taux_defaut_pct
FROM deciles
GROUP BY decile
ORDER BY decile;

-- Q5 : Classement des decennies d'age par niveau de risque (RANK)
WITH par_decennie AS (
    SELECT
        CAST(FLOOR(age / 10.0) * 10 AS SIGNED)    AS decennie,
        COUNT(*)                                   AS nb_clients,
        ROUND(100.0 * AVG(SeriousDlqin2yrs), 2)    AS taux_defaut_pct
    FROM credit
    GROUP BY decennie
)
SELECT
    decennie,
    nb_clients,
    taux_defaut_pct,
    RANK() OVER (ORDER BY taux_defaut_pct DESC) AS rang_risque
FROM par_decennie
ORDER BY rang_risque;

-- Q6 : Impact de l'historique de retards de plus de 90 jours
SELECT
    CASE
        WHEN NumberOfTimes90DaysLate = 0 THEN '0 retard'
        WHEN NumberOfTimes90DaysLate = 1 THEN '1 retard'
        WHEN NumberOfTimes90DaysLate = 2 THEN '2 retards'
        ELSE '3 retards ou plus'
    END AS retards_90j,
    COUNT(*)                                   AS nb_clients,
    ROUND(100.0 * AVG(SeriousDlqin2yrs), 2)    AS taux_defaut_pct
FROM credit
GROUP BY retards_90j
ORDER BY taux_defaut_pct;

-- Q7 : Courbe de gain - part cumulee des defauts captures en ciblant les clients les plus utilisateurs de credit (SUM OVER)
WITH deciles AS (
    SELECT
        SeriousDlqin2yrs,
        NTILE(10) OVER (ORDER BY RevolvingUtilizationOfUnsecuredLines DESC) AS decile
    FROM credit
),
agregat AS (
    SELECT
        decile,
        COUNT(*)                 AS nb_clients,
        SUM(SeriousDlqin2yrs)    AS nb_defauts
    FROM deciles
    GROUP BY decile
)
SELECT
    decile,
    nb_clients,
    nb_defauts,
    ROUND(100.0 * SUM(nb_defauts) OVER (ORDER BY decile) / SUM(nb_defauts) OVER (), 2) AS pct_defauts_captures_cumule
FROM agregat
ORDER BY decile;