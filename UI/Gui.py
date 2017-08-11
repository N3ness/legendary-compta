import tkinter.ttk as ttk
from tkinter import *
from DA.Da import *


class Gui(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.Database = Da(Name='DB/legendaryCompta.db')

        self.Frame_Appli = Frame(self, borderwidth=2, relief=GROOVE)

        self.initFrameMenu()

        self.Frame_Appli.pack(side=LEFT, padx=20, pady=20, fill=NONE, expand=TRUE)
        self.seeAddInput()

    def initFrameMenu(self):
        Frame_Menu = Frame(self)
        Frame_Menu.pack(side=LEFT, padx=10, pady=10)
        Bouton_Ajout = Button(Frame_Menu, text='Nouvelle Entrée', command=self.seeAddInput)
        Bouton_Ajout.pack(pady=5, fill=X)
        Bouton_Journal = Button(Frame_Menu, text='Voir le Journal', command= self.seeJournal)
        Bouton_Journal.pack(pady=5, fill=X)
        Bouton_Comptes = Button(Frame_Menu, text='Voir les Comptes', command=self.seeAccounts)
        Bouton_Comptes.pack(pady=5, fill=X)
        Bouton_Resultat = Button(Frame_Menu, text='Voir le Resultat')
        Bouton_Resultat.pack(pady=5, fill=X)
        Bouton_Bilan = Button(Frame_Menu, text='Voir le Bilan')
        Bouton_Bilan.pack(pady=5, fill=X)


    def unload_Appli(self,FrameToUnload):
        list = FrameToUnload.pack_slaves()
        for widget in list:
            widget.destroy()

    def seeAddInput(self):
        self.unload_Appli(self.Frame_Appli)

        # Label nouvelle entrée
        label = Label(self.Frame_Appli, text="Nouvelle entrée")
        label.pack()

        # Date
        label = Label(self.Frame_Appli, text="Date (jj/mm/aaaa)")
        label.pack()
        iptDate = Entry(self.Frame_Appli)
        iptDate.pack(padx=10)

        # Compte
        label = Label(self.Frame_Appli, text="Compte")
        label.pack()

        listeComptes = Listbox(self.Frame_Appli,width=60)

        maliste = self.Database.getAllAccounts()
        for i in maliste:
            listeComptes.insert(i[0],i[1])
        listeComptes.pack(pady=5)

        # Libelle
        label = Label(self.Frame_Appli, text="Libellé")
        label.pack()
        iptLib = Entry(self.Frame_Appli, width=60)
        iptLib.pack(padx=30)

        # JournalFrame.py conteneur
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
        bouton = Button(self.Frame_Appli,
                        text="valider",width=50,
                        command=lambda: self.Database.formatAndSaveEcritures(iptDate.get(),
                                                                             maliste[listeComptes.curselection()[0]],
                                                                             iptLib.get(), iptSens.get(), iptMontant.get()))

        bouton.pack(pady=10)

    def seeJournal(self):

        self.unload_Appli(self.Frame_Appli)

        self.Frame_Appli.pack(fill=BOTH)

        frame_dt = Frame(self.Frame_Appli)
        frame_dt.pack(side=LEFT, padx=20, pady=20)

        tree_dt = ttk.Treeview(frame_dt)

        tree_dt.pack(padx=2, pady=2)

        tree_dt.heading("#0",text="Date")
        tree_dt.column("#0", width=110)

        for dt in self.Database.getAllMonths():
            id = tree_dt.insert("",0,iid= parser.parse(dt[0]).year,text=parser.parse(dt[0]).year,values=parser.parse(dt[0]).year)
            tree_dt.insert(id, "end", text='Janvier', values=1)
            tree_dt.insert(id, "end", text='Février', values=2)
            tree_dt.insert(id, "end", text='Mars', values=3)
            tree_dt.insert(id, "end", text='Avril', values=4)
            tree_dt.insert(id, "end", text='Mai', values=5)
            tree_dt.insert(id, "end", text='Juin', values=6)
            tree_dt.insert(id, "end", text='Juillet', values=7)
            tree_dt.insert(id, "end", text='Aout', values=8)
            tree_dt.insert(id, "end", text='Septembre', values=9)
            tree_dt.insert(id, "end", text='Octobre', values=10)
            tree_dt.insert(id, "end", text='Novembre', values=11)
            tree_dt.insert(id, "end", text='Décembre', values=12)

        label = Label(self.Frame_Appli,text='Journal')
        label.pack(expand=FALSE)

        scrollbar = Scrollbar(self.Frame_Appli)
        scrollbar.pack(side=RIGHT, fill=Y)

        cols = ("CLE","Date","Compte", "Libellé", "Débit","Crédit")
        dcols =("Date","Compte", "Libellé", "Débit","Crédit")
        tree=ttk.Treeview(self.Frame_Appli,columns=cols, displaycolumns=dcols,yscrollcommand=scrollbar.set)
        tree['show'] = 'headings'
        tree.column("Date",width=80)
        tree.column("Débit", width=80)
        tree.column("Crédit", width=80)

        for i in cols:
            tree.heading(i,text=i)

        scrollbar.config(command=tree.yview)
        tree.pack(fill=BOTH,expand=True)

        tree_dt.bind("<<TreeviewSelect>>", lambda _: self.journalLoad('', tree, parentz=str(tree_dt.parent(item=tree_dt.focus())),
                                                                      childrenz=str(tree_dt.item(tree_dt.focus())['values'][0])))


    def journalLoad(self, event, tree, childrenz, parentz):
        for i in tree.get_children():
            tree.delete(i)

        parentz=str(parentz)
        if len(str(childrenz))==1:
            childrenz = '0' + str(childrenz)
        else:
            childrenz = str(childrenz)

        for journalView in self.Database.getEcrituresByMonthAndYear(childrenz, parentz):
            self.insertJournalViewInTree(journalView,tree)


    def seeAccounts(self):
        self.unload_Appli(self.Frame_Appli)
        self.Frame_Appli.pack(fill=BOTH)

        frame_ct = Frame(self.Frame_Appli)
        frame_ct.pack(side=LEFT, padx=20, pady=20)

        tree_ct = ttk.Treeview(frame_ct)
        tree_ct.pack(padx=2, pady=2, expand=True, fill=BOTH)

        tree_ct.heading("#0", text="Comptes")
        tree_ct.column("#0", width=200)


        for i in self.Database.getAllAccounts():
            tree_ct.insert("",0,text=i[1],values=[i[1]])

        label = Label(self.Frame_Appli, text='Compte')
        label.pack(expand=FALSE)

        scrollbar = Scrollbar(self.Frame_Appli)
        scrollbar.pack(side=RIGHT, fill=Y)

        cols = ("CLE", "Date", "Libellé", "Débit", "Crédit")
        dcols = ("Date", "Libellé", "Débit", "Crédit")
        tree = ttk.Treeview(self.Frame_Appli, columns=cols, displaycolumns=dcols, yscrollcommand=scrollbar.set)
        tree['show'] = 'headings'
        tree.column("Date", width=80)
        tree.column("Débit", width=80)
        tree.column("Crédit", width=80)

        for i in cols:
            tree.heading(i, text=i)

        scrollbar.config(command=tree.yview)
        tree.pack(fill=BOTH, expand=True)

        tree_ct.bind("<<TreeviewSelect>>",
                     lambda _: self.accountsLoad(tree, SelectedMonth= tree_ct.item(tree_ct.focus())['values']))

    def accountsLoad(self, tree, SelectedMonth):
        for i in tree.get_children():
            tree.delete(i)

        for accountView in self.Database.getEcrituresByAccount(SelectedMonth):
            self.insertAccountViewInTree(accountView,tree)


    def insertJournalViewInTree(self, journalView, tree):
        if journalView.sens == ('Debit'):
            tree.insert("", 0, text="", values=(journalView.idEcriture, journalView.date, journalView.libelleCompte, journalView.libelleJournal, journalView.montant, 0))
        elif journalView.sens == ('Credit'):
            tree.insert("", 0, text="", values=(journalView.idEcriture, journalView.date, journalView.libelleCompte, journalView.libelleJournal, 0, journalView.montant))

    def insertAccountViewInTree(self, accountView, tree):
        if accountView.sens == ('Debit'):
            tree.insert("", 0, text="", values=(accountView.idEcriture, accountView.date, accountView.libelleJournal, accountView.montant, 0))
        elif accountView.sens == ('Credit'):
            tree.insert("", 0, text="", values=(accountView.idEcriture, accountView.date, accountView.libelleJournal, 0, accountView.montant))
