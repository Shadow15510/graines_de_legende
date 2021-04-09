class Player:
    def __init__(self, identificator, name, species, stat, image, history="", injuries=[], weapons=[["mains nues", "Arme naturelle", "un poing serré peut faire des dégâts.", -3]], armors=[], shells=[], stuff=[], languages=[], capacities=[], archetype=[], notes=[]):
        self.id = identificator
        self.name = name
        self.species = species
        self.history = history
        # stat : [Agilité - 0, Constitution - 1, Force - 2, Précision - 3,  Sens - 4, Social - 5, Survie - 6, Volonté - 7, (XP dépensés, XP économisé) - 8, PV - 9, monnaie de (or, cuivre) - 10, couleur - 11]
        self.stat = stat[:]
        self.image = image

        if languages: self.languages = languages[:]
        else: self.languages = ["Commun"]

        if archetype: self.archetype = archetype[:]
        else: self.archetype = [
            [species, 0], # éthnie
            ["", 0], # commun
            ["", 0], # héroïque I
            ["", 0], # héroïque II
            ["", 0], # héroïque III
            ["", 0]] # légendaire

        if capacities: self.capacities = capacities[:]
        else: self.capacities = [[["attaque de base", 1], ["lever de bouclier", 1]], [], [], [], [], [], []]

        self.armors = [Armor(*i) for i in armors]
        self.shells = [Shell(*i) for i in shells]
        self.injuries = [Injury(i) for i in injuries]
        self.weapons = [Weapon(*i) for i in weapons]
        self.stuff = [Stuff(*i) for i in stuff]
        self.notes = notes[:]

    def export(self): return [self.id, self.name, self.species, self.stat, self.image, self.history, [i.export() for i in self.injuries], [i.export() for i in self.weapons], [i.export() for i in self.armors], [i.export() for i in self.shells], [i.export() for i in self.stuff], self.languages, self.capacities, self.archetype, self.notes]

    def isalive(self): return self.stat[9] > 0

    def natural_healing(self): return (2, 4, 5, 8, 15)[self.stat[1]]

    def max_pv(self): return (10, 16, 20, 24, 30)[self.stat[1]]

    def get_minimum(self, name): return 6 - self.stat[("agilité", "constitution", "force", "précision", "sens", "social", "survie", "volonté").index(name.lower())] # score au dé minimum à obtenir pour valider le lancer

    def add_note(self, note_value):
        self.notes.append([len(self.notes) + 1, note_value])

    def del_note(self, index_target):
        if 0 < index_target <= len(self.notes):
            content = self.notes[index_target - 1][1]
            del(self.notes[index_target - 1])
            for index, value in enumerate(self.notes):
                if index >= index_target - 1: self.notes[index] = [index + 1, value[1]]
            return content
        else:
            return None

    def have_item(self, name):
        for cat_index, category in enumerate((self.weapons, self.armors, self.shells, self.stuff)):
            for index, item in enumerate(category):
                if item.name == name: return (cat_index, category), index

        return None, -1

    def del_item(self, name, category_target=-1):
        category, index = self.have_item(name)
        if index != -1 and (category_target == -1 or (category_target != -1 and category_target == category[0])):
            del(category[1][index])
            return True

        else: return False

    # item = [args dans l'ordre de l'objet]
    def add_item(self, item, category):
        if not self.have_item(item[0])[0]:
            if category == 0:
                self.weapons.append(Weapon(*item))
            elif category == 1:
                self.armors.append(Armor(*item))
            elif category == 2:
                self.shells.append(Shell(*item))
            return True
        return False
    
    # 0 : objet non possédé ; 1 : pas assez d'objet ; 2 : succès
    def use_stuff(self, stuff_name, nb):
        def get_index(name):
            for index, item in enumerate(self.stuff):
                if item.name == stuff_name: return index
            return -1

        index = get_index(stuff_name)

        if index == -1: return 0 # objet non possédé
        if self.stuff[index].nb_use >= nb:
            self.stuff[index].nb_use -= nb
            if self.stuff[index].nb_use == 0: self.del_item(stuff_name, 3)
            return 2

        return 1

    def have_capacity(self, cap_name):
        for index_1, archetype in enumerate(self.capacities):
            for index_2, capacity in enumerate(archetype):
                if capacity[0] == cap_name: return index_1, index_2 # la capacité est stockée dans : Player.capacities[index_1][index_2], de la forme (nom, utilisable ?)
        return -1, -1

    def rest(self, capa_data):
        for archetype in self.capacities:
            for capacity in archetype:
                if capa_data[capacity[0]][0] == "rencontre": capacity[1] = 1
        pass


    def night(self):
        # Récupération des points de vie
        self.stat[9] += self.natural_healing()
        max_pv = self.max_pv()
        if self.stat[9] > max_pv: self.stat[9] = max_pv

        for archetype in self.capacities:
            for capacity in archetype:
                capacity[1] = 1
        # recharger toute les capacités (rencontre et quotidienne)





class Weapon:
    def __init__(self, name, category, description, bonus):
        self.name = name
        self.category = category
        self.description = description
        self.bonus = bonus

    def export(self): return [self.name, self.category, self.description, self.bonus]


class Armor:
    def __init__(self, name, category, description, stat):
        self.name = name
        self.category = category
        self.description = description
        # stat = [Réduction de Dégâts (RD), Points d'Armure (PA), agilité maximale]
        self.stat = stat

    def export(self): return [self.name, self.category, self.description, self.stat]


class Shell:
    def __init__(self, name, description, shell_points):
        self.name = name
        self.description = description
        self.shell_points = shell_points

    def export(self): return [self.name, self.description, self.shell_points]


class Stuff:
    def __init__(self, name, description, nb_use):
        self.name = name
        self.description = description
        self.nb_use = nb_use

    def export(self): return [self.name, self.description, self.nb_use]


class Injury:
    def __init__(self, description):
        self.description = description

    def export(self): return self.description


