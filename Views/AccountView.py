class AccountView:

    def __init__(self, idEcriture, libelleJournal, date, montant, sens):
        self.idEcriture = idEcriture
        self.date = date
        self.libelleJournal = libelleJournal
        self.montant = montant
        self.sens = sens
