import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="userP6",
    password="mdpP6",
    database="foncieres"
)

print("Connexion réussie à la base de données!")

# ============================================
# QUESTION 1 : Évolution du nombre de mutations par mois
# ============================================
query1 = """
SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
       COUNT(*) as nombre_mutations
FROM MUTATION
GROUP BY mois
ORDER BY mois;
"""
df1 = pd.read_sql(query1, mydb)
fig1 = px.line(df1, x='mois', y='nombre_mutations', 
               title='Q1: Évolution du nombre de mutations par mois',
               labels={'mois': 'Mois', 'nombre_mutations': 'Nombre de mutations'})
fig1.update_traces(mode='lines+markers')
fig1.show()

# ============================================
# QUESTION 2 : Distribution des valeurs foncières par tranche
# ============================================
query2 = """
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
"""
df2 = pd.read_sql(query2, mydb)
fig2 = px.bar(df2, x='tranche', y='nombre', 
              title='Q2: Distribution des valeurs foncières par tranche',
              labels={'tranche': 'Tranche de prix', 'nombre': 'Nombre de mutations'})
fig2.show()

# ============================================
# QUESTION 3 : Valeur foncière moyenne par nature de mutation
# ============================================
query3 = """
SELECT nm.nature_mutation, 
       AVG(m.valeur_fonciere) as valeur_moyenne
FROM MUTATION m
JOIN NATURE_MUTATION nm ON m.id_nature_mutation = nm.id_nature_mutation
WHERE m.valeur_fonciere IS NOT NULL
GROUP BY nm.nature_mutation
ORDER BY valeur_moyenne DESC;
"""
df3 = pd.read_sql(query3, mydb)
fig3 = px.bar(df3, x='valeur_moyenne', y='nature_mutation', orientation='h',
              title='Q3: Valeur foncière moyenne par nature de mutation',
              labels={'valeur_moyenne': 'Valeur moyenne (€)', 'nature_mutation': 'Nature de mutation'})
fig3.show()

# ============================================
# QUESTION 4 : Répartition des biens par type de local
# ============================================
query4 = """
SELECT tl.type_local, 
       COUNT(*) as nombre
FROM BIEN b
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE tl.type_local IS NOT NULL
GROUP BY tl.type_local
ORDER BY nombre DESC;
"""
df4 = pd.read_sql(query4, mydb)
fig4 = px.pie(df4, values='nombre', names='type_local', 
              title='Q4: Répartition des biens par type de local')
fig4.show()

# ============================================
# QUESTION 5 : Prix moyen au m² par type de local
# ============================================
query5 = """
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
"""
df5 = pd.read_sql(query5, mydb)
fig5 = px.bar(df5, x='type_local', y='prix_m2', 
              title='Q5: Prix moyen au m² par type de local',
              labels={'type_local': 'Type de local', 'prix_m2': 'Prix au m² (€)'})
fig5.show()

# ============================================
# QUESTION 6 : Distribution du nombre de pièces principales
# ============================================
query6 = """
SELECT nombre_pieces_principales, 
       COUNT(*) as nombre_biens
FROM BIEN
WHERE nombre_pieces_principales IS NOT NULL
GROUP BY nombre_pieces_principales
ORDER BY nombre_pieces_principales;
"""
df6 = pd.read_sql(query6, mydb)
fig6 = px.bar(df6, x='nombre_pieces_principales', y='nombre_biens', 
              title='Q6: Distribution du nombre de pièces principales',
              labels={'nombre_pieces_principales': 'Nombre de pièces', 'nombre_biens': 'Nombre de biens'})
fig6.show()

# ============================================
# QUESTION 7 : Top 10 des communes par nombre de transactions
# ============================================
query7 = """
SELECT c.commune, 
       COUNT(DISTINCT m.id_mutation) as nb_transactions
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN COMMUNE c ON b.id_commune = c.id_commune
GROUP BY c.commune
ORDER BY nb_transactions DESC
LIMIT 10;
"""
df7 = pd.read_sql(query7, mydb)
fig7 = px.bar(df7, x='nb_transactions', y='commune', orientation='h',
              title='Q7: Top 10 des communes par nombre de transactions',
              labels={'nb_transactions': 'Nombre de transactions', 'commune': 'Commune'})
fig7.show()

