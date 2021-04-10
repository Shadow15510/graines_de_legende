import discord
from discord.ext import commands

from lib.gdl_lib import *

class CapacityCommands(commands.Cog):
    def __init__(self, bot, config, player_data, cmnd_data, capa_data):
        self.bot = bot
        self.config = config

        self.player_data = player_data
        self.cmnd_data = cmnd_data
        self.capa_data = capa_data

    @commands.command(name="capacité")
    async def capa(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["capacité"][0][0]<= len(args) <= self.cmnd_data["capacité"][0][1]):
            await ctx.send(error("capacité", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        # si pas d'argument : on affiche les capacités possédées par le joueur.
        if not args:
            # capacity : [(nom de la capacité, utilisable ?, archétype), ]
            capacity = [(i[0], i[1], self.capa_data[i[0]][3]) for i in player.capacities[0]]

            values = []
            for index, i in enumerate(player.archetype):
                if i[1]:
                    values.append(f"__{i[0].capitalize()}__\n" + "\n".join([f" {('❌', '❖')[j[1]]} {j[0]}" for j in player.capacities[index + 1]]))
                else:
                    values.append("< aucune capacité >")

            fields = [
                ("Capacités de base", "\n".join([f"❖ {j[0]}" for j in player.capacities[0]]), True), ("XP économisés", f"{player.stat[8][1]} XP", True), (". . .", ". . . ", True),
                (f"Ethnique", values[0], True),   (f"Commun", values[1], True),      (f"Légendaire", values[5], True),
                (f"Héroïque I", values[2], True), (f"Héroïque II", values[3], True), (f"Héroïque III", values[4], True)]

            embed = make_embed(f"Capacités de {player.name}", "", player.stat[11], fields, player.image)

        else:
            args[0] = args[0].lower()
            if not args[0] in self.capa_data:
                await ctx.send(f"*Erreur : la capacité '{args[0]}' n'existe pas.*")
                return

            details = self.capa_data[args[0]]
            fields = [
                ("Description", f"{details[2]}", False),
                ("Effet", details[3], False)]

            cost = capacity_xp_cost(details[4][0], details[4][2])
            if cost: cost = f"(coût : {cost} XP)"
            else: cost = ""

            footer = f"archétype {details[4][0]} ({details[4][1]}) {('', 'première capacité', 'seconde capacité', 'troisième capacité', 'quatrième capacité', 'cinquième capacité')[details[4][2]]} {cost}"

            color = (26367, 1179409, 16737792, 16716049)[("passif", "à volonté", "rencontre", "quotidien").index(details[0])] # bleu (passif), vert (à volonté), orange (rencontre), rouge (quotidien)
            embed = make_embed(args[0].capitalize(), f"{details[0]} - {details[1]}", color, fields)
            embed.set_footer(text=footer)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def utilise(self, ctx, *, args=None):
        args = analize(args, self.config[1])
        if len(args) != 1:
            await ctx.send(error("utilise", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        archetype, capacity = player.have_capacity(args[0])
        if archetype == -1:
            await ctx.send(f"*Erreur : vous n'avez pas cette capacité : '{args[0]}'")
        
        elif not player.capacities[archetype][capacity][1]:
            await ctx.send("*Erreur : vous devez vous reposez pour utiliser à nouveau cette capacité.*")
        
        else:
            await ctx.send(f"Vous utilisez la capacité : '{args[0]}'\n{self.capa_data[args[0]][3]}")
            if self.capa_data[args[0]][0] in ("rencontre", "quotidien"):
                player.capacities[archetype][capacity][1] = 0

        export_save(self.player_data)

    @commands.command()
    async def achat(self, ctx, *, args=None):
        args = analize(args, self.config[1])
        if len(args) > 1:
            await ctx.send(error("utilise", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        available = capa_available(player, self.capa_data)

        # si pas d'argument : affichage de toutes les capacités achetables
        if not args:

            values = []
            for archetype in available:
                if archetype: values.append("\n".join([f" ❖ {capacity}" for capacity in archetype]))
                else: values.append("< aucune capacité >")

            fields = [(i.capitalize(), values[index], True) for index, i in enumerate(("ethnique", "commun", "héroïque", "légendaire"))]
            embed = make_embed(f"Capacités achetables par {player.name}", "", player.stat[11], fields)
            await ctx.send(embed=embed)

        else:
            args[0] = args[0].lower()
            if not True in [args[0] in i for i in available]:
                await ctx.send(f"*Erreur : vous ne pouvez pas acheter la capacité : '{args[0]}'.*")
                return

            cost = capacity_xp_cost(self.capa_data[args[0]][4][0], self.capa_data[args[0]][4][2])
            if player.stat[8][1] >= cost:
                index = ("ethnique", "commun", "héroïque", "légendaire").index(self.capa_data[args[0]][4][0])
                
                player.capacities[index + 1].append([args[0], 1])
                player.archetype[index][0] = self.capa_data[args[0]][4][1]
                player.archetype[index][1] += 1
                
                player.stat[8][1] -= cost
                player.stat[8][0] += cost
                await ctx.send(f"{player.name} achète la capacité : '{args[0]}' pour {cost} XP.")
            else:
                await ctx.send("*Erreur : vous n'avez pas assez d'expérience.")

            export_save(self.player_data)










        

            
