drop database foncieres;
create database foncieres;
use foncieres;

-- ============================================
-- ÉTAPE 1 : CRÉATION TABLE D'IMPORT
-- ============================================

DROP TABLE IF EXISTS DVF_IMPORT;

CREATE TABLE DVF_IMPORT (
    identifiant_document VARCHAR(50),
    reference_document VARCHAR(50),
    article_cgi_1 VARCHAR(50),
    article_cgi_2 VARCHAR(50),
    article_cgi_3 VARCHAR(50),
    article_cgi_4 VARCHAR(50),
    article_cgi_5 VARCHAR(50),
    no_disposition VARCHAR(10),
    date_mutation VARCHAR(10),
    nature_mutation VARCHAR(50),
    valeur_fonciere VARCHAR(20),
    no_voie VARCHAR(10),
    btq VARCHAR(5),
    type_de_voie VARCHAR(10),
    code_voie VARCHAR(10),
    voie VARCHAR(100),
    code_postal VARCHAR(10),
    commune VARCHAR(100),
    code_departement VARCHAR(3),
    code_commune VARCHAR(10),
    prefixe_section VARCHAR(10),
    section VARCHAR(10),
    no_plan VARCHAR(10),
    no_volume VARCHAR(10),
    lot_1 VARCHAR(10),
    surface_carrez_1 VARCHAR(20),
    lot_2 VARCHAR(10),
    surface_carrez_2 VARCHAR(20),
    lot_3 VARCHAR(10),
    surface_carrez_3 VARCHAR(20),
    lot_4 VARCHAR(10),
    surface_carrez_4 VARCHAR(20),
    lot_5 VARCHAR(10),
    surface_carrez_5 VARCHAR(20),
    nombre_lots VARCHAR(10),
    code_type_local VARCHAR(10),
    type_local VARCHAR(50),
    identifiant_local VARCHAR(50),
    surface_reelle_bati VARCHAR(20),
    nombre_pieces_principales VARCHAR(10),
    nature_culture VARCHAR(5),
    nature_culture_speciale VARCHAR(50),
    surface_terrain VARCHAR(20)
);

-- ============================================
-- ÉTAPE 2 : IMPORT DU FICHIER TXT
-- ============================================

SET GLOBAL local_infile = 1;  -- Permettre l'importation de données
SHOW GLOBAL VARIABLES LIKE 'secure_file_priv'; -- emplacement des données à importer

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/data_dvf.txt'
INTO TABLE DVF_IMPORT
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- ============================================
-- ÉTAPE 3 : CRÉATION DES TABLES NORMALISÉES
-- ============================================

DROP TABLE IF EXISTS DEPARTEMENT;
CREATE TABLE DEPARTEMENT (
    code_departement VARCHAR(3) PRIMARY KEY
);

DROP TABLE IF EXISTS COMMUNE;
CREATE TABLE COMMUNE (
    id_commune INT PRIMARY KEY AUTO_INCREMENT,
    code_departement VARCHAR(3),
    commune VARCHAR(100),
    code_postal VARCHAR(10)
);

DROP TABLE IF EXISTS NATURE_MUTATION;
CREATE TABLE NATURE_MUTATION (
    id_nature_mutation INT PRIMARY KEY AUTO_INCREMENT,
    nature_mutation VARCHAR(50)
);

DROP TABLE IF EXISTS TYPE_LOCAL;
CREATE TABLE TYPE_LOCAL (
    id_type_local INT PRIMARY KEY AUTO_INCREMENT,
    type_local VARCHAR(50)
);

DROP TABLE IF EXISTS NATURE_CULTURE;
CREATE TABLE NATURE_CULTURE (
    code_nature_culture VARCHAR(5) PRIMARY KEY
);

DROP TABLE IF EXISTS MUTATION;
CREATE TABLE MUTATION (
    id_mutation INT PRIMARY KEY AUTO_INCREMENT,
    no_disposition VARCHAR(10),
    date_mutation DATE,
    nature_mutation VARCHAR(50),
    valeur_fonciere DECIMAL(12,2)
);

