DROP DATABASE IF EXISTS foncieres;
CREATE DATABASE foncieres;
USE foncieres;

-- ============================================
-- ÉTAPE 1 : CRÉATION TABLE D'IMPORT (BRUTE)
-- ============================================

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
-- ÉTAPE 2 : IMPORT DU FICHIER
-- ============================================

SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ValeursFoncieres-2025-S1_part.txt'
INTO TABLE DVF_IMPORT
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- Conversion de la date de str en DATE
ALTER TABLE DVF_IMPORT ADD COLUMN date_mutation_clean DATE;
SET SQL_SAFE_UPDATES = 0;

UPDATE DVF_IMPORT 
SET date_mutation_clean = STR_TO_DATE(date_mutation, '%d/%m/%Y');

ALTER TABLE DVF_IMPORT DROP COLUMN date_mutation;

ALTER TABLE DVF_IMPORT 
CHANGE COLUMN date_mutation_clean date_mutation DATE;
SET SQL_SAFE_UPDATES = 1;
-- ============================================
-- ÉTAPE 3 : CRÉATION DES TABLES NORMALISÉES
-- ============================================

CREATE TABLE DEPARTEMENT (
    code_departement VARCHAR(3) PRIMARY KEY
);

CREATE TABLE COMMUNE (
    id_commune INT PRIMARY KEY AUTO_INCREMENT,
    code_departement VARCHAR(3),
    commune VARCHAR(100),
    code_postal VARCHAR(10),
    UNIQUE (code_departement, commune, code_postal)
);

CREATE TABLE NATURE_MUTATION (
    id_nature_mutation INT PRIMARY KEY AUTO_INCREMENT,
    nature_mutation VARCHAR(50)
);

CREATE TABLE TYPE_LOCAL (
    id_type_local INT PRIMARY KEY AUTO_INCREMENT,
    type_local VARCHAR(50)
);

CREATE TABLE NATURE_CULTURE (
    code_nature_culture VARCHAR(5) PRIMARY KEY
);


CREATE TABLE MUTATION (
    id_mutation INT PRIMARY KEY AUTO_INCREMENT,
    no_disposition VARCHAR(10),
    date_mutation DATE,
    id_nature_mutation INT,
    valeur_fonciere DECIMAL(15,2)
);

CREATE TABLE BIEN (
    id_bien INT PRIMARY KEY AUTO_INCREMENT,
    id_commune INT,
    id_type_local INT,
    surface_reelle_bati DECIMAL(10,2),
    nombre_pieces_principales INT,
    nature_culture VARCHAR(5),
    surface_terrain DECIMAL(10,2),
    -- On garde l'id_local temporairement pour faire la liaison avec Mutation
    _tmp_row_id int
);

drop table if exists mutation_bien;
CREATE TABLE MUTATION_BIEN (
    id_mutation INT,
    id_bien INT,
    PRIMARY KEY (id_mutation, id_bien)
);

-- ============================================
-- ÉTAPE 4 : RÉPARTITION DES DONNÉES
-- ============================================

INSERT INTO DEPARTEMENT (code_departement)
SELECT DISTINCT code_departement FROM DVF_IMPORT WHERE code_departement IS NOT NULL;

INSERT INTO COMMUNE (code_departement, commune, code_postal)
SELECT DISTINCT code_departement, commune, code_postal FROM DVF_IMPORT WHERE commune IS NOT NULL;

INSERT INTO NATURE_MUTATION (nature_mutation)
SELECT DISTINCT nature_mutation FROM DVF_IMPORT WHERE nature_mutation IS NOT NULL;

INSERT INTO TYPE_LOCAL (type_local)
SELECT DISTINCT type_local FROM DVF_IMPORT WHERE type_local IS NOT NULL;

INSERT INTO NATURE_CULTURE (code_nature_culture)
SELECT DISTINCT nature_culture FROM DVF_IMPORT WHERE nature_culture IS NOT NULL;

