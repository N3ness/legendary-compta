CREATE TABLE `Ecriture` (
	`idEcriture`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`idJournal`	INTEGER NOT NULL,
	`idCompte`	INTEGER,
	`montant`	REAL,
	`sens`	TEXT,
	FOREIGN KEY(`idJournal`) REFERENCES `Journal`(`idJournal`),
	FOREIGN KEY(`idCompte`) REFERENCES `Comptes`(`idCompte`)
);
CREATE TABLE `Journal` (
	`idJournal`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    `libelle`	TEXT,
	`date`	NUMERIC
);
CREATE TABLE `Compte` (
	`idCompte`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`idCompteSymetrique`	INTEGER,
	`libelle`	TEXT,
	`type`	TEXT,
	FOREIGN KEY(`idCompteSymetrique`) REFERENCES `Comptes`(`idCompte`)
);