DROP TABLE IF EXISTS BIEN;
CREATE TABLE BIEN (
    id_bien INT PRIMARY KEY AUTO_INCREMENT,
    no_disposition VARCHAR(10),
    date_mutation DATE,
    valeur_fonciere DECIMAL(12,2),
    commune VARCHAR(100),
    code_departement VARCHAR(3),
    code_postal VARCHAR(10),
    type_local VARCHAR(50),
    surface_reelle_bati VARCHAR(10),
    nombre_pieces_principales VARCHAR(10),
    nature_culture VARCHAR(5),
    surface_terrain VARCHAR(10)
);

-- ============================================
-- ÉTAPE 4 : RÉPARTITION DES DONNÉES
-- ============================================

-- Remplir DEPARTEMENT
INSERT INTO DEPARTEMENT (code_departement)
SELECT DISTINCT code_departement
FROM DVF_IMPORT
WHERE code_departement IS NOT NULL;

-- Remplir COMMUNE
INSERT INTO COMMUNE (code_departement, commune, code_postal)
SELECT DISTINCT code_departement, commune, code_postal
FROM DVF_IMPORT
WHERE commune IS NOT NULL;

-- Remplir NATURE_MUTATION
INSERT INTO NATURE_MUTATION (nature_mutation)
SELECT DISTINCT nature_mutation
FROM DVF_IMPORT
WHERE nature_mutation IS NOT NULL;

-- Remplir TYPE_LOCAL
INSERT INTO TYPE_LOCAL (type_local)
SELECT DISTINCT type_local
FROM DVF_IMPORT
WHERE type_local IS NOT NULL;

-- Remplir NATURE_CULTURE
INSERT INTO NATURE_CULTURE (code_nature_culture)
SELECT DISTINCT nature_culture
FROM DVF_IMPORT
WHERE nature_culture IS NOT NULL;

-- Remplir MUTATION
INSERT INTO MUTATION (no_disposition, date_mutation, nature_mutation, valeur_fonciere)
SELECT DISTINCT 
    no_disposition,
    STR_TO_DATE(date_mutation, '%d/%m/%Y'),
    nature_mutation,
    CAST(REPLACE(valeur_fonciere, ',', '.') AS DECIMAL(12,2))
FROM DVF_IMPORT;

-- Remplir BIEN
INSERT INTO BIEN (no_disposition, date_mutation, valeur_fonciere, commune, code_departement, 
                  code_postal, type_local, surface_reelle_bati, nombre_pieces_principales, 
                  nature_culture, surface_terrain)
SELECT 
    no_disposition,
    STR_TO_DATE(date_mutation, '%d/%m/%Y'),
    CAST(REPLACE(valeur_fonciere, ',', '.') AS DECIMAL(12,2)),
    commune,
    code_departement,
    code_postal,
    type_local,
    surface_reelle_bati,
    nombre_pieces_principales,
    nature_culture,
    surface_terrain
FROM DVF_IMPORT;

-- ============================================
-- VÉRIFICATION
-- ============================================

SELECT 'DVF_IMPORT' as Table_name, COUNT(*) as Nb_lignes FROM DVF_IMPORT
UNION ALL
SELECT 'DEPARTEMENT', COUNT(*) FROM DEPARTEMENT
UNION ALL
SELECT 'COMMUNE', COUNT(*) FROM COMMUNE
UNION ALL
SELECT 'NATURE_MUTATION', COUNT(*) FROM NATURE_MUTATION
UNION ALL
SELECT 'TYPE_LOCAL', COUNT(*) FROM TYPE_LOCAL
UNION ALL
SELECT 'NATURE_CULTURE', COUNT(*) FROM NATURE_CULTURE
UNION ALL
SELECT 'MUTATION', COUNT(*) FROM MUTATION
UNION ALL
SELECT 'BIEN', COUNT(*) FROM BIEN;