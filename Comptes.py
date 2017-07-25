
class Compte:
    def __init__(self,Name, Type):
        self.Name = Name
        self.Type = Type


compte1 = Compte("electricité","charge")



print(compte1.Name, compte1.Type)