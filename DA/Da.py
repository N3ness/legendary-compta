import sqlite3

import dateutil.parser as parser

from Model.Compte import Compte
from Model.Journal import Journal
from Model.Operation import Operation


class Da:

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

    def AddToDB(self, iptDate, iptCompte, iptLibelle, iptSens, iptMontant):
        Sens=''
        if iptSens==1:
            Sens='Credit'
        elif iptSens==2:
# and iptCompte[2] == "Produits" )or(iptSens==1 and iptCompte[2] == "Charges"):
            Sens ='Debit'
        else:
            print('erreur valeur sens')

        if len(str(parser.parse(iptDate).month))== 1:
            mois="0"+str(parser.parse(iptDate).month)
        else:
            mois=str(parser.parse(iptDate).month)

        if len(str(parser.parse(iptDate).day))== 1:
            jour="0"+str(parser.parse(iptDate).day)
        else:
            jour=str(parser.parse(iptDate).day)

        #####BANQUE##### (Le compte "Banque" est la contrepartie de tous les mouvments de comptes.
        ################    Il y a donc une ligne banque ajoutée pour chaque ligne de compte du journal)

        if Sens == 'Debit':
            SensBanque = 'Credit'
        elif Sens == 'Credit':
            SensBanque = 'Debit'

        iptDate= str(parser.parse(iptDate).year) + '-' + mois + '-' + jour

        self.createOperation(str(iptDate), iptCompte[0], str(iptLibelle), Sens, iptMontant)


    def createOperation(self,date, idCompte, libelle, sens, montant):
        idJ1 = self.createJournal(idCompte,sens)
        compte = self.getCompteById(idCompte)
        idJSym = self.createSymJournal(compte.idCompteSymetric,sens)
        return self.__insert("""INSERT INTO Operation(idJournal1, idJournal2, libelle, date, montant) VALUES(?, ?, ?, ?, ?)""", (idJ1, compte.idCompteSymetric, libelle, date, montant))

    def createJournal(self,idCompte,sens):
        return self.__insert("""INSERT INTO Journal(idCompte, sens) VALUES(?, ?)""", (idCompte, sens))

    def createSymJournal(self,idCompteSym, sens):
        if sens == 'Debit':
            sens = 'Credit'
        elif sens == 'Credit':
            sens = 'Debit'
        return self.createJournal(idCompteSym, sens)

    def getCompteById(self,id):
        compte =  self.__select("""SELECT * FROM Comptes WHERE idCompte = ? """, (id,))
        return Compte(compte[0][0], compte[0][1], compte[0][2], compte[0][3])

    def getJournalById(self,id):
        journal =  self.__select("""SELECT * FROM Journal WHERE idJournal = ? """, (id,))
        return Journal(journal[0], journal[1], journal[2])

    #REQUETE INSERTION LIGNE
    def AddToBase(self,DBDate,DBCompte,DBLibelle,DBSens,DBMontant):

        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Journal(Date, Compte, Libelle, Sens, Montant) VALUES(?, ?, ?, ?, ?)""", (DBDate,DBCompte,DBLibelle,DBSens,DBMontant))
        conn.commit()
        conn.close()

    def AddAccount(self,AccName,AccType):

        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Comptes (Compte, Type) VALUES(?, ?)""", (AccName,AccType))
        conn.commit()
        conn.close()

    def SelectAccounts(self):

        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT idCompte,libelle, type FROM Comptes""")
        result = cursor.fetchall()
        conn.close()
        return result

    #REQUETE SELECT
    def SelectQuery(self,querychildrenz,queryparentz):

        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        if queryparentz =='':
            cursor.execute("""SELECT j.id, j.date,c.compte,j.libelle,j.sens,j.montant
                                        FROM Journal j JOIN Comptes c ON j.compte = c.id
                                        WHERE strftime('%Y',j.date) =?
                                        ORDER BY j.date
                                         """, ([str(querychildrenz)]))
        else:
            cursor.execute("""SELECT j.id, j.date,c.compte,j.libelle,j.sens,j.montant
                            FROM Journal j JOIN Comptes c ON j.compte = c.id
                            WHERE strftime('%m',j.date) =? AND strftime('%Y', j.date) = ?
                            ORDER BY j.date
                             """,(querychildrenz,queryparentz))
        result = cursor.fetchall()
        conn.close()
        return result

    def SelectAccountDetail(self,Account):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""SELECT j.id, j.date,c.compte,j.libelle,j.sens,j.montant
                        FROM Journal j JOIN Comptes c ON j.compte = c.id
                        WHERE c.compte = ?
                        ORDER BY j.date""",(Account))
        result = cursor.fetchall()
        conn.close()
        return result

    def MonthQuery(self):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""SELECT strftime('%Y',Date) FROM Journal GROUP BY strftime('%Y',Date) ORDER BY strftime('%Y',Date) """)
        result = cursor.fetchall()
        conn.close()
        return result

    def AddAccount(self, AccName, AccType):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""
        ALTER TABLE Journal
        ADD Commonid INTEGER""", (AccName, AccType))
        conn.commit()
        conn.close()

