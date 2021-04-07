import discord
from discord.ext import commands

from lib.gdl_lib import *


class GeneralCommands(commands.Cog):
    def __init__(self, bot, config, player_data, cmnd_data):
        self.bot = bot
        self.config = config

        self.player_data = player_data
        self.cmnd_data = cmnd_data


    def __save(self):
        export_save(self.player_data)


    @commands.command()
    async def nouveau(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != self.cmnd_data["nouveau"][0][0]:
            await ctx.send(error("nouveau", self.cmnd_data, *self.config[:2]))
        
        elif ctx.author.id in self.player_data:
            await ctx.send(f"*Erreur : vous êtes déjà enregistré sous le nom de {self.player_data[ctx.author.id].name}.*")
        
        else:
            spec = ("agilité", "constitution", "force", "précision", "sens", "social", "survie", "volonté")

            stat_bad = spec.index(args[2].lower()), spec.index(args[3].lower())
            stat_excellent = spec.index(args[4].lower()), spec.index(args[5].lower())
            stat_default = ([1, 1], 20, 1000, randint(0, 16777215)) # XP, PV, monnaie de cuivre, couleur
            
            stat = [2 for i in range(12)]

            for i in range(12):
                if i in stat_bad: stat[i] = 1
                elif i in stat_excellent: stat[i] = 3
                elif i > 7: stat[i] = stat_default[i - 8]

            self.player_data[ctx.author.id] = Player(ctx.author.id, args[0], args[1], stat, ctx.author.avatar_url, args[6])

            player = self.player_data[ctx.author.id]
            player.stat[9] = player.max_pv()

            await ctx.send(f"{args[0]} enregistré.")

            self.__save()


    @commands.command(name="stat", aliases=("info", "information", "informations", "statistique", "statistiques"))
    async def stat(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) > self.cmnd_data["stat"][0][1]:
            await ctx.send(error("stat", self.cmnd_data["stat"], *self.config[:2]))
            return

        if args:
            target = get_id_from_nick(self.player_data, args[0])
        else:
            target = ctx.author.id

        if target not in self.player_data:
            if args: await ctx.send(f"*Erreur : {args[0]} n'est pas un joueur.*")
            else: await ctx.send("*Erreur : vous n'êtes pas un joueur.*")
            return

        player = self.player_data[target]

        gold, copper = player.get_money()

        if player.injuries: injuries = "\n".join([f" ❖ {i.description}" for i in player.injuries])
        else: injuries = "< aucune blessure >"

        if player.weapons:
            weapons = "\n".join([f" ❖ {i.name}" for i in player.weapons])
        else:
            weapons = "< aucune arme >"

        if player.armors:
            armor = "\n".join([f" ❖ {i.name}" for i in player.armors])
        else:
            armor = "< aucune armure >"

        if player.shells:
            shell = "\n".join([f" ❖ {i.name}" for i in player.shells])
        else:
            shell = "< aucun bouclier >"

        if player.stuff:
            stuff = "\n".join([f" ❖ {i.name} {(' (nombre restant : {} ) '.format(i.nb_use), '')[i.nb_use == 1]}" for i in player.stuff])
        else:
            stuff = "< aucun équipement > "

        if player.notes:
            notes = "\n".join(f"{i[0]} - {i[1]}" for i in player.notes)
        else:
            notes = "< aucune note >"

        spec_level = ("Exécrable", "Mauvais", "Moyen", "Excellent", "Mythique")
        
        fields = [
            ("Agilité", spec_level[player.stat[0]], True),      ("Sens", spec_level[player.stat[4]], True),       ("Expérience totale", f"{player.stat[8][0]} XP", True),
            ("Constitution", spec_level[player.stat[1]], True), ("Social", spec_level[player.stat[5]], True),     ("Langues", "\n".join([f" ❖ {i}" for i in player.languages]), True),
            ("Force", spec_level[player.stat[2]], True),        ("Survie", spec_level[player.stat[6]], True),     (". . .", ". . .", True),
            ("Précision", spec_level[player.stat[3]], True),    ("Volonté", spec_level[player.stat[7]], True),    (". . .", ". . .", True),
            
            (". . .", f". . .", True),                           (". . .", ". . .", True),                         (". . .", ". . .", True),
            
            ("Points de vie", f"{player.stat[9]} / {player.max_pv()} PV", True), ("Guérison naturelle", f"+{player.natural_healing()} PV", True), ("Blessures graves", injuries, True),
            ("Armes", weapons, True), ("Armures", armor, True), ("Boucliers", shell, True),
            ("Richesse", f"{gold} Pièce{('', 's')[gold > 1]} d'or\n{copper} Pièce{('', 's')[copper > 1]} de cuivre", True), ("Équipement", stuff, True),
            ("Notes", notes, False)]

        embed = make_embed(f"{player.name}\n", player.history, player.stat[11], fields, player.image)
        await ctx.send(embed=embed)


    @commands.command()
    async def test(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != self.cmnd_data["test"][0][0]:
            await ctx.send(error("test", self.cmnd_data["test"], *self.config[:2]))
        else:
            player = self.player_data[ctx.author.id]
            await ctx.send(("Échec", "Réussite")[roll(player, args[0], args[1])])


    @commands.command()
    async def formatage(self, ctx):
        if not ctx.author.id in self.config[2]:
            await ctx.send("*Erreur : commande non-autorisée*")
            return

        self.player_data = {}
        print("Sauvegarde formatée")
        self.__save()


    @commands.command()
    async def note(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 2:
            await ctx.send(error("note", self.cmnd_data, *self.config[:2]))
            return

        player = self.player_data[ctx.author.id]

        if args[0] == "+":
            player.add_note(args[1])
            await ctx.send(f"Vous avez ajouté une note : \n> {args[1]}")
        else:
            result = player.del_note(args[1])
            if result: await ctx.send(f"Vous avez supprimé la note :\n> {result}")
            else: await ctx.send(f"*Erreur : la note n°{args[1]} n'existe pas.*")

        self.__save()


    @commands.command()
    async def blessure(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["blessure"][0][0] <= len(args) <= self.cmnd_data["blessure"][0][1]):
            await ctx.send(error("blessure", self.cmnd_data, *self.config[:2]))
            return
        elif len(args) == 1: target = ctx.author.id
        else:
            if ctx.author.id in self.config[2]:
                target = get_id_from_nick(self.player_data, args[1])
            else:
                await ctx.send("*Erreur : commande non-autorisée.*")
                return

        player = self.player_data[target]
        player.injuries.append(Injury(args[0]))
        await ctx.send(f"{player.name} est blessé.e ! {args[0]}")

        self.__save()

    @commands.command(name="aide", aliases=("assistance", "doc", "documentation"))
    async def aide(self, ctx):
        fields = [(command, f"{display_syntax(command, self.cmnd_data[command], *self.config[:2])}\n{self.cmnd_data[command][2]}", False) for command in self.cmnd_data]
        embed = make_embed("Graines de Légendes — assistance", "Liste de toutes les commandes disponibles.", 8421504, fields)
        await ctx.send(embed=embed)