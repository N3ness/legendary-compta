import sqlite3



#conn = sqlite3.connect('ma_base.db')
# #
# # CREATION TABLE
# conn = sqlite3.connect('ma_base.db')
# cursor = conn.cursor()
# cursor.execute("""
# CREATE TABLE Journal(
#      id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#      Date DATE,
#      Compte INTEGER,
#      Libelle TEXT,
#      Sens TEXT,
#      Montant REAL,
#      FOREIGN KEY(Compte) REFERENCES Comptes(id)
#      )""")
# conn.commit()
# conn.close()


#REQUETE INSERTION LIGNE
def AddToBase(DBDate,DBCompte,DBLibelle,DBSens,DBMontant):

    conn = sqlite3.connect('DB\ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Journal(Date, Compte, Libelle, Sens, Montant) VALUES(?, ?, ?, ?, ?)""", (DBDate,DBCompte,DBLibelle,DBSens,DBMontant))
    conn.commit()
    conn.close()




def AddAccount(AccName,AccType):

    conn = sqlite3.connect('DB\ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Comptes (Compte, Type) VALUES(?, ?)""", (AccName,AccType))
    conn.commit()
    conn.close()


def SelectAccounts():

    conn = sqlite3.connect('DB\ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, Compte, Type FROM Comptes""")
    result = cursor.fetchall()
    conn.close()
    return result

#REQUETE SELECT
def SelectQuery(querymonth,queryyear):
    conn = sqlite3.connect('DB\ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT j.id, j.date,c.compte,j.libelle,j.sens,j.montant
                    FROM Journal j JOIN Comptes c ON j.compte = c.id
                    WHERE strftime('%m',j.date)=? AND strftime('%Y', j.date) = ?
                     """,(querymonth,queryyear))
    result = cursor.fetchall()
    conn.close()
    return result


def MonthQuery():
    conn = sqlite3.connect('DB\ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT strftime('%Y',date) FROM Operation GROUP BY strftime('%Y',date) ORDER BY strftime('%Y',date) """)
    result = cursor.fetchall()
    conn.close()
    return result

#REQUETE SUPRESSION
def Suppression():
    conn = sqlite3.connect('DB\ma_base.db')
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

# print(SelectAccounts()[1][1])