# ============================================
# QUESTION 8 : Valeur foncière moyenne par département
# ============================================
query8 = """
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
"""
df8 = pd.read_sql(query8, mydb)
fig8 = px.bar(df8, x='code_departement', y='valeur_moyenne', 
              title='Q8: Valeur foncière moyenne par département',
              labels={'code_departement': 'Département', 'valeur_moyenne': 'Valeur moyenne (€)'})
fig8.show()

# ============================================
# QUESTION 9 : Volume de transactions par code postal
# ============================================
query9 = """
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
"""
df9 = pd.read_sql(query9, mydb)
fig9 = px.bar(df9, x='code_postal', y='nombre_transactions', 
              title='Q9: Top 15 des codes postaux par nombre de transactions',
              labels={'code_postal': 'Code postal', 'nombre_transactions': 'Nombre de transactions'})
fig9.show()

# ============================================
# QUESTION 10 : Distribution des surfaces bâties
# ============================================
query10 = """
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
"""
df10 = pd.read_sql(query10, mydb)
fig10 = px.bar(df10, x='tranche_surface', y='nombre', 
               title='Q10: Distribution des surfaces bâties',
               labels={'tranche_surface': 'Tranche de surface', 'nombre': 'Nombre de biens'})
fig10.show()

# ============================================
# QUESTION 11 : Corrélation surface bâtie vs valeur foncière
# ============================================
query11 = """
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
"""
df11 = pd.read_sql(query11, mydb)
fig11 = px.scatter(df11, x='surface_reelle_bati', y='valeur_fonciere', 
                   title='Q11: Corrélation surface bâtie vs valeur foncière',
                   labels={'surface_reelle_bati': 'Surface bâtie (m²)', 'valeur_fonciere': 'Valeur foncière (€)'},
                   trendline="ols")
fig11.show()

# ============================================
# QUESTION 12 : Surface terrain moyenne par nature de culture
# ============================================
query12 = """
SELECT nc.code_nature_culture, 
       AVG(b.surface_terrain) as surface_moyenne
FROM BIEN b
JOIN NATURE_CULTURE nc ON b.nature_culture = nc.code_nature_culture
WHERE b.surface_terrain IS NOT NULL 
  AND b.surface_terrain > 0
GROUP BY nc.code_nature_culture
ORDER BY surface_moyenne DESC;
"""
df12 = pd.read_sql(query12, mydb)
fig12 = px.bar(df12, x='code_nature_culture', y='surface_moyenne', 
               title='Q12: Surface terrain moyenne par nature de culture',
               labels={'code_nature_culture': 'Nature de culture', 'surface_moyenne': 'Surface moyenne (m²)'})
fig12.show()

# ============================================
# QUESTION 13 : Évolution du prix moyen mensuel
# ============================================
query13 = """
SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
       AVG(valeur_fonciere) as prix_moyen
FROM MUTATION
WHERE valeur_fonciere IS NOT NULL
GROUP BY mois
ORDER BY mois;
"""
df13 = pd.read_sql(query13, mydb)
fig13 = px.line(df13, x='mois', y='prix_moyen', 
                title='Q13: Évolution du prix moyen mensuel',
                labels={'mois': 'Mois', 'prix_moyen': 'Prix moyen (€)'})
fig13.update_traces(mode='lines+markers')
fig13.show()

# ============================================
# QUESTION 14 : Comparaison prix moyen par type de bien
# ============================================
query14 = """
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
"""
df14 = pd.read_sql(query14, mydb)
fig14 = go.Figure()
fig14.add_trace(go.Bar(name='Prix moyen', x=df14['type_local'], y=df14['prix_moyen']))
fig14.add_trace(go.Bar(name='Prix min', x=df14['type_local'], y=df14['prix_min']))
fig14.add_trace(go.Bar(name='Prix max', x=df14['type_local'], y=df14['prix_max']))
fig14.update_layout(title='Q14: Comparaison des prix par type de bien',
                    xaxis_title='Type de local',
                    yaxis_title='Prix (€)',
                    barmode='group')
fig14.show()

# ============================================
# QUESTION 15 : Distribution des prix pour maisons vs appartements
# ============================================
query15 = """
SELECT tl.type_local, 
       m.valeur_fonciere
FROM MUTATION m
JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
JOIN BIEN b ON mb.id_bien = b.id_bien
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE tl.type_local IN ('Maison', 'Appartement')
  AND m.valeur_fonciere IS NOT NULL
  AND m.valeur_fonciere < 800000;
"""
df15 = pd.read_sql(query15, mydb)
fig15 = px.box(df15, x='type_local', y='valeur_fonciere', 
               title='Q15: Distribution des prix - Maisons vs Appartements',
               labels={'type_local': 'Type de bien', 'valeur_fonciere': 'Valeur foncière (€)'})
