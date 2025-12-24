import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="userP6",
    password="mdpP6",
    database="foncieres"
)

cursor = mydb.cursor()

# ============================================
# Q1 : Évolution du prix moyen par mois
# ============================================
query1 = """
SELECT 
    DATE_FORMAT(date_mutation, '%Y-%m') as mois,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM MUTATION
GROUP BY DATE_FORMAT(date_mutation, '%Y-%m')
ORDER BY mois
"""
df1 = pd.read_sql(query1, mydb)
fig1 = px.line(df1, x='mois', y='prix_moyen', 
               title='Évolution du prix moyen des ventes par mois',
               labels={'mois': 'Mois', 'prix_moyen': 'Prix moyen (€)'})
fig1.show()

# ============================================
# Q2 : Nombre de ventes par mois
# ============================================
query2 = """
SELECT 
    DATE_FORMAT(date_mutation, '%Y-%m') as mois,
    COUNT(*) as nb_ventes
FROM MUTATION
GROUP BY DATE_FORMAT(date_mutation, '%Y-%m')
ORDER BY mois
"""
df2 = pd.read_sql(query2, mydb)
fig2 = px.bar(df2, x='mois', y='nb_ventes',
              title='Nombre de ventes par mois',
              labels={'mois': 'Mois', 'nb_ventes': 'Nombre de ventes'})
fig2.show()

# ============================================
# Q4 : Prix moyen par commune
# ============================================
query4 = """
SELECT 
    commune,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM BIEN
GROUP BY commune
ORDER BY prix_moyen DESC
LIMIT 10
"""
df4 = pd.read_sql(query4, mydb)
fig4 = px.bar(df4, x='prix_moyen', y='commune', orientation='h',
              title='Top 10 - Prix moyen par commune',
              labels={'commune': 'Commune', 'prix_moyen': 'Prix moyen (€)'})
fig4.show()

# ============================================
# Q5 : Prix moyen par département
# ============================================
query5 = """
SELECT 
    code_departement,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_ventes
FROM BIEN
GROUP BY code_departement
ORDER BY prix_moyen DESC
"""
df5 = pd.read_sql(query5, mydb)
fig5 = px.bar(df5, x='code_departement', y='prix_moyen',
              title='Prix moyen par département',
              labels={'code_departement': 'Département', 'prix_moyen': 'Prix moyen (€)'})
fig5.show()

# ============================================
# Q6 : Nombre de transactions par commune
# ============================================
query6 = """
SELECT 
    commune,
    COUNT(DISTINCT no_disposition) as nb_transactions
FROM BIEN
GROUP BY commune
ORDER BY nb_transactions DESC
LIMIT 10
"""
df6 = pd.read_sql(query6, mydb)
fig6 = px.bar(df6, x='nb_transactions', y='commune', orientation='h',
              title='Top 10 - Communes avec le plus de transactions',
              labels={'commune': 'Commune', 'nb_transactions': 'Nombre de transactions'})
fig6.show()

# ============================================
# Q7 : Prix moyen par type de local
# ============================================
query7 = """
SELECT 
    type_local,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL
GROUP BY type_local
ORDER BY prix_moyen DESC
"""
df7 = pd.read_sql(query7, mydb)
fig7 = px.bar(df7, x='type_local', y='prix_moyen',
              title='Prix moyen par type de local',
              labels={'type_local': 'Type de local', 'prix_moyen': 'Prix moyen (€)'})
fig7.show()

# ============================================
# Q8 : Répartition des ventes par type de local
# ============================================
query8 = """
SELECT 
    type_local,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL
GROUP BY type_local
ORDER BY nb_biens DESC
"""
df8 = pd.read_sql(query8, mydb)
fig8 = px.pie(df8, values='nb_biens', names='type_local',
              title='Répartition des ventes par type de local')
fig8.show()

# ============================================
# Q9 : Surface moyenne par type de local
# ============================================
query9 = """
SELECT 
    type_local,
    AVG(surface_reelle_bati) as surface_moyenne,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL AND surface_reelle_bati > 0
GROUP BY type_local
ORDER BY surface_moyenne DESC
"""
df9 = pd.read_sql(query9, mydb)
fig9 = px.bar(df9, x='type_local', y='surface_moyenne',
              title='Surface moyenne par type de local',
              labels={'type_local': 'Type de local', 'surface_moyenne': 'Surface moyenne (m²)'})
fig9.show()

# ============================================
# Q10 : Répartition par tranche de prix
# ============================================
query10 = """
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
ORDER BY MIN(valeur_fonciere)
"""
df10 = pd.read_sql(query10, mydb)
fig10 = px.histogram(df10, x='tranche_prix', y='nb_biens',
                     title='Distribution des biens par tranche de prix',
                     labels={'tranche_prix': 'Tranche de prix', 'nb_biens': 'Nombre de biens'})
fig10.show()

# ============================================
# Q11 : Prix au m² par type de bien
# ============================================
query11 = """
SELECT 
    type_local,
    AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_m2_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE type_local IS NOT NULL AND surface_reelle_bati > 0
GROUP BY type_local
ORDER BY prix_m2_moyen DESC
"""
df11 = pd.read_sql(query11, mydb)
fig11 = px.bar(df11, x='type_local', y='prix_m2_moyen',
               title='Prix moyen au m² par type de bien',
               labels={'type_local': 'Type de local', 'prix_m2_moyen': 'Prix au m² (€/m²)'})
fig11.show()

