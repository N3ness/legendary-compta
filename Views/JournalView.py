class JournalView:

    def __init__(self, idEcriture, libelleJournal, date, libelleCompte, montant, sens):
        self.idEcriture = idEcriture
        self.date = date
        self.libelleCompte = libelleCompte
        self.libelleJournal = libelleJournal
        self.montant = montant
        self.sens = sens

class TotalJournalView:

    def __init__(self, montant, sens):
        self.montant = montant
        self.sens = sens