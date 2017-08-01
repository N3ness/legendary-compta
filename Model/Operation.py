class Operation:

    def __init__(self, idOperation, journal1, journalBanque, libelle, date, montant ):
        self.idOperation = idOperation
        self.date = date
        self.montant = montant
        self.libelle = libelle
        self.journal1 = journal1.idJournal
        self.journlBanque = journalBanque.idJournal

