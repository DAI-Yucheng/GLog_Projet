-- ============================================
-- 20 QUESTIONS SQL - ANALYSE DVF
-- ============================================

-- ============================================
-- ANALYSES TEMPORELLES
-- ============================================

-- Q1 : Évolution du prix moyen des ventes par mois
SELECT 
    DATE_FORMAT(date_mutation, '%Y-%m') as mois,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM MUTATION
GROUP BY DATE_FORMAT(date_mutation, '%Y-%m')
ORDER BY mois;

-- Q2 : Nombre de ventes par mois
SELECT 
    DATE_FORMAT(date_mutation, '%Y-%m') as mois,
    COUNT(*) as nb_ventes
FROM MUTATION
GROUP BY DATE_FORMAT(date_mutation, '%Y-%m')
ORDER BY mois;

-- Q3 : Mois avec le plus de transactions
SELECT 
    MONTH(date_mutation) as mois,
    COUNT(*) as nb_ventes
FROM MUTATION
GROUP BY MONTH(date_mutation)
ORDER BY nb_ventes DESC;

-- ============================================
-- ANALYSES GÉOGRAPHIQUES
-- ============================================

-- Q4 : Prix moyen par commune
SELECT 
    commune,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM BIEN
GROUP BY commune
ORDER BY prix_moyen DESC;

-- Q5 : Prix moyen par département
SELECT 
    code_departement,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM BIEN
GROUP BY code_departement
ORDER BY prix_moyen DESC;

-- Q6 : Nombre de transactions par commune
SELECT 
    commune,
    COUNT(DISTINCT no_disposition) as nb_transactions
FROM BIEN
GROUP BY commune
ORDER BY nb_transactions DESC;

-- ============================================
-- ANALYSES PAR TYPE DE BIEN
-- ============================================

-- Q7 : Prix moyen par type de local
SELECT 
    type_local,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL
GROUP BY type_local
ORDER BY prix_moyen DESC;

-- Q8 : Répartition des ventes par type de local
SELECT 
    type_local,
    COUNT(*) as nb_biens,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM BIEN WHERE type_local IS NOT NULL), 2) as pourcentage
FROM BIEN
WHERE type_local IS NOT NULL
GROUP BY type_local
ORDER BY nb_biens DESC;

-- Q9 : Surface moyenne par type de local
SELECT 
    type_local,
    AVG(surface_reelle_bati) as surface_moyenne,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL AND surface_reelle_bati > 0
GROUP BY type_local
ORDER BY surface_moyenne DESC;

-- ============================================
-- ANALYSES DE PRIX
-- ============================================

-- Q10 : Répartition des biens par tranche de prix
SELECT 
    CASE 
        WHEN valeur_fonciere < 100000 THEN '0-100k'
        WHEN valeur_fonciere < 200000 THEN '100-200k'
        WHEN valeur_fonciere < 300000 THEN '200-300k'
        WHEN valeur_fonciere < 500000 THEN '300-500k'
        ELSE '500k+'
    END as tranche_prix,
    COUNT(*) as nb_biens
FROM BIEN
GROUP BY 
    CASE 
        WHEN valeur_fonciere < 100000 THEN '0-100k'
        WHEN valeur_fonciere < 200000 THEN '100-200k'
        WHEN valeur_fonciere < 300000 THEN '200-300k'
        WHEN valeur_fonciere < 500000 THEN '300-500k'
        ELSE '500k+'
    END
ORDER BY MIN(valeur_fonciere);

-- Q11 : Prix moyen au m² par type de bien
SELECT 
    type_local,
    AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_m2_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL AND surface_reelle_bati > 0
GROUP BY type_local
ORDER BY prix_m2_moyen DESC;

-- Q12 : Prix moyen selon le nombre de pièces
SELECT 
    nombre_pieces_principales,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE nombre_pieces_principales > 0
GROUP BY nombre_pieces_principales
ORDER BY nombre_pieces_principales;

-- ============================================
-- ANALYSES DE CORRÉLATION
-- ============================================

