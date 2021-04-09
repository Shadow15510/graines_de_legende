import discord
from discord.ext import commands

from lib.gdl_lib import *

class StuffCommands(commands.Cog):
    def __init__(self, bot, config, player_data, cmnd_data, capa_data):
        self.bot = bot
        self.config = config

        self.player_data = player_data
        self.cmnd_data = cmnd_data
        self.capa_data = capa_data

    @commands.command()
    async def arme(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["arme"][0][0] <= len(args) <= self.cmnd_data["arme"][0][1]):
            await ctx.send(error("arme", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":
            if len(args) < 4:
                await ctx.send(error("arme", self.cmnd_data, *self.config[:2]))
                return

            if len(args) == 5: bonus = args[4]
            else: bonus = 0

            if player.add_item((args[1], args[2], args[3], get_weapon_bonus(args[2], bonus)), 0):
                await ctx.send(f"{player.name} reçoit : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : {player.name} a déjà cette arme.*")

        else:
            if len(args) > 2:
                await ctx.send(error("arme", self.cmnd_data, *self.config[:2]))
                return

            if player.del_item(args[1], 0):
                await ctx.send(f"{player.name} n'a plus l'arme : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : {player.name} n'a pas d'arme portant le nom : '{args[1]}'.*") 

        export_save(self.player_data)

    @commands.command()
    async def armure(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["armure"][0][0] <= len(args) <= self.cmnd_data["armure"][0][1]):
            await ctx.send(error("armure", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":
            if len(args) < 4:
                await ctx.send(error("armure", self.cmnd_data, *self.config[:2]))
                return

            stat = get_armor_stat(args[2])
            if player.add_item((args[1], args[2], args[3], stat), 1):
                if player.stat[0] > stat[2]: player.stat[0] = stat[2]
                await ctx.send(f"{player.name} reçoit : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : {player.name} a déjà cette armure.*")

        else:
            if len(args) > 2:
                await ctx.send(error("armure", self.cmnd_data, *self.config[:2]))
                return

            if player.del_item(args[1], 1):
                await ctx.send(f"{player.name} n'a plus l'armure : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : {player.name} n'a pas d'armure portant le nom : '{args[1]}'.*") 

        export_save(self.player_data)


    @commands.command()
    async def bouclier(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["bouclier"][0][0] <= len(args) <= self.cmnd_data["bouclier"][0][1]):
            await ctx.send(error("bouclier", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":
            if len(args) < 4:
                await ctx.send(error("bouclier", self.cmnd_data, *self.config[:2]))
                return

            if player.add_item((args[1], args[2], args[3]), 2):
                await ctx.send(f"{player.name} reçoit : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : {player.name} a déjà ce bouclier.*")

        else:
            if len(args) > 2:
                await ctx.send(error("bouclier", self.cmnd_data, *self.config[:2]))
                return

            if player.del_item(args[1], 2):
                await ctx.send(f"{player.name} n'a plus le bouclier : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : {player.name} n'a pas de bouclier portant le nom : '{args[1]}'.*") 

        export_save(self.player_data)

    @commands.command(name="objet", aliases=("équipement", "stuff"))
    async def objet(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["objet"][0][0] <= len(args) <= self.cmnd_data["objet"][0][1]):
            await ctx.send(error("objet", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":
            have = player.have_item(args[2])
            if have[1] == -1:
                player.stuff.append(Stuff(args[2], args[3], args[1]))
            else:
                player.stuff[have[1]].nb_use += args[1]

            await ctx.send(f"{player.name} reçoit : '{args[2]}' ({args[1]})")

        else:
            result = player.use_stuff(args[2], args[1])
            if result == 0:
                await ctx.send(f"*Erreur : {player.name} n'a pas d'objet portant le nom : '{args[2]}'.*") 
            elif result == 1:
                await ctx.send(f"*Erreur : {player.name} n'a pas l'objet '{args[2]}' en assez grand nombre.*")
            else:
                result = player.have_item(args[2])
                if result[1] == -1:
                    result = f"Vous n'avez plus l'objet : '{args[2]}'"
                else:
                    result = f"Il vous en reste {result[0][1][result[1]].nb_use}."

                await ctx.send(f"{player.name} a utilisé l'objet : '{args[2]}'\n{result}")

        export_save(self.player_data)