# ============================================
# Q12 : Prix selon le nombre de pièces
# ============================================
query12 = """
SELECT 
    nombre_pieces_principales,
    AVG(valeur_fonciere) as prix_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE nombre_pieces_principales > 0
GROUP BY nombre_pieces_principales
ORDER BY nombre_pieces_principales
"""
df12 = pd.read_sql(query12, mydb)
fig12 = px.line(df12, x='nombre_pieces_principales', y='prix_moyen', markers=True,
                title='Prix moyen selon le nombre de pièces',
                labels={'nombre_pieces_principales': 'Nombre de pièces', 'prix_moyen': 'Prix moyen (€)'})
fig12.show()

# ============================================
# Q13 : Corrélation surface/prix
# ============================================
query13 = """
SELECT 
    surface_reelle_bati,
    valeur_fonciere,
    type_local
FROM BIEN
WHERE surface_reelle_bati > 0 AND surface_reelle_bati < 500
"""
df13 = pd.read_sql(query13, mydb)
fig13 = px.scatter(df13, x='surface_reelle_bati', y='valeur_fonciere', color='type_local',
                   title='Corrélation entre surface et prix',
                   labels={'surface_reelle_bati': 'Surface (m²)', 'valeur_fonciere': 'Prix (€)'})
fig13.show()

# ============================================
# Q14 : Corrélation nombre de pièces/prix
# ============================================
query14 = """
SELECT 
    nombre_pieces_principales,
    valeur_fonciere,
    type_local
FROM BIEN
WHERE nombre_pieces_principales > 0 AND nombre_pieces_principales < 15
"""
df14 = pd.read_sql(query14, mydb)
fig14 = px.scatter(df14, x='nombre_pieces_principales', y='valeur_fonciere', color='type_local',
                   title='Corrélation entre nombre de pièces et prix',
                   labels={'nombre_pieces_principales': 'Nombre de pièces', 'valeur_fonciere': 'Prix (€)'})
fig14.show()

# ============================================
# Q15 : Top 10 des ventes les plus chères
# ============================================
query15 = """
SELECT 
    commune,
    type_local,
    valeur_fonciere,
    surface_reelle_bati,
    nombre_pieces_principales
FROM BIEN
ORDER BY valeur_fonciere DESC
LIMIT 10
"""
df15 = pd.read_sql(query15, mydb)
df15['description'] = df15['commune'] + ' - ' + df15['type_local'].fillna('N/A')
fig15 = px.bar(df15, x='valeur_fonciere', y='description', orientation='h',
               title='Top 10 des ventes les plus chères',
               labels={'description': '', 'valeur_fonciere': 'Prix (€)'})
fig15.show()

# ============================================
# Q16 : Répartition par nature de culture
# ============================================
query16 = """
SELECT 
    nature_culture,
    COUNT(*) as nb_biens
FROM BIEN
WHERE nature_culture IS NOT NULL
GROUP BY nature_culture
ORDER BY nb_biens DESC
"""
df16 = pd.read_sql(query16, mydb)
fig16 = px.pie(df16, values='nb_biens', names='nature_culture',
               title='Répartition par nature de culture')
fig16.show()


# ============================================
# Q18 : Biens avec/sans lots
# ============================================
query18 = """
SELECT 
    CASE 
        WHEN nombre_lots > 0 THEN 'Avec lots'
        ELSE 'Sans lots'
    END as categorie,
    COUNT(*) as nb_biens
FROM DVF_IMPORT
GROUP BY 
    CASE 
        WHEN nombre_lots > 0 THEN 'Avec lots'
        ELSE 'Sans lots'
    END
"""
df18 = pd.read_sql(query18, mydb)
fig18 = px.pie(df18, values='nb_biens', names='categorie',
               title='Proportion de biens avec/sans lots (copropriété)')
fig18.show()

# ============================================
# Q19 : Surface terrain moyenne par commune
# ============================================
query19 = """
SELECT 
    commune,
    AVG(surface_terrain) as surface_terrain_moyenne,
    COUNT(*) as nb_biens
FROM BIEN
WHERE surface_terrain > 0
GROUP BY commune
ORDER BY surface_terrain_moyenne DESC
LIMIT 10
"""
df19 = pd.read_sql(query19, mydb)
fig19 = px.bar(df19, x='surface_terrain_moyenne', y='commune', orientation='h',
               title='Top 10 - Surface terrain moyenne par commune',
               labels={'commune': 'Commune', 'surface_terrain_moyenne': 'Surface moyenne (m²)'})
fig19.show()

# ============================================
# Q20 : Évolution du prix au m² dans le temps
# ============================================
query20 = """
SELECT 
    DATE_FORMAT(date_mutation, '%Y-%m') as mois,
    AVG(valeur_fonciere / NULLIF(surface_reelle_bati, 0)) as prix_m2_moyen,
    COUNT(*) as nb_biens
FROM BIEN
WHERE surface_reelle_bati > 0
GROUP BY DATE_FORMAT(date_mutation, '%Y-%m')
ORDER BY mois
"""
df20 = pd.read_sql(query20, mydb)
fig20 = px.line(df20, x='mois', y='prix_m2_moyen',
                title='Évolution du prix au m² dans le temps',
                labels={'mois': 'Mois', 'prix_m2_moyen': 'Prix au m² (€/m²)'})
fig20.show()

# Fermeture de la connexion
cursor.close()
mydb.close()

print("Tous les graphiques ont été générés avec succès !")