import discord
from discord.ext import commands

from lib.gdl_lib import *

class StuffCommands(commands.Cog):
    def __init__(self, bot, config, player_data, cmnd_data):
        self.bot = bot
        self.config = config

        self.player_data = player_data
        self.cmnd_data = cmnd_data


    def __save(self):
        export_save(self.player_data)


    @commands.command()
    async def arme(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["arme"][0][0] <= len(args) <= self.cmnd_data["arme"][0][1]):
            await ctx.send(error("arme", self.cmnd_data, *self.config[:2]))
            return

        player = self.player_data[ctx.author.id]

        if args[0] == "+":
            if len(args) < 4:
                await ctx.send(error("arme", self.cmnd_data, *self.config[:2]))
                return

            if not player.have_item(args[1])[0]:
                if len(args) == 5: bonus = args[4]
                else: bonus = 0
                player.weapons.append(Weapon(args[1], args[2], args[3], get_weapon_bonus(args[2], bonus)))
                await ctx.send(f"{player.name} reçoit : '{args[1]}'")
            else:
                await ctx.send(f"*Vous avez déjà cette arme.*")

        else:
            if len(args) > 2:
                await ctx.send(error("arme", self.cmnd_data, *self.config[:2]))
                return

            if player.del_item(args[1], 0):
                await ctx.send(f"Vous n'avez plus l'arme : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : Vous n'avez pas d'arme portant le nom : '{args[1]}'.*") 

        self.__save()

    @commands.command()
    async def armure(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["armure"][0][0] <= len(args) <= self.cmnd_data["armure"][0][1]):
            await ctx.send(error("armure", self.cmnd_data, *self.config[:2]))
            return

        player = self.player_data[ctx.author.id]

        if args[0] == "+":
            if len(args) < 4:
                await ctx.send(error("armure", self.cmnd_data, *self.config[:2]))
                return

            if not player.have_item(args[1])[0]:
                player.armors.append(Armor(args[1], args[2], args[3], get_armor_stat(args[2])))
                await ctx.send(f"{player.name} reçoit : '{args[1]}'")
            else:
                await ctx.send(f"*Vous avez déjà cette armure.*")

        else:
            if len(args) > 2:
                await ctx.send(error("armure", self.cmnd_data, *self.config[:2]))
                return

            if player.del_item(args[1], 1):
                await ctx.send(f"Vous n'avez plus l'armure : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : Vous n'avez pas d'armure portant le nom : '{args[1]}'.*") 

        self.__save()


    @commands.command()
    async def bouclier(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["bouclier"][0][0] <= len(args) <= self.cmnd_data["bouclier"][0][1]):
            await ctx.send(error("bouclier", self.cmnd_data, *self.config[:2]))
            return

        player = self.player_data[ctx.author.id]

        if args[0] == "+":
            if len(args) < 4:
                await ctx.send(error("bouclier", self.cmnd_data, *self.config[:2]))
                return

            if not player.have_item(args[1])[0]:
                player.shells.append(Shell(args[1], args[2], args[3]))
                await ctx.send(f"{player.name} reçoit : '{args[1]}'")
            else:
                await ctx.send(f"*Vous avez déjà ce bouclier.*")

        else:
            if len(args) > 2:
                await ctx.send(error("bouclier", self.cmnd_data, *self.config[:2]))
                return

            if player.del_item(args[1], 2):
                await ctx.send(f"Vous n'avez plus le bouclier : '{args[1]}'")
            else:
                await ctx.send(f"*Erreur : Vous n'avez pas de bouclier portant le nom : '{args[1]}'.*") 

        self.__save()

