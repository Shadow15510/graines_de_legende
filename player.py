class Player:
    
    def __init__(self, name, species, stat, equipement, ):
        self.name = name
        self.species = species
        self.stat = stat[:]

    def export(self):
        return (self.name, self.species, self.stat)