INSERT INTO MUTATION (no_disposition, date_mutation, id_nature_mutation, valeur_fonciere)
SELECT DISTINCT 
    i.no_disposition, 
    i.date_mutation,
    nm.id_nature_mutation,
    -- On nettoie la chaîne : on enlève les espaces et on remplace la virgule
    -- Si le résultat est vide ou non numérique, on met NULL
    CASE 
        WHEN TRIM(REPLACE(i.valeur_fonciere, ',', '.')) REGEXP '^[0-9]+(\.[0-9]+)?$' 
        THEN CAST(TRIM(REPLACE(i.valeur_fonciere, ',', '.')) AS DECIMAL(15,2))
        ELSE NULL 
    END
FROM DVF_IMPORT i
JOIN NATURE_MUTATION nm ON i.nature_mutation = nm.nature_mutation
WHERE i.valeur_fonciere IS NOT NULL AND i.valeur_fonciere != '';

-- Bien : chaque ligne de l'import est un bien (bati ou terrain)

-- ÉTAPE 1 : Ajouter une colonne d'index temporaire à DVF_IMPORT
ALTER TABLE DVF_IMPORT ADD COLUMN _tmp_row_id INT AUTO_INCREMENT PRIMARY KEY FIRST;

-- ÉTAPE 3 : Insertion des BIEN avec l'index de ligne
INSERT INTO BIEN (id_commune, id_type_local, surface_reelle_bati, nombre_pieces_principales, nature_culture, surface_terrain, _tmp_row_id)
SELECT 
    c.id_commune,
    tl.id_type_local,
    CAST(REPLACE(NULLIF(i.surface_reelle_bati, ''), ',', '.') AS DECIMAL(10,2)),
    CAST(NULLIF(i.nombre_pieces_principales, '') AS UNSIGNED),
    i.nature_culture,
    CAST(REPLACE(NULLIF(i.surface_terrain, ''), ',', '.') AS DECIMAL(10,2)),
    i._tmp_row_id  -- On capture l'index de la ligne d'import
FROM DVF_IMPORT i
LEFT JOIN COMMUNE c ON i.commune = c.commune AND i.code_postal = c.code_postal AND i.code_departement = c.code_departement
LEFT JOIN TYPE_LOCAL tl ON i.type_local = tl.type_local;

-- ÉTAPE 4 : Mutation_Bien avec liaison par _tmp_row_id

INSERT INTO MUTATION_BIEN (id_mutation, id_bien)
SELECT DISTINCT m.id_mutation, b.id_bien
FROM DVF_IMPORT i
JOIN MUTATION m ON i.no_disposition = m.no_disposition 
    AND i.date_mutation = m.date_mutation
JOIN BIEN b ON b._tmp_row_id = i._tmp_row_id;

-- ============================================
-- ÉTAPE 5 : CONTRAINTES (FK)
-- ============================================

ALTER TABLE COMMUNE ADD CONSTRAINT fk_commune_dept FOREIGN KEY (code_departement) REFERENCES DEPARTEMENT(code_departement);
ALTER TABLE BIEN ADD CONSTRAINT fk_bien_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune);
ALTER TABLE BIEN ADD CONSTRAINT fk_bien_type FOREIGN KEY (id_type_local) REFERENCES TYPE_LOCAL(id_type_local);
ALTER TABLE BIEN ADD CONSTRAINT fk_bien_culture FOREIGN KEY (nature_culture) REFERENCES NATURE_CULTURE(code_nature_culture);
ALTER TABLE MUTATION ADD CONSTRAINT fk_mutation_nature FOREIGN KEY (id_nature_mutation) REFERENCES NATURE_MUTATION(id_nature_mutation);
ALTER TABLE MUTATION_BIEN ADD CONSTRAINT fk_mb_mutation FOREIGN KEY (id_mutation) REFERENCES MUTATION(id_mutation);
ALTER TABLE MUTATION_BIEN ADD CONSTRAINT fk_mb_bien FOREIGN KEY (id_bien) REFERENCES BIEN(id_bien);