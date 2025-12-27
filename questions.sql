-- ============================================
-- SCRIPT SQL - 20 QUESTIONS ANALYTIQUES DVF
-- Base de données : foncieres
-- ============================================

USE foncieres;

-- ============================================
-- QUESTIONS SUR LES VALEURS ET VOLUMES
-- ============================================

-- Question 1 : Évolution du nombre de mutations par mois
-- Type de graphe : Courbe temporelle
SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
       COUNT(*) as nombre_mutations
FROM MUTATION
GROUP BY mois
ORDER BY mois;

-- Question 2 : Distribution des valeurs foncières par tranche
-- Type de graphe : Histogramme
SELECT 
    CASE 
        WHEN valeur_fonciere < 100000 THEN '0-100k'
        WHEN valeur_fonciere < 200000 THEN '100k-200k'
        WHEN valeur_fonciere < 300000 THEN '200k-300k'
        WHEN valeur_fonciere < 500000 THEN '300k-500k'
        ELSE '500k+'
    END as tranche,
    COUNT(*) as nombre
FROM MUTATION
WHERE valeur_fonciere IS NOT NULL
GROUP BY tranche
ORDER BY MIN(valeur_fonciere);

-- Question 3 : Valeur foncière moyenne par nature de mutation
-- Type de graphe : Diagramme en barres horizontales
SELECT nm.nature_mutation, 
       AVG(m.valeur_fonciere) as valeur_moyenne
FROM MUTATION m
JOIN NATURE_MUTATION nm ON m.id_nature_mutation = nm.id_nature_mutation
WHERE m.valeur_fonciere IS NOT NULL
GROUP BY nm.nature_mutation
ORDER BY valeur_moyenne DESC;

-- ============================================
-- QUESTIONS SUR LES TYPES DE BIENS
-- ============================================

-- Question 4 : Répartition des biens par type de local
-- Type de graphe : Diagramme circulaire (camembert)
SELECT tl.type_local, 
       COUNT(*) as nombre
FROM BIEN b
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE tl.type_local IS NOT NULL
GROUP BY tl.type_local
ORDER BY nombre DESC;

-- Question 5 : Prix moyen au m² par type de local
-- Type de graphe : Diagramme en barres
SELECT tl.type_local, 
       AVG(m.valeur_fonciere / b.surface_reelle_bati) as prix_m2
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE b.surface_reelle_bati > 0 
  AND m.valeur_fonciere IS NOT NULL
GROUP BY tl.type_local
ORDER BY prix_m2 DESC;

-- Question 6 : Distribution du nombre de pièces principales
-- Type de graphe : Histogramme
SELECT nombre_pieces_principales, 
       COUNT(*) as nombre_biens
FROM BIEN
WHERE nombre_pieces_principales IS NOT NULL
GROUP BY nombre_pieces_principales
ORDER BY nombre_pieces_principales;

-- ============================================
-- QUESTIONS GÉOGRAPHIQUES
-- ============================================

-- Question 7 : Top 10 des communes par nombre de transactions
-- Type de graphe : Diagramme en barres horizontales
SELECT c.commune, 
       COUNT(DISTINCT m.id_mutation) as nb_transactions
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN COMMUNE c ON b.id_commune = c.id_commune
GROUP BY c.commune
ORDER BY nb_transactions DESC
LIMIT 10;

-- Question 8 : Valeur foncière moyenne par département
-- Type de graphe : Carte choroplèthe ou diagramme en barres
SELECT d.code_departement, 
       AVG(m.valeur_fonciere) as valeur_moyenne
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN COMMUNE c ON b.id_commune = c.id_commune
JOIN DEPARTEMENT d ON c.code_departement = d.code_departement
WHERE m.valeur_fonciere IS NOT NULL
GROUP BY d.code_departement
ORDER BY valeur_moyenne DESC;

-- Question 9 : Volume de transactions par code postal
-- Type de graphe : Diagramme en barres
SELECT c.code_postal, 
       COUNT(*) as nombre_transactions
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN COMMUNE c ON b.id_commune = c.id_commune
WHERE c.code_postal IS NOT NULL
GROUP BY c.code_postal
ORDER BY nombre_transactions DESC
LIMIT 15;

-- ============================================
-- QUESTIONS SUR LES SURFACES
-- ============================================

-- Question 10 : Distribution des surfaces bâties
-- Type de graphe : Histogramme avec intervalles
SELECT 
    CASE 
        WHEN surface_reelle_bati < 50 THEN '0-50m²'
        WHEN surface_reelle_bati < 100 THEN '50-100m²'
        WHEN surface_reelle_bati < 150 THEN '100-150m²'
        WHEN surface_reelle_bati < 200 THEN '150-200m²'
        ELSE '200m²+'
    END as tranche_surface,
    COUNT(*) as nombre
