from tkinter import *
import sqlite
import tkinter.ttk as ttk
import dateutil.parser as parser



def capartenbase(iptDate, iptCompte, iptLibelle, iptSens, iptMontant):
    Sens=''
    if iptSens==1:
        Sens='Entree'
    elif iptSens == 2:
        Sens ='Sortie'
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
    sqlite.AddToBase(str(iptDate), str(iptCompte), str(iptLibelle), Sens, iptMontant)

class appli(Tk):
    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.Frame_Appli = Frame(self.parent, borderwidth=2, relief=GROOVE)



        Frame_Menu = Frame(self.parent)
        Frame_Menu.pack(side=LEFT, padx=10,pady=10)

        Bouton_Ajout = Button(Frame_Menu,text = 'Nouvelle Entrée',command=self.Add_Input)
        Bouton_Ajout.pack(pady=5,fill=X)

        Bouton_Journal = Button(Frame_Menu, text='Voir le Journal',command=self.voir_journal)
        Bouton_Journal.pack(pady=5,fill=X)

        Bouton_Comptes = Button(Frame_Menu,text='Voir les Comptes')
        Bouton_Comptes.pack(pady=5,fill=X)

        Bouton_Resultat = Button(Frame_Menu, text='Voir le Resultat')
        Bouton_Resultat.pack(pady=5,fill=X)

        Bouton_Bilan = Button(Frame_Menu,text='Voir le Bilan')
        Bouton_Bilan.pack(pady=5,fill=X)

        self.Frame_Appli.pack(side=LEFT, padx=20, pady=20, fill=NONE, expand=TRUE)
        self.Add_Input()

    def unload_Appli(self):

        list = self.Frame_Appli.pack_slaves()
        for widget in list:
            widget.destroy()

    def Add_Input(self):
        self.unload_Appli()

        # Label nouvelle entrée
        label = Label(self.Frame_Appli, text="Nouvelle entrée")
        label.pack()

        # Frame conteneur
        # Frame1 = Frame(self.Frame_Appli, borderwidth=2, relief=GROOVE)
        # Frame1.pack(side=TOP, padx=30, pady=20)

        # Date
        label = Label(self.Frame_Appli, text="Date (jj/mm/aaaa)")
        label.pack()
        iptDate = Entry(self.Frame_Appli)
        iptDate.pack(padx=10)

        # Compte
        label = Label(self.Frame_Appli, text="Compte")
        label.pack()
        listeComptes = Listbox(self.Frame_Appli,width=60)
        listeComptes.insert(1, "Consultation Seul")
        listeComptes.insert(2, "Consultation Couple")
        listeComptes.insert(3, "Commission sur consultation")
        listeComptes.insert(4, "Assurance")
        listeComptes.insert(5, "Frais bancaires")
        listeComptes.insert(5, "Fournitures")
        listeComptes.insert(5, "Autre charge")
        listeComptes.pack(pady=5)

        # Libelle
        label = Label(self.Frame_Appli, text="Libellé")
        label.pack()
        iptLib = Entry(self.Frame_Appli, width=60)
        iptLib.pack(padx=30)

        # Frame conteneur
        Frame2 = Frame(self.Frame_Appli, borderwidth=2, relief=GROOVE)
        Frame2.pack(side=TOP, pady=10)

        # entree / sortie
        value = StringVar()
        iptSens = IntVar()
        iptEntree = Radiobutton(Frame2, text="Entrée", variable=iptSens, value=1)
        iptSortie = Radiobutton(Frame2, text="Sortie", variable=iptSens, value=2)
        iptEntree.pack(pady=5)
        iptSortie.pack(pady=5)

        # Montant
        label = Label(self.Frame_Appli, text="Montant")
        label.pack()
        iptMontant = Entry(self.Frame_Appli, width=60)
        iptMontant.pack()

        # bouton valider
        bouton = Button(self.Frame_Appli, text="valider",width=50, command=lambda: capartenbase(iptDate.get(),listeComptes.get(listeComptes.curselection()),iptLib.get(),iptSens.get(),iptMontant.get()))
        bouton.pack(pady=10)

    def voir_journal(self):

        self.unload_Appli()

        self.Frame_Appli.pack(fill=BOTH)

        frame_dt = Frame(self.Frame_Appli)
        frame_dt.pack(side=LEFT, padx=20, pady=20)

        tree_dt = ttk.Treeview(frame_dt)
        tree_dt.pack(padx=2, pady=2)
        tree_dt.heading("#0",text="Date")
        tree_dt.column("#0", width=110)


        for dt in sqlite.MonthQuery():
            id = tree_dt.insert("",0,text=parser.parse(dt[0]).year)
            tree_dt.insert(id, "end", text='Janvier')
            tree_dt.insert(id, "end", text='Février')
            tree_dt.insert(id, "end", text='Mars')
            tree_dt.insert(id, "end", text='Avril')
            tree_dt.insert(id, "end", text='Mai')
            tree_dt.insert(id, "end", text='Juin')
            tree_dt.insert(id, "end", text='Juillet')
            tree_dt.insert(id, "end", text='Aout')
            tree_dt.insert(id, "end", text='Septembre')
            tree_dt.insert(id, "end", text='Octobre')
            tree_dt.insert(id, "end", text='Novembre')
            tree_dt.insert(id, "end", text='Décembre')




        label = Label(self.Frame_Appli,text='Journal')
        label.pack(expand=FALSE)

        scrollbar = Scrollbar(self.Frame_Appli)
        scrollbar.pack(side=RIGHT, fill=Y)

        cols=("CLE","Date","Compte", "Libellé", "Sens","Montant")
        dcols=("Date","Compte", "Libellé", "Sens","Montant")
        tree=ttk.Treeview(self.Frame_Appli,columns=cols, displaycolumns=dcols,yscrollcommand=scrollbar.set)
        tree['show'] = 'headings'
        tree.column("Date",width=80)
        tree.column("Sens", width=80)
        tree.column("Montant", width=80)




        for i in cols:
            tree.heading(i,text=i)

        for item in sqlite.SelectQuery():
            tree.insert("",0,text="",values=item)

        scrollbar.config(command=tree.yview)
        tree.pack(fill=BOTH,expand=True)


        # # liste.pack(expand=TRUE,fill=Y)



# x = str.index(i[0],len(i) + (" "*(10)



if __name__ == "__main__":
    app = appli(None)
    app.title('merfzz')
    app.mainloop()



#
#
# print(Nice_Line(("zizi","fefesse","chatte")))
# print(Nice_Line(("couille","cul","bite")))