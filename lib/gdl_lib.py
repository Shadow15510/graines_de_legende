import discord
from lib.gdl_objects import *
from random import randint

# Fonction du jeu

# roll : test de caractérique
def roll(player, spec, level):
    minimum = player.get_minimum(spec)

    level = ("très facile", "facile", "moyen", "difficile", "très difficile", "inacessible").index(level.lower())
    nb_dice, success_target = [(3, 1), (2, 1), (1, 1), (2, 2), (3, 3), (4, 4)][level]

    success = 0
    for _ in range(nb_dice):
        if randint(1, 6) > minimum: success += 1

    return success >= success_target


# roll_dice : simule un lancer de dé
def roll_dice(nb_dice=1):
    return randint(nb_dice, nb_dice * 6)


# get_weapon_bonus : renvoie le bonus de l'arme en fonction de sa catégorie
def get_weapon_bonus(weapon_category, bonus=0):
    weapon_type = ("arme inadaptée", "arme légère", "arme intermédaire", "arme lourde", "arme naturelle").index(weapon_category.lower())
    return (-2, 0, 2, 4, bonus)[weapon_type]


# get_armor_type : renvoie les statistiques de l'armure en fonction de sa catégorie
def get_armor_stat(armor_category):
    armor_type = ("pièce d'armure", "armure légère", "armure intermédaire", "armure lourde").index(armor_category.lower())
    return ((1, 6, 3), (2, 16, 2), (4, 40, 1), (6, 72, 0))[armor_type]


# capacity_xp_cost : retourne le prix en XP d'une capacité en fonction du type de son archétype et de son rang dans l'archétype
def capacity_xp_cost(cap_type, cap_rank):
    calc = lambda n: (n + 1) // 2

    if cap_type == "commun":
        return 1
    if cap_type in ("ethnique", "héroïque"):
        if cap_type == "ethnique" and not cap_rank: return 0
        return calc(cap_rank)
    if cap_type == "legendaire":
        return 2 ** calc(cap_rank)


# get_capa_from_type : retourne toutes les capacités d'un archétype d'un type donné
def get_capa_from_type(capa_data, target, limit):
    return [capacity for capacity in capa_data if capa_data[capacity][4][2] <= limit + 1 and capa_data[capacity][4][0] == target]


# get_capa_from_name : retourne toutes les capacités d'un archétype d'un nom donné
def get_capa_from_name(capa_data, target, limit):
    return [capacity for capacity in capa_data if capa_data[capacity][4][2] <= limit + 1 and capa_data[capacity][4][1] == target]


# capa_available : retourne la liste des capacités achetables
def capa_available(player, capa_data):
    def get(player, capa_data, index, name):
        if player.archetype[index][0]: return get_capa_from_name(capa_data, player.archetype[index][0], player.archetype[index][1])
        else: return get_capa_from_type(capa_data, name, 5)

    capacity = [get_capa_from_name(capa_data, player.species.lower(), player.archetype[0][1])] # capacité ethniques
    capacity.append(get(player, capa_data, 1, "commun")) # capacité communes

    if player.archetype[1][1] >= 3: # le joueur à accès aux catégories suppérieures
        for i in range(2, 4): # les capacités Héroïques I, II
            capacity.append(get(player, capa_data, i, "héroïque"))

        if player.archetype[2][1] >= 3 or player.archetype[3][1] >= 3: # Accès à la catégorie héroïque III
            capacity.append(get(player, capa_data, 4, "héroïque"))
        else:
            capacity.append([])
    else:
        capacity.append([])

    if player.stat[8][0] > 30:
        capacity.append(get(player, capa_data, 5, "légendaire"))
    else:
        capacity.append([])

    answer = []
    for i in range(len(capacity)):
        answer.append([capacity[i][j] for j in range(len(capacity[i])) if player.have_capacity(capacity[i][j]) == (-1, -1)])
    return answer






# Fonctions vitales du bot

# analize : séparare les arguments en fonction d'un sépérateur
def analize(arguments, separator):
    if not arguments: return []
    arguments = arguments.split(separator)

    for index, value in enumerate(arguments):
        try: arguments[index] = int(value)
        except: arguments[index] = value.strip().rstrip()

    return arguments


# error : affiche une erreur en cas de syntaxe incorrecte
def error(name, doc, prefix, separator):
    return f"*Erreur : syntaxe incorrecte* {display_syntax(name, doc[name], prefix, separator)}"


# display_syntax : retourne la syntaxe d'une commande du bot
def display_syntax(name, documentation, prefix, separator):
    arguments = []
    for index, arg in enumerate(documentation[1]):
        if index + 1 <= documentation[0][0]: arguments.append(f"< {arg} >")
        else: arguments.append(f"[< {arg} >]")

    arguments = f" {separator} ".join(arguments)
    return f"`{prefix}{name} {arguments}`"


# get_if_from_nick : retourne l'id d'un joueur en fonction de son nom (None sinon)
def get_id_from_nick(data_player, player_nick):
    for player_id in data_player:
        if data_player[player_id].name == player_nick: return player_id


# get_player_from_id : renvoie l'objet Player associé à l'id passé en argument
def get_player_from_id(data_player, player_id):
    if player_id in data_player: return data_player[player_id]


# make_embed : fabrique un embed et le renvoie
def make_embed(title, description, color, fields, image=None):
    answer = discord.Embed(title=title, description=description, color=color)

    for i in fields:
        answer.add_field(name=i[0], value=i[1], inline=i[2])
    if image: answer.set_thumbnail(url=image)

    return answer


# export_save : enregistre les joueurs dans 'save.txt'
def export_save(data_player):
    print("Enregistrement de la partie")
    save = [data_player[player_id].export() for player_id in data_player]
    with open("gdl_save.txt", "w") as file:
        file.write(str(save))


# load_save : charge les joueurs depuis 'save.txt'
def load_save():
    print("Chargment de la partie")
    try:
        with open("gdl_save.txt", "r") as file:
            save = file.read()
        print("# partie chargée")
        return {player[0]: Player(*player) for player in eval(save)}
    
    except:
        print("# aucune partie trouvée\n# création d'une nouvelle partie")
        with open("gdl_save.txt", "w") as file:
            file.write("[]")
        return {}
