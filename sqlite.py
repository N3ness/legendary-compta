import sqlite3



#conn = sqlite3.connect('ma_base.db')
# #
# # CREATION TABLE
# conn = sqlite3.connect('ma_base.db')
# cursor = conn.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Comptes(
#      id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#      Compte TEXT,
#      Type TEXT
#      )""")
# conn.commit()
# conn.close()


#REQUETE INSERTION LIGNE
def AddToBase(DBDate,DBCompte,DBLibelle,DBSens,DBMontant):

    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Journal(Date, Compte, Libelle, Sens, Montant) VALUES(?, ?, ?, ?, ?)""", (DBDate,DBCompte,DBLibelle,DBSens,DBMontant))
    conn.commit()
    conn.close()




def AddAccount(AccName,AccType):

    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Comptes (Compte, Type) VALUES(?, ?)""", (AccName,AccType))
    conn.commit()
    conn.close()


def SelectAccounts():

    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT ID, Compte, Type FROM Comptes""")
    result = cursor.fetchall()
    conn.close()
    return result

#REQUETE SELECT
def SelectQuery():
    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Journal""")
    result = cursor.fetchall()

    conn.close()
    return result


def MonthQuery():
    conn = sqlite3.connect('ma_base.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT strftime('%Y',Date) FROM Journal GROUP BY strftime('%Y',Date) ORDER BY strftime('%Y',Date) """)
    result = cursor.fetchall()

    conn.close()
    return result

#REQUETE SUPRESSION
def Suppression():
    conn = sqlite3.connect('ma_base.db')
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

print(SelectAccounts()[1][1])