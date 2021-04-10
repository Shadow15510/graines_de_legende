import discord
from discord.ext import commands

from lib.gdl_lib import *


class GeneralCommands(commands.Cog):
    def __init__(self, bot, config, player_data, cmnd_data, capa_data):
        self.bot = bot
        self.config = config

        self.player_data = player_data
        self.cmnd_data = cmnd_data
        self.capa_data = capa_data

    @commands.command()
    async def nouveau(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 2:
            await ctx.send(error("nouveau", self.cmnd_data, *self.config[:2]))
        
        elif ctx.author.id in self.player_data:
            await ctx.send(f"*Erreur : vous êtes déjà enregistré sous le nom de {self.player_data[ctx.author.id].name}.*")
        
        else:
            stat = [2 for _ in range(8)] + [[0, 0], 20, [0, 0], randint(0, 16777215)]
            self.player_data[ctx.author.id] = Player(ctx.author.id, args[0], args[1], stat, str(ctx.author.avatar_url))

            steps = [
                ("Choisir ses points faibles", f"Choisissez deux caractéristiques dans lesquelles vous serez mauvais.\n`{self.config[0]}carac 1 {self.config[1]} capacité 1 {self.config[1]} capacité 2`", False),
                ("Choisir ses points fort", f"Selectionnez deux caractéristiques parmis les six restantes\n`{self.config[0]}carac 3 {self.config[1]} capacité 1 {self.config[1]} capacité 2`", False),
                ("Écrire son histoire", f"`{self.config[0]}histoire contenu`", False),
                ("Régler son XP de départ", f"Cela va automatiquement régler vos richesses de départ.\n`{self.config[0]}xp montant`", False)]

            embed = make_embed("Création d'un nouveau joueur", "Vous avez commencé la création d'un joueur, veuillez suivres les étapes ci-dessous pour finaliser sa création.", 8421504, steps)
            await ctx.send(embed=embed)
            export_save(self.player_data)

    @commands.command(name="carac", aliases=("caractéristique", "caractéristiques"))
    async def carac(self, ctx, *, args=None):
        args = analize(args, self.config[1])
        if len(args) < 2:
            await ctx.send(error("carac", self.cmnd_data, *self.config[:2]))

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        spec_name = ("agilité", "constitution", "force", "précision", "sens", "social", "survie", "volonté")
        nb, spec = ('exécrable', 'mauvaise', 'moyenne', 'excellente', 'mythique').index(args[0].lower()), [spec_name.index(i.lower()) for i in args[1:]]

        for i in spec:
            player.stat[i] = nb

        max_pv = player.max_pv()
        if player.stat[9] > max_pv: player.stat[9] = max_pv

        if len(args[1:]) > 1: await ctx.send(f"Les caractéristiques : {', '.join(args[1:])} sont devenues {args[0]}.")
        else: await ctx.send(f"La caractéristique : {args[1]} est devenue {args[0]}.")
        export_save(self.player_data)

    @commands.command()
    async def histoire(self, ctx, *, args=None):
        args = analize(args, self.config[1])
        if len(args) != 1:
            await ctx.send(error("carac", self.cmnd_data, *self.config[:2]))

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        player.history = args[0]
        await ctx.send(f"L'histoire de {player.name} a été mise à jour.")

        export_save(self.player_data)

    @commands.command(name="xp", aliases=("expérience", "XP"))
    async def xp(self, ctx, *, args=None):
        args = analize(args, self.config[1])
        if len(args) != 1:         
            await ctx.send(error("xp", self.cmnd_data, *self.config[:2]))

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if player.stat[8][0] + player.stat[8][1] != 0:
            await ctx.send("*Erreur : vous ne pouvez pas changer votre expérience une fois la partie commencée.*")
            return

        player.stat[9] = player.max_pv()
        player.stat[8][1] = args[0]
        player.stat[10][0] = 10 * args[0]
        player.stat[12] = (10, 16, 20, 24, 30)[self.stat[1]]
        player.stat[13](2, 4, 5, 8, 15)[self.stat[1]]

        player.archetype[0][1] = 1
        player.capacities[1].append([get_capa_from_name(self.capa_data, player.species.lower(), 2)[0], 1])

        await ctx.send(f"L'expérience de {player.name} a été réglée sur {args[0]}\nVotre personnage est terminé !")
        export_save(self.player_data)


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

        gold, copper = player.stat[10]

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
            stuff = "\n".join([f" ❖ {i.name} {(' ({}) '.format(i.nb_use), '')[i.nb_use == 1]}" for i in player.stuff])
        else:
            stuff = "< aucun équipement > "

        if player.notes:
            notes = "\n".join(f"{i[0]} - {i[1]}" for i in player.notes)
        else:
            notes = "< aucune note >"

        spec_level = ("Exécrable", "Mauvais", "Moyen", "Excellent", "Mythique")
        
        fields = [
            ("Agilité", spec_level[player.stat[0]], True),      ("Sens", spec_level[player.stat[4]], True),       ("XP dépensés", f"{player.stat[8][0]} XP", True),
            ("Constitution", spec_level[player.stat[1]], True), ("Social", spec_level[player.stat[5]], True),     (". . .", ". . .", True),
            ("Force", spec_level[player.stat[2]], True),        ("Survie", spec_level[player.stat[6]], True),     (". . .", ". . .", True),
            ("Précision", spec_level[player.stat[3]], True),    ("Volonté", spec_level[player.stat[7]], True),    (". . .", ". . .", True),
            
            (". . .", f". . .", True),                           (". . .", ". . .", True),                         (". . .", ". . .", True),
            
            ("Points de vie", f"{player.stat[9]} / {player.stat[12]} PV", True), ("Guérison naturelle", f"+{player.stat[13]} PV", True), ("Blessures graves", injuries, True),
            ("Armes", weapons, True), ("Armures", armor, True), ("Boucliers", shell, True),
            ("Langues", "\n".join([f" ❖ {i}" for i in player.languages]), True), ("Richesse", f"{gold} Pièce{('', 's')[gold > 1]} d'or\n{copper} Pièce{('', 's')[copper > 1]} de cuivre", True), ("Équipement", stuff, True),
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
        export_save({})


    @commands.command()
    async def note(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 2:
            await ctx.send(error("note", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":
            player.add_note(args[1])
            await ctx.send(f"Vous avez ajouté une note : \n> {args[1]}")
        else:
            result = player.del_note(args[1])
            if result: await ctx.send(f"Vous avez supprimé la note :\n> {result}")
            else: await ctx.send(f"*Erreur : la note n°{args[1]} n'existe pas.*")

        export_save(self.player_data)


    @commands.command()
    async def blessure(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if not (self.cmnd_data["blessure"][0][0] <= len(args) <= self.cmnd_data["blessure"][0][1]):
            await ctx.send(error("blessure", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        player.injuries.append(Injury(args[0]))
        await ctx.send(f"{player.name} est blessé.e ! {args[0]}")

        export_save(self.player_data)

    @commands.command(name="aide", aliases=("assistance", "doc", "documentation"))
    async def aide(self, ctx):
        fields = [(command, f"{display_syntax(command, self.cmnd_data[command], *self.config[:2])}\n{self.cmnd_data[command][2]}", False) for command in self.cmnd_data]
        embed = make_embed("Graines de Légendes — assistance", "Liste de toutes les commandes disponibles.", 8421504, fields)
        await ctx.send(embed=embed)

    @commands.command()
    async def inventaire(self, ctx):
        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if player.weapons:
            weapons = "\n".join([f" ❖ **{i.name}** {i.category}, bonus de l'arme : {i.bonus}\n*{i.description}*" for i in player.weapons])
        else:
            weapons = "< aucune arme >"

        if player.armors:
            armors = "\n".join([f" ❖ **{i.name}** {i.category}, RD : {i.stat[0]}, PA : {i.stat[1]}, Agilité maximale : {('Exécrable', 'Mauvais', 'Moyen', 'Excellent', 'Mythique')[i.stat[2]]}\n*{i.description}*" for i in player.armors])
        else:
            armors = "< aucune armure >"

        if player.shells:
            shells = "\n".join([f" ❖ **{i.name}** Points de bouclier : {i.shell_points}\n*{i.description}*" for i in player.shells])
        else:
            shells = "< aucun bouclier >"

        if player.stuff:
            stuff = "\n".join([f" ❖ **{i.name}** nombre restant : {i.nb_use}\n*{i.description}*" for i in player.stuff])
        else:
            stuff = "< aucun équipement >"

        gold, copper = player.stat[10]
        fields = [("Richesse", f"{gold} Pièce{('', 's')[gold > 1]} d'or\n{copper} Pièce{('', 's')[copper > 1]} de cuivre", False), ("Armes", weapons, False), ("Armures", armors, False), ("Boucliers", shells, False), ("Équipement", stuff, False)]
        embed = make_embed(f"Inventaire de {player.name}", "Description de l'inventaire", player.stat[11], fields, player.image)
        await ctx.send(embed=embed)

    @commands.command()
    async def langue(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 2:
            await ctx.send(error("langue", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":
            player.languages.append(args[1])
            await ctx.send(f"{player.name} apprend une nouvelle langue : '{args[1]}'.")
        else:
            if args[1] in player.languages:
                player.languages.remove(args[1])
                await ctx.send(f"{player.name} oublie une langue : '{args[1]}'.")
            else:
                await ctx.send(f"*Erreur : {player^.name} ne connaît pas la langue : '{args[1]}'.*")

        export_save(self.player_data)

    @commands.command()
    async def richesse(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 3:
            await ctx.send(error("richesse", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "+":

            player.stat[10][0] += args[1]
            player.stat[10][1] += args[2]
            action = "reçoit"
        else:
            if args[1] > player.stat[10][0] or (args[2] > player.stat[10][1] + 100 * player.stat[10][0]):
                await ctx.send(f"*Erreur : {player.name} n'a pas assez de richesse.*")
                return
            else:
                while args[2] > player.stat[10][1]:
                    player.stat[10][0] -= 1
                    player.stat[10][1] += 100

            player.stat[10][0] -= args[1]
            player.stat[10][1] -= args[2]
            action = "donne"
                
        if args[1]:
            if args[2]:
                answer = f"{player.name} {action} {args[1]} pièce{('', 's')[args[1] > 1]} d'or et {args[2]} pièce{('', 's')[args[2] > 1]} de cuivre."
            else:
                answer = f"{player.name} {action} {args[1]} pièce{('', 's')[args[1] > 1]} d'or."
        else:
            if args[2]:
                answer = f"{player.name} {action} {args[2]} pièce{('', 's')[args[2] > 1]} de cuivre."
            else:
                answer = f"{player.name} ne {action} rien."

        await ctx.send(answer)

        export_save(self.player_data)


    @commands.command()
    async def vie(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 1:
            await ctx.send(error("vie", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        player.stat[9] += args[0]
        max_pv = player.max_pv()

        await ctx.send(f"{player.name} {('gagne', 'perd')[args[0] < 0]} {abs(args[0])} Point{('', 's')[abs(args[0]) > 1]} de vie.")

        if player.stat[9] < 0:
            player.stat[9] = 0
            await ctx.send(f"{player.name} est sur le point de mourir !")
        elif player.stat[9] > max_pv: player.stat[9] = max_pv

        export_save(self.player_data)


    @commands.command(name="repos", aliases=("sieste", "nuit", "dodo"))
    async def repos(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 1:
            await ctx.send(error("repos", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if args[0] == "long":
            player.night()
            await ctx.send(f"{player.name} dort profondément.")

        elif args[0] == "court":
            player.rest(self.capa_data)
            await ctx.send(f"{player.name} fait une sieste.")

        else:
            await ctx.send(error("repos", self.cmnd_data, *self.config[:2]))


    @commands.command(name="lancer", aliases=("dé", "dés", "lancé"))
    async def lancer(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) > 1:
            await ctx.send(error("lancer", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        if not args: nb = 1
        elif len(args) == 1: nb = args[0]

        if nb < 1: nb = 1
        await ctx.send(f"{player.name} lance {nb}d6. Résultat : {roll_dice(nb)} / {nb * 6}")

    @commands.command()
    async def max_pv(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 1:
            await ctx.send(error("max_pv", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        player.stat[12] = args[0]
        await ctx.send(f"La vie maximale de {player.name} est désormais de {args[0]} PV.")

        @commands.command(name="guérison")
    async def guerison(self, ctx, *, args=None):
        args = analize(args, self.config[1])

        if len(args) != 1:
            await ctx.send(error("guérison", self.cmnd_data, *self.config[:2]))
            return

        player = get_player_from_id(self.player_data, ctx.author.id)
        if not player:
            await ctx.send("*Erreur : vous n'est pas un joueur.*")
            return

        player.stat[13] = args[0]
        await ctx.send(f"La guérison naturelle de {player.name} est désormais de {args[0]} PV.")


            



