import sqlite3

import dateutil.parser as parser

from Model.Compte import Compte
from Model.Journal import Journal
from Model.Ecriture import Ecriture
from Views.AccountView import AccountView
from Views.JournalView import JournalView


class Da:

    sens = ['Debit','Credit']

    def __init__(self,Name):
        self.databaseName = Name

    def __query(self, query):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def __insert(self, query, params):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute(query,params)
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return id

    def __select(self, query, params):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    def formatAndSaveEcritures(self, iptDate, iptCompte, iptLibelle, iptSens, iptMontant):

        if len(str(parser.parse(iptDate).month))== 1:
            mois="0"+str(parser.parse(iptDate).month)
        else:
            mois=str(parser.parse(iptDate).month)

        if len(str(parser.parse(iptDate).day))== 1:
            jour="0"+str(parser.parse(iptDate).day)
        else:
            jour=str(parser.parse(iptDate).day)

        iptDate= str(parser.parse(iptDate).year) + '-' + mois + '-' + jour

        self.newJournal(str(iptDate), iptCompte[0], str(iptLibelle), iptSens, iptMontant)

    def newJournal(self,date, idCompte, libelle, idxSens, montant):
        idNewJournal = self.createJournal(libelle,date)
        self.newEcritures(idNewJournal,idCompte,montant,idxSens)

    def newEcritures(self,idNewJournal,idCompte,montant,idxSens):
        self.createEcriture(idNewJournal, idCompte, montant, self.sens[idxSens])
        idSymCompte = self.getAccountById(idCompte).idCompteSymetric
        self.createEcriture(idNewJournal, idSymCompte, montant, self.sens[(idxSens + 1) % 2])

    def createEcriture(self,idJournal,idCompte,montant,sens):
        return self.__insert("""INSERT INTO Ecriture(idJournal, idCompte, montant, sens) VALUES(?, ?, ?, ?)""", (idJournal, idCompte, montant, sens))

    def createJournal(self,libelle,date):
        return self.__insert("""INSERT INTO Journal(libelle, date) VALUES(?, ?)""", (libelle, date))

    def getAccountById(self, idCompte):
        compte =  self.__select("""SELECT * FROM Compte WHERE idCompte = ? """, (idCompte,))
        return Compte(compte[0][0], compte[0][1], compte[0][2], compte[0][3])

    def getJournalById(self,id):
        journal =  self.__select("""SELECT * FROM Journal WHERE idJournal = ? """, (id,))
        return Journal(journal[0], journal[1], journal[2])

    def getAllMonths(self):
        months =  self.__select("""SELECT strftime('%Y',Date) FROM Journal GROUP BY strftime('%Y',Date) ORDER BY strftime('%Y',Date) """,())
        return months

    def getAllAccounts(self):
        accounts = self.__select("""SELECT idCompte, libelle, type FROM Compte""",())
        return accounts

    def getEcrituresByMonthAndYear(self, querychildrenz, queryparentz):
        queryStart = """SELECT e.idEcriture, j.libelle, j.date, c.libelle, e.montant, e.sens
                            FROM Ecriture e 
                            JOIN Compte c ON e.idCompte = c.idCompte
                            JOIN Journal j ON j.idJournal = e.idJournal """
        if queryparentz =='':
            journalViews = map(lambda x: JournalView(x[0], x[1], x[2], x[3], x[4], x[5]), self.__select(queryStart + """WHERE strftime('%Y', j.date) = ?
                            ORDER BY j.date,j.libelle,e.idJournal""", (querychildrenz,)))
        else:
            journalViews = map(lambda x: JournalView(x[0], x[1], x[2], x[3], x[4], x[5]), self.__select(queryStart + """WHERE strftime('%m',j.date) =? AND strftime('%Y', j.date) = ?
                            ORDER BY j.date,j.libelle,e.idJournal""", (querychildrenz,queryparentz)))
        return journalViews

    def getEcrituresByAccount(self, accountLibelle):
        accountViews = map(lambda x: AccountView(x[0],x[1],x[2],x[3],x[4]),self.__select("""SELECT e.idEcriture, j.libelle, j.date, e.montant, e.sens
                            FROM Ecriture e 
                            JOIN Compte c ON e.idCompte = c.idCompte
                            JOIN Journal j ON j.idJournal = e.idJournal
                            WHERE c.libelle = ? """, (accountLibelle)))
        return accountViews

