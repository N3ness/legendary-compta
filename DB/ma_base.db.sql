BEGIN TRANSACTION;
CREATE TABLE `Operation` (
	`idOperation`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`idJournal1`	INTEGER NOT NULL,
	`idJournal2`	INTEGER NOT NULL,
	`libelle`	TEXT,
	`date`	NUMERIC,
	`montant`	REAL,
	FOREIGN KEY(`idJournal1`) REFERENCES `Journal`(`idJournal`),
	FOREIGN KEY(`idJournal2`) REFERENCES `Journal`(`idJournal`)
);
INSERT INTO `Operation` VALUES (2,22,1,'1','2017-01-01',100.0);
INSERT INTO `Operation` VALUES (3,24,1,'','2010-01-01',50.0);
INSERT INTO `Operation` VALUES (4,26,1,'Test','2011-01-02',80.0);
CREATE TABLE `Journal` (
	`idJournal`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`idCompte`	INTEGER,
	`sens`	TEXT,
	FOREIGN KEY(`idCompte`) REFERENCES `Comptes`(`idCompte`)
);
INSERT INTO `Journal` VALUES (22,2,'Credit');
INSERT INTO `Journal` VALUES (23,1,'Debit');
INSERT INTO `Journal` VALUES (24,3,'Credit');
INSERT INTO `Journal` VALUES (25,1,'Debit');
INSERT INTO `Journal` VALUES (26,3,'Debit');
INSERT INTO `Journal` VALUES (27,1,'Credit');
CREATE TABLE `Comptes` (
	`idCompte`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`idCompteSymetrique`	INTEGER,
	`libelle`	TEXT,
	`type`	TEXT,
	FOREIGN KEY(`idCompteSymetrique`) REFERENCES `Comptes`(`idCompte`)
);
INSERT INTO `Comptes` VALUES (1,NULL,'Banque','Actif');
INSERT INTO `Comptes` VALUES (2,1,'Consultation','Produit');
INSERT INTO `Comptes` VALUES (3,1,'Electricité','Charge');
COMMIT;
