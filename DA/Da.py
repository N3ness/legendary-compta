import dateutil.parser as parser
import sqlite3

class Da:

    def __init__(self,Name):
        self.databaseName = Name

    def AddToDB(self, iptDate, iptCompte, iptLibelle, iptSens, iptMontant):
        Sens=''
        if( iptSens==1 and iptCompte[2] == "Produits" )or(iptSens==2 and iptCompte[2] == "Charges"):
            Sens='Credit'
        elif ( iptSens==2 and iptCompte[2] == "Produits" )or(iptSens==1 and iptCompte[2] == "Charges"):
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


        print(iptCompte[0])
        iptDate= str(parser.parse(iptDate).year) + '-' + mois + '-' + jour
        self.AddToBase(str(iptDate), iptCompte[0], str(iptLibelle), Sens, iptMontant)
        self.AddToBase(str(iptDate), 4, str(iptLibelle), SensBanque, iptMontant)


    def createJournalTable(self):
        conn = sqlite3.connect(self.databaseName)
        #
        # CREATION TABLE
        conn = sqlite3.connect('ma_base.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE Journal(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             Date DATE,
             Compte INTEGER,
             Libelle TEXT,
             Sens TEXT,
             Montant REAL,
             FOREIGN KEY(Compte) REFERENCES Comptes(id)
             )""")
        conn.commit()
        conn.close()


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
        SELECT id, Compte, Type FROM Comptes""")
        result = cursor.fetchall()
        conn.close()
        return result

    #REQUETE SELECT
    def SelectQuery(self,querymonth,queryyear):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""SELECT j.id, j.date,c.compte,j.libelle,j.sens,j.montant
                        FROM Journal j JOIN Comptes c ON j.compte = c.id
                        WHERE strftime('%m',j.date) =? AND strftime('%Y', j.date) = ?
                         """,(querymonth,queryyear))
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

    #REQUETE SUPRESSION
    def Suppression(self):
        conn = sqlite3.connect(self.databaseName)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM Journal""")
        conn.commit()
        conn.close()

    #REQUETE SUPRESSION
    # conn = sqlite3.connect('ma_base.db')
    # cursor = conn.cursor()
    # cursor.execute("""DROP TABLE Journal""")
    # conn.commit()
    # conn.close()