fig15.show()

# ============================================
# QUESTION 16 : Ratio surface terrain / surface bâtie par commune
# ============================================
query16 = """
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
"""
df16 = pd.read_sql(query16, mydb)
fig16 = px.bar(df16, x='ratio_moyen', y='commune', orientation='h',
               title='Q16: Top 10 ratio surface terrain/surface bâtie par commune',
               labels={'ratio_moyen': 'Ratio moyen', 'commune': 'Commune'})
fig16.show()

# ============================================
# QUESTION 17 : Nombre de biens par transaction
# ============================================
query17 = """
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
"""
df17 = pd.read_sql(query17, mydb)
fig17 = px.bar(df17, x='nb_biens', y='nb_mutations', 
               title='Q17: Nombre de biens par transaction',
               labels={'nb_biens': 'Nombre de biens', 'nb_mutations': 'Nombre de mutations'})
fig17.show()

# ============================================
# QUESTION 18 : Pourcentage de biens avec/sans terrain par type
# ============================================
query18 = """
SELECT tl.type_local,
       SUM(CASE WHEN b.surface_terrain > 0 THEN 1 ELSE 0 END) as avec_terrain,
       SUM(CASE WHEN b.surface_terrain IS NULL OR b.surface_terrain = 0 THEN 1 ELSE 0 END) as sans_terrain
FROM BIEN b
JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
WHERE tl.type_local IS NOT NULL
GROUP BY tl.type_local;
"""
df18 = pd.read_sql(query18, mydb)
fig18 = go.Figure()
fig18.add_trace(go.Bar(name='Avec terrain', x=df18['type_local'], y=df18['avec_terrain']))
fig18.add_trace(go.Bar(name='Sans terrain', x=df18['type_local'], y=df18['sans_terrain']))
fig18.update_layout(title='Q18: Biens avec/sans terrain par type',
                    xaxis_title='Type de local',
                    yaxis_title='Nombre de biens',
                    barmode='stack')
fig18.show()

# ============================================
# QUESTION 19 : Transactions par jour de la semaine
# ============================================
query19 = """
SELECT DAYNAME(date_mutation) as jour_semaine,
       DAYOFWEEK(date_mutation) as jour_num,
       COUNT(*) as nombre_transactions
FROM MUTATION
GROUP BY jour_semaine, jour_num
ORDER BY jour_num;
"""
df19 = pd.read_sql(query19, mydb)
fig19 = px.bar(df19, x='jour_semaine', y='nombre_transactions', 
               title='Q19: Transactions par jour de la semaine',
               labels={'jour_semaine': 'Jour de la semaine', 'nombre_transactions': 'Nombre de transactions'})
fig19.show()

# ============================================
# QUESTION 20 : Comparaison volumes de ventes par semaine
# ============================================
query20 = """
SELECT YEARWEEK(date_mutation) as semaine,
       COUNT(*) as nb_transactions,
       SUM(valeur_fonciere) as volume_total,
       AVG(valeur_fonciere) as moyenne_transaction
FROM MUTATION
WHERE valeur_fonciere IS NOT NULL
GROUP BY semaine
ORDER BY semaine;
"""
df20 = pd.read_sql(query20, mydb)

# Création d'un graphique avec deux axes Y
fig20 = make_subplots(specs=[[{"secondary_y": True}]])
fig20.add_trace(
    go.Scatter(x=df20['semaine'], y=df20['nb_transactions'], name="Nb transactions", mode='lines+markers'),
    secondary_y=False,
)
fig20.add_trace(
    go.Scatter(x=df20['semaine'], y=df20['volume_total'], name="Volume total", mode='lines+markers'),
    secondary_y=True,
)
fig20.update_layout(title='Q20: Évolution du volume de ventes par semaine')
fig20.update_xaxis_title("Semaine")
fig20.update_yaxis_title("Nombre de transactions", secondary_y=False)
fig20.update_yaxis_title("Volume total (€)", secondary_y=True)
fig20.show()

# Fermeture de la connexion
mydb.close()
print("\nToutes les visualisations ont été générées avec succès!")
print("Connexion à la base de données fermée.")