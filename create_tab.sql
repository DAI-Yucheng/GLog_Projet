create database foncieres;
use foncieres;
-- drop database foncieres;

DROP TABLE IF EXISTS 

-- *******************************************
-- ÉTAPE 1 : CRÉATION DES TABLES INDÉPENDANTES
-- *******************************************

-- Table 1 : ADRESSE (Nouvelle table unique pour la localisation)
CREATE TABLE ADRESSE (
    ID_Adresse        INT PRIMARY KEY AUTO_INCREMENT, -- Clé primaire auto-incrémentée
    Code_postal       VARCHAR(5) NOT NULL,
    Commune           VARCHAR(100) NOT NULL,
    Code_departement  VARCHAR(3),
    Code_commune      VARCHAR(5),
    No_voie           VARCHAR(10),
    B_T_Q             VARCHAR(10),
    Type_de_voie      VARCHAR(50),
    Voie              VARCHAR(150),
    
    -- Clé UNIQUE pour garantir que chaque adresse complète n'est insérée qu'une seule fois
    UNIQUE KEY idx_unique_adresse (No_voie, B_T_Q, Type_de_voie, Voie, Code_postal) 
);

-- Table 2 : LOCAL (Détails de l'unité bâtie)
CREATE TABLE LOCAL (
    Identifiant_local         INT PRIMARY KEY AUTO_INCREMENT,
    Code_type_local           VARCHAR(5),
    Type_local                VARCHAR(50),
    Surface_reelle_bati       VARCHAR(5),
    Nombre_pieces_principales VARCHAR(5)
);

-- Table 3 : TERRAIN (Détails du terrain/parcelle)
CREATE TABLE TERRAIN (
    Identifiant_terrain     INT PRIMARY KEY AUTO_INCREMENT, -- PK et FK vers LOCAL
    ID_Adresse 				INT,
    Prefixe_de_section      VARCHAR(3),
    Section                 VARCHAR(5),
    No_plan                 VARCHAR(5),
    No_Volume               VARCHAR(5),
    Nature_culture          VARCHAR(50),
    Nature_culture_speciale VARCHAR(50),
    Surface_terrain         VARCHAR(10),
    
    FOREIGN KEY (Id_adresse) REFERENCES ADRESSE(ID_Adresse)
        ON UPDATE CASCADE ON DELETE RESTRICT
        
);


-- *******************************************
-- ÉTAPE 2 : CRÉATION DE LA TABLE CENTRALE ET DE LIAISON
-- *******************************************

-- Table 4 : MUTATION (Transaction immobilière)
CREATE TABLE MUTATION (
    No_disposition    INT PRIMARY KEY,
    Date_mutation     DATE,
    Nature_mutation   VARCHAR(50),
    Valeur_fonciere   DECIMAL(15, 2),
    Nombre_de_lots    INT,
    
    Id_adresse       INT,
    FOREIGN KEY (Id_adresse) REFERENCES ADRESSE(ID_Adresse)
        ON UPDATE CASCADE ON DELETE RESTRICT,
        
    Identifiant_local VARCHAR(50),
    FOREIGN KEY (Identifiant_local) REFERENCES LOCAL(Identifiant_local)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Table 5 : LOTS (Détail de chaque lot vendu dans une transaction)
CREATE TABLE LOTS (
    No_disposition     INT NOT NULL,          -- FK vers MUTATION
    No_Lot_Index       TINYINT NOT NULL,      -- 1, 2, 3...
    No_lot_original    VARCHAR(50),           -- L'identifiant textuel du lot
    Surface_Carrez     DECIMAL(10, 2),
    
    PRIMARY KEY (No_disposition, No_Lot_Index), 
    
    FOREIGN KEY (No_disposition) REFERENCES MUTATION(No_disposition)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Créer la table temporaire RawData (avec les noms de colonnes originaux du CSV)
CREATE TABLE RawData (
    No_disposition VARCHAR(50),
    Date_mutation VARCHAR(50),
    Nature_mutation VARCHAR(50),
    Valeur_fonciere VARCHAR(50),
    No_voie VARCHAR(50),
    B_T_Q VARCHAR(50),
    Type_de_voie VARCHAR(50),
    Code_voie VARCHAR(50),
    Voie VARCHAR(255),
    Code_postal VARCHAR(50),
    Commune VARCHAR(150),
    Code_departement VARCHAR(50),
    
    Code_commune VARCHAR(50),
    Prefixe_de_section VARCHAR(50),
    Section VARCHAR(50),
    No_plan VARCHAR(50),
    No_Volume VARCHAR(50),
    
    lot1 VARCHAR(50), 
    surface_carrez_lot1 VARCHAR(50),
    lot2 VARCHAR(50),
    surface_carrez_lot2 VARCHAR(50),
	lot3 VARCHAR(50), 
    surface_carrez_lot3 VARCHAR(50),
    lot4 VARCHAR(50),
    surface_carrez_lot4 VARCHAR(50),
    lot5 VARCHAR(50),
    surface_carrez_lot5 VARCHAR(50),
    
    Nombre_de_lots VARCHAR(50),
    Code_type_local VARCHAR(50),
    Type_local VARCHAR(50),
    Identifiant_local VARCHAR(50),
    Surface_reelle_bati VARCHAR(50),
    Nombre_pieces_principales VARCHAR(50),
    Nature_culture VARCHAR(50),
    Nature_culture_speciale VARCHAR(50),
    Surface_terrain VARCHAR(50)
);

-- 1. Peuplement de la table ADRESSE
-- Insertion IGNORE pour éviter les erreurs de doublon sur la clé unique composite.
INSERT IGNORE INTO ADRESSE (Code_postal, Commune, Code_departement, Code_commune, No_voie, B_T_Q, Type_de_voie, Voie)
SELECT 
    TRIM(Code_postal),
    TRIM(Commune),
    TRIM(Code_departement),
    TRIM(Code_commune),
    TRIM(No_voie),
    TRIM(B_T_Q),
    TRIM(Type_de_voie),
    TRIM(Voie)
FROM
    RawData
WHERE Code_postal IS NOT NULL AND TRIM(Code_postal) <> '';
select * from adresse;

-- 2. Peuplement de la table LOCAL
-- Insère les Identifiants locaux uniques
INSERT INTO LOCAL (Code_type_local, Type_local, Surface_reelle_bati, Nombre_pieces_principales)
SELECT DISTINCT
--    TRIM(Identifiant_local),
    TRIM(Code_type_local),
    TRIM(Type_local),
    TRIM(Surface_reelle_bati), 
    TRIM(Nombre_pieces_principales)
FROM
    RawData
ON DUPLICATE KEY UPDATE
    local.Identifiant_local = rawdata.Identifiant_local;
select * from local;

-- 3. Peuplement de la table TERRAIN
INSERT INTO TERRAIN (Prefixe_de_section, Section, No_plan, No_Volume, Nature_culture, Nature_culture_speciale, Surface_terrain,adresse)
SELECT DISTINCT
    TRIM(Prefixe_de_section),
	TRIM(Section),
    TRIM(No_plan),
    TRIM(No_Volume),
    TRIM(Nature_culture),
    TRIM(Nature_culture_speciale),
    TRIM(Surface_terrain)
FROM
    RawData;
select * from terrain;
-- 4. Peuplement de la table MUTATION
INSERT INTO MUTATION (No_disposition, Date_mutation, Nature_mutation, Valeur_fonciere, Nombre_de_lots, ID_Adresse, Identifiant_local)
SELECT DISTINCT
    TRIM(RD.No_disposition),
    STR_TO_DATE(TRIM(RD.Date_mutation), '%d/%m/%Y'), -- Conversion de la date
    NULLIF(TRIM(RD.Nature_mutation), ''),
    NULLIF(TRIM(RD.Valeur_fonciere), ''),
    NULLIF(TRIM(RD.Nombre_de_lots), ''),
    A.ID_Adresse, -- CLÉ RÉCUPÉRÉE PAR LA JOINTURE
    NULLIF(TRIM(RD.Identifiant_local), '')
FROM
    RawData AS RD
-- Jointure sur toutes les colonnes d'adresse pour récupérer l'ID_Adresse
JOIN 
    ADRESSE AS A ON 
        TRIM(RD.Code_postal) = A.Code_postal AND
        TRIM(RD.Voie) = A.Voie AND 
        NULLIF(TRIM(RD.No_voie), '') = A.No_voie AND
        NULLIF(TRIM(RD.B_T_Q), '') = A.B_T_Q
WHERE RD.No_disposition IS NOT NULL AND TRIM(RD.No_disposition) <> ''
ON DUPLICATE KEY UPDATE
    No_disposition = No_disposition;
    
-- 5. Peuplement de la table LOTS (Pivotage)
INSERT INTO LOTS (No_disposition, No_Lot_Index, No_lot_original, Surface_Carrez)

-- Lot 1
SELECT 
    TRIM(No_disposition) AS No_disposition, 
    1 AS No_Lot_Index, 
    NULLIF(TRIM(lot1), '') AS No_lot_original, 
    NULLIF(TRIM(surface_carrez_lot1), '') AS Surface_Carrez 
FROM RawData 
WHERE lot1 IS NOT NULL AND TRIM(lot1) <> '' 

UNION ALL

-- Lot 2
SELECT 
    TRIM(No_disposition), 
    2, 
    NULLIF(TRIM(lot2), ''), 
    NULLIF(TRIM(surface_carrez_lot2), '')
FROM RawData 
WHERE lot2 IS NOT NULL AND TRIM(lot2) <> ''

UNION ALL

-- Lot 3
SELECT 
    TRIM(No_disposition), 
    3, 
    NULLIF(TRIM(lot3), ''), 
    NULLIF(TRIM(surface_carrez_lot3), '')
FROM RawData 
WHERE lot3 IS NOT NULL AND TRIM(lot3) <> ''

UNION ALL

-- Lot 4
SELECT 
    TRIM(No_disposition), 
    4, 
    NULLIF(TRIM(lot4), ''), 
    NULLIF(TRIM(surface_carrez_lot4), '')
FROM RawData 
WHERE lot4 IS NOT NULL AND TRIM(lot4) <> ''

UNION ALL

-- Lot 5
SELECT 
    TRIM(No_disposition), 
    5, 
    NULLIF(TRIM(lot5), ''), 
    NULLIF(TRIM(surface_carrez_lot5), '')
FROM RawData 
WHERE lot5 IS NOT NULL AND TRIM(lot5) <> '';

SET GLOBAL local_infile = 1;  -- Permettre l'importation de données
SHOW GLOBAL VARIABLES LIKE 'secure_file_priv'; -- emplacement des données à importer

-- LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ValeursFoncieres-2025-S1.csv'
-- INTO TABLE RawData
-- FIELDS TERMINATED BY '|' -- Le séparateur de colonne (virgule, point-virgule, etc.)
-- LINES TERMINATED BY '\n' -- Le séparateur de ligne
-- IGNORE 1 LINES;