FROM BIEN
WHERE surface_reelle_bati IS NOT NULL
GROUP BY tranche_surface
ORDER BY MIN(surface_reelle_bati);

-- Question 11 : Corrélation surface bâtie vs valeur foncière
-- Type de graphe : Nuage de points (scatter plot)
SELECT b.surface_reelle_bati, 
       m.valeur_fonciere
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
WHERE b.surface_reelle_bati IS NOT NULL 
  AND b.surface_reelle_bati > 0
  AND m.valeur_fonciere IS NOT NULL
  AND m.valeur_fonciere < 1000000
LIMIT 500;

-- Question 12 : Surface terrain moyenne par nature de culture
-- Type de graphe : Diagramme en barres
SELECT nc.code_nature_culture, 
       AVG(b.surface_terrain) as surface_moyenne
FROM BIEN b
JOIN NATURE_CULTURE nc ON b.nature_culture = nc.code_nature_culture
WHERE b.surface_terrain IS NOT NULL 
  AND b.surface_terrain > 0
GROUP BY nc.code_nature_culture
ORDER BY surface_moyenne DESC;

-- ============================================
-- QUESTIONS SUR LES PRIX
-- ============================================

-- Question 13 : Évolution du prix moyen mensuel
-- Type de graphe : Courbe temporelle
SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
       AVG(valeur_fonciere) as prix_moyen
FROM MUTATION
WHERE valeur_fonciere IS NOT NULL
GROUP BY mois
ORDER BY mois;

-- Question 14 : Comparaison prix moyen par type de bien
-- Type de graphe : Diagramme en barres groupées
SELECT tl.type_local,
       AVG(m.valeur_fonciere) as prix_moyen,
       MIN(m.valeur_fonciere) as prix_min,
       MAX(m.valeur_fonciere) as prix_max
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE m.valeur_fonciere IS NOT NULL
GROUP BY tl.type_local, tl.id_type_local
ORDER BY prix_moyen DESC;

-- Question 15 : Distribution des prix pour les maisons vs appartements
-- Type de graphe : Box plot ou histogrammes comparés
SELECT tl.type_local, 
       m.valeur_fonciere
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE tl.type_local IN ('Maison', 'Appartement')
  AND m.valeur_fonciere IS NOT NULL
  AND m.valeur_fonciere < 800000;

-- ============================================
-- QUESTIONS ANALYTIQUES AVANCÉES
-- ============================================

-- Question 16 : Ratio surface terrain / surface bâtie par commune
-- Type de graphe : Diagramme en barres
SELECT c.commune,
       AVG(b.surface_terrain / NULLIF(b.surface_reelle_bati, 0)) as ratio_moyen
FROM BIEN b
JOIN COMMUNE c ON b.id_commune = c.id_commune
WHERE b.surface_terrain > 0 
  AND b.surface_reelle_bati > 0
GROUP BY c.commune
HAVING COUNT(*) > 5
ORDER BY ratio_moyen DESC
LIMIT 10;

-- Question 17 : Nombre de biens par transaction
-- Type de graphe : Histogramme
SELECT nb_biens, 
       COUNT(*) as nb_mutations
FROM (
    SELECT m.id_mutation, 
           COUNT(mb.id_bien) as nb_biens
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    GROUP BY m.id_mutation
) as subq
GROUP BY nb_biens
ORDER BY nb_biens;

-- Question 18 : Pourcentage de biens avec/sans terrain par type
-- Type de graphe : Diagramme en barres empilées (stacked bar)
SELECT tl.type_local,
       SUM(CASE WHEN b.surface_terrain > 0 THEN 1 ELSE 0 END) as avec_terrain,
       SUM(CASE WHEN b.surface_terrain IS NULL OR b.surface_terrain = 0 THEN 1 ELSE 0 END) as sans_terrain
FROM BIEN b
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE tl.type_local IS NOT NULL
GROUP BY tl.type_local;

-- ============================================
-- QUESTIONS TEMPORELLES
-- ============================================

-- Question 19 : Transactions par jour de la semaine
-- Type de graphe : Diagramme en barres
SELECT DAYNAME(date_mutation) as jour_semaine,
       DAYOFWEEK(date_mutation) as jour_num,
       COUNT(*) as nombre_transactions
FROM MUTATION
GROUP BY jour_semaine, jour_num
ORDER BY jour_num;

-- Question 20 : Comparaison volumes de ventes par semaine
-- Type de graphe : Courbe temporelle
SELECT YEARWEEK(date_mutation) as semaine,
       COUNT(*) as nb_transactions,
       SUM(valeur_fonciere) as volume_total,
       AVG(valeur_fonciere) as moyenne_transaction
FROM MUTATION
WHERE valeur_fonciere IS NOT NULL
GROUP BY semaine
ORDER BY semaine;