-- Q13 : Relation surface/prix (pour scatter plot)
SELECT 
    surface_reelle_bati,
    valeur_fonciere,
    type_local
FROM BIEN
WHERE surface_reelle_bati > 0 AND surface_reelle_bati < 500
ORDER BY surface_reelle_bati;

-- Q14 : Relation nombre de pièces/prix (pour scatter plot)
SELECT 
    nombre_pieces_principales,
    valeur_fonciere,
    type_local
FROM BIEN
WHERE nombre_pieces_principales > 0 AND nombre_pieces_principales < 15
ORDER BY nombre_pieces_principales;

-- ============================================
-- ANALYSES DE MARCHÉ
-- ============================================

-- Q15 : Top 10 des ventes les plus chères
SELECT 
    commune,
    type_local,
    valeur_fonciere,
    surface_reelle_bati,
    nombre_pieces_principales,
    date_mutation
FROM BIEN
ORDER BY valeur_fonciere DESC
LIMIT 10;

-- Q16 : Répartition par nature de culture
SELECT 
    nature_culture,
    COUNT(*) as nb_biens,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM BIEN WHERE nature_culture IS NOT NULL), 2) as pourcentage
FROM BIEN
WHERE nature_culture IS NOT NULL
GROUP BY nature_culture
ORDER BY nb_biens DESC;

-- Q17 : Prix médian et prix moyen par commune
SELECT 
    commune,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM BIEN
GROUP BY commune
HAVING COUNT(*) >= 2
ORDER BY prix_moyen DESC;

-- Q18 : Proportion de biens avec/sans lots
SELECT 
    'Avec lots' as categorie,
    COUNT(*) as nb_biens
FROM DVF_IMPORT
WHERE nombre_lots > 0
UNION ALL
SELECT 
    'Sans lots',
    COUNT(*)
FROM DVF_IMPORT
WHERE nombre_lots = 0 OR nombre_lots IS NULL;

-- Q19 : Surface terrain moyenne par commune
SELECT 
    commune,
    AVG(surface_terrain) as surface_terrain_moyenne,
    COUNT(*) as nb_biens
FROM BIEN
WHERE surface_terrain > 0
GROUP BY commune
ORDER BY surface_terrain_moyenne DESC;

-- Q20 : Évolution du prix au m² dans le temps
SELECT 
    DATE_FORMAT(date_mutation, '%Y-%m') as mois,
    AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_m2_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE surface_reelle_bati > 0
GROUP BY DATE_FORMAT(date_mutation, '%Y-%m')
ORDER BY mois;

-- ============================================
-- REQUÊTES BONUS - ANALYSES COMPLÉMENTAIRES
-- ============================================

-- Distribution des surfaces habitables
SELECT 
    CASE 
        WHEN surface_reelle_bati < 50 THEN '0-50 m²'
        WHEN surface_reelle_bati < 100 THEN '50-100 m²'
        WHEN surface_reelle_bati < 150 THEN '100-150 m²'
        WHEN surface_reelle_bati < 200 THEN '150-200 m²'
        ELSE '200+ m²'
    END as tranche_surface,
    COUNT(*) as nb_biens
FROM BIEN
WHERE surface_reelle_bati > 0
GROUP BY 
    CASE 
        WHEN surface_reelle_bati < 50 THEN '0-50 m²'
        WHEN surface_reelle_bati < 100 THEN '50-100 m²'
        WHEN surface_reelle_bati < 150 THEN '100-150 m²'
        WHEN surface_reelle_bati < 200 THEN '150-200 m²'
        ELSE '200+ m²'
    END
ORDER BY MIN(surface_reelle_bati);

-- Statistiques globales
SELECT 
    COUNT(*) as total_ventes,
    AVG(valeur_fonciere) as prix_moyen,
    MIN(valeur_fonciere) as prix_min,
    MAX(valeur_fonciere) as prix_max,
    AVG(surface_reelle_bati) as surface_moyenne
FROM BIEN;