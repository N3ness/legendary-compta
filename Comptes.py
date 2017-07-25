
class Compte:
    def __init__(self,Id, Name, Type):
        self.Id = Id
        self.Name = Name
        self.Type = Type


compte1 = Compte("electricité","charge")



print(compte1.Name, compte1.Type)