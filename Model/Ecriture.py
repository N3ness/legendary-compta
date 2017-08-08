class Ecriture:

    def __init__(self, idEcriture, journal, compte, montant, sens):
        self.idEcriture = idEcriture
        self.journal = journal.idJournal
        self.compte = compte.idCompte
        self.montant = montant
        self.sens = sens
