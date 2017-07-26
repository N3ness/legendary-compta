import dateutil.parser as parser
from DB import sqlite

class Da():


    def AddToDB(iptDate, iptCompte, iptLibelle, iptSens, iptMontant):
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

        iptDate= str(parser.parse(iptDate).year) + '-' + mois + '-' + jour
        sqlite.AddToBase(str(iptDate), iptCompte[0], str(iptLibelle), Sens, iptMontant)
