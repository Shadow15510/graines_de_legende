# Graines de Légendes

## Présentation

### Bot Discord

De manière à faciliter les jeux de rôles par écrans interposés avec ce système. Le concept a été porté en Python en un bot Discord.

### Licence

Le bot et tous les fichiers de ce dépôt sont soumis à une licence GNU General Public Licence v3.0.

Cette licence ne concerne que le bot et ne s'applique pas au système en lui-même qui reste la propriété exclusive de son auteure.

## Installer Graines de Légendes sur un serveur

L'installation ne nécessite aucune compétence particulière. Il sera néanmoins nécessaire d'avoir quelques dépendances à savoir : 

 - git
 - pip3+
 - python 3+
 - discord.py

L'installation se déroule comme suit :

 - Installation des dépendances 
 - Clonage du dépôt
 - Création du bot
 - Ajout du bot à un serveur

### Installation des dépendances

#### git

Vous devez impérativement avoir git d'installer sur votre ordinateur. Savoir s'en servir n'est pas nécessaire, toutes les commandes à taper seront explicement notées.

Pour installer git il y a plein de tutos très bien fait : https://www.atlassian.com/fr/git

Dans les grandes lignes, soit vous passez pas un gestionnaire de paquet (brew pour MacOS, pacman pour Arch…) soit vous allez directement sur le site de git pour le télécharger.

#### pip3

Pip3 est un gestionnaire de paquet pour les modules Python. Il vous permet d'accéder à la base de données Pypi qui concentre une très grande quantité de modules (numpy, scipy, requests, discord…)

De même que pour git, l'installation ne pose pas de problème particulier et est bien documentée.

### Python

Il est impératif d'avoir une version supérieure à Python 3. Le bot a été programmé et testé avec Python 3.9.2 .

Encore une fois, les procédures sont multiples et diffèrent de beaucoup suivant votre OS.

#### discord

Ouvrez un terminal et entrez la commande : 

`$ sudo pip3 install discord`

Le terminal devrait vous demander le mot de passe administrateur et installer le module discord.py

### Cloner le dépôt

Dans un terminal, entrez : 

`$ git clone https://github.com/Shadow15510/graines_de_legendes.git`

Cette commande va copier l'intégralité du dépôt à la racine de votre répertoire personnel.

### Création du bot

Rendez-vous sur le site Discord Developer Portal et identifiez-vous. Cliquez sur le bouton 'New Application', en haut à droite. Dans la colonne de gauche, allez dans l'onglet bot, puis selectionnez 'Add Bot'. Confirmez.

### Ajout du bot à un serveur Discord

Dans l'onglet OAuth2, descendez au niveau du cadre 'SCOPES' et selectionnez la case 'bot' un second cadre nommé 'BOT PERMISSIONS' devrait appraître en dessous, sélectionnez 'Administrator'. Ouvrez le lien situé dans le champ, en bas du cadre 'SCOPES' et laissez-vous guider par Discord. (Identification, sélection du serveur, vérification)

Avant de fermez la fenêtre, retournez dans l'onglet Bot et copiez le token.

## Configurer Graines de Légendes

Dans votre répertoire personnel, allez dans le dossier `graines_de_legendes` et créez un fichier `config.json`. Ouvrez-le et insérez-y le code suivant : 

```
    {
        "TOKEN": < le token copié à l'étape précédente >,
        "PREFIX": "§",
        "SEPARATOR": ";",
        "XP": 1,
        "ADMIN": []
    }
```

À noter que le token doit être entre guillemets et doit rester secret.

Le préfix vous permettra d'appeller le bot lorsque vous jouerez, prenez un charactère simple, de préférence unique, évitez les charactères déjà pris (*, /, _, …).

Le sépérateur va séparer les arguments des commandes transmises au bot, de même vous pouvez mettre un caractère de votre choix. Évitez les virgules qui ne sont pas pratiques et les espaces qui produiront des erreurs.

L'XP est le nombre de points d'expérience que les joueur vont gagner par scéance de jeu. Par défaut chaque joueur reçoit donc 1 point d'expérience par scéance.

La liste ADMIN est la liste des idenfiants des maîtres du jeux qui auront ainsi accès à quelques commandes supplémentaires (surtout pour modérer les joueurs). Pour connaître l'idenfiant d'une personne, activez le mode développeur de Discord et faîtes clique droit sur la personne, dernière ligne 'copier l'identifiant'. Il s'agit bien d'un chiffre et non d'une chaîne de caractères.

## Jouer avec Graines de Légendes

### Lancer le bot

Ouvrez un terminal et entrez : 

`$ cd graines_de_legendes && python gdl_main.py && exit`

Si vous avez un doute sur la version de python installée sur votre ordinateur, vous pouvez forcer l'utilisation de python 3 en entrant : 

`$ cd graines_de_legendes && python3 gdl_main.py && exit`

Si vous avez changé de place le répertoire `graines_de_legendes` il faut préciser le chemin relatif en partant de la racine de votre répertoire personnel au niveau du `$cd`.

Par exemple si le répertoire `graines_de_legendes` est stocké dans un dossier `bots_discord` situé sur le bureau, la commande devient : 
    
`$ cd Bureau/bots_discord/graines_de_legendes && python gdl_main.py && exit`

### Premières commandes

La commande pour accéder à l'assistance est affichée dans le status personnalisé du bot. Par défaut la commande est `§aide`.

### Mettre le bot à jour

Si votre version du bot n'est plus à jour, vous pouvez mettre à jour votre dépôt local en entrant : 

`$ cd graines_de_legendes && git pull`

dans un terminal.

### Fichier créé par le bot

Le seul fichier créé par le bot est `gdl_save.txt` qui contient toute les statistiques des joueurs. Ce fichier n'est pas crypté et est tout à fait modifiable à la main. Lorsque le bot est éteint, ce fichier constitue sa seule mémoire, le supprimer revient à détruire la partie.

Normalement, si le fichier n'est pas corrompu, il ne devrait pas y avoir de problème de lecture. Mais faire un duplicata du fichier peut-être judicieux en cas de modification manuelle du fichier.
