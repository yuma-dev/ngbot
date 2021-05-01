import discord
import DiscordUtils
from discord.ext import commands
from typing import Optional


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("help.py working...")

    @commands.command()
    async def help(self, ctx, commandhelp : Optional[str]):
        if commandhelp is None:
            e1 = discord.Embed(color=discord.Color.magenta())
            #e1.set_thumbnail(url=ctx.me.avatar_url)
            e1.add_field(name="<:ngbotquestionmark:798559729038655488> **Help**", value="<:ngbotrs2:798673229937246218> `ng!help aesthetic`", inline=True)
            e1.add_field(name="<:ngbotehre2:798673244096954400> **Ehre**", value="<:ngbotrs2:798673229937246218> `ng!ehre pay @Yuma 3`", inline=True)
            e1.add_field(name="<:ngbotbirthday2:798673254025658368> **Geburtstage**", value="<:ngbotrs2:798673229937246218> `ng!geburtstage`", inline=True)
            e1.add_field(name="<:ngbotfun2:798673280667746374> **Spaß**", value="<:ngbotrs2:798673229937246218> `ng!pat @Nicolae Guta`", inline=True)
            e1.add_field(name="<:ngbotgames2:798673267925712966> **Spiele**",value="<:ngbotrs2:798673229937246218> `ng!typeracer`", inline=True)
            e1.add_field(name="<:ngbotutility2:798673530992197662> **Utility**",value="<:ngbotrs2:798673229937246218> `ng!userinfo @Yuma`", inline=True)
            e1.set_footer(text="Reagiere mit den Jeweiligen Emote um die Kategorie zu öffnen!\nFür Hilfe zu spezifischen Commands schreib einfach ng!help <Command>\n<> = Pflicht                                                    () = Optional                                                    [] = Eins davon")
        
            e2 = discord.Embed(title="<:ngbotehre2:798673244096954400> **Ehre**", color=discord.Color.magenta())
            e2.add_field(name="<:ngbotdot:798719264869449728> **ng!ehre**", value="<:ngbotrs2:798673229937246218> `Zeigt deine Ehre.`", inline=False)
            e2.add_field(name="<:ngbotdot:798719264869449728> **ng!ehre <@User>**", value="<:ngbotrs2:798673229937246218> `Zeigt User's Ehre.`", inline=False)
            e2.add_field(name="<:ngbotdot:798719264869449728> **ng!ehre pay│give│geben│gib│an│für <@User> <Anzahl>**", value="<:ngbotrs2:798673229937246218> `Bezahlt User die Anzahl an Ehre.`", inline=False)
            e2.add_field(name="<:ngbotdot:798719264869449728> **ng!ehre top**", value="<:ngbotrs2:798673229937246218> `Zeigt die top 10 Ehren.`", inline=False)
            e2.add_field(name="<:ngbotdot:798719264869449728> **ng!ehre add <@User> <Anzahl>**", value="<:ngbotrs2:798673229937246218> *`Gibt User die Anzahl an Ehre.`", inline=False)
            e2.add_field(name="<:ngbotdot:798719264869449728> **ng!ehre remove <@User> <Anzahl>**", value="<:ngbotrs2:798673229937246218> *`Nimmt User die Anzahl an Ehre.`", inline=False)
            e2.set_footer(text="*Nur für User mit der Rolle '💠│Family'\nFür Hilfe zu spezifischen Commands schreib einfach ng!help <Command>\n<> = Pflicht                                () = Optional                                [] = Eins davon")

            e3 = discord.Embed(title="<:ngbotbirthday2:798673254025658368> **Geburtstage**", color=discord.Color.magenta())
            e3.add_field(name="<:ngbotdot:798719264869449728> **ng!geburtstag│birthday│bd (@User)**", value="<:ngbotrs2:798673229937246218> `Zeigt deinen Geburtstag oder den des markierten Nutzers wenn bereits ein eingetragener Geburtstag vorhanden ist.`", inline=False)
            e3.add_field(name="<:ngbotdot:798719264869449728> **ng!geburtstag│birthday│bd (@User) <DD.MM>**", value="<:ngbotrs2:798673229937246218> `Setzt deinen Geburtstag oder den des markierten Nutzers zum angegebenen Datum.`", inline=False)
            e3.add_field(name="<:ngbotdot:798719264869449728> **ng!geburtstage│birthdays│bds**", value="<:ngbotrs2:798673229937246218> `Zeigt alle bekannten Geburtstage.`", inline=False)
            e3.set_footer(text="Für Hilfe zu spezifischen Commands schreib einfach ng!help <Command>\n<> = Pflicht                                () = Optional                                [] = Eins davon")

            e4 = discord.Embed(title="<:ngbotfun2:798673280667746374> **Spaß**", color=discord.Color.magenta())
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!wave│hello│hi**", value="<:ngbotrs2:798673229937246218> `Zeige anderen das du da bist.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!praise**", value="<:ngbotrs2:798673229937246218> `Praising intensifies.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!pat│headpat <@User>**", value="<:ngbotrs2:798673229937246218> `Streichelt einen User.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!fraktur <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen fraktur Text.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!aesthetics│ae <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen aesthetic Text.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!boldfraktur│bf <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen boldfraktur Text.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!fancy│ff <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen fancy Text.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!boldfancy│bff <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen boldfancy Text.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!double│doublestruck│ds <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen doublestruck Text.`", inline=False)
            e4.add_field(name="<:ngbotdot:798719264869449728> **ng!smallcaps│sc <Text>**", value="<:ngbotrs2:798673229937246218> `Generiert einen smallcaps Text.`", inline=False)
            e4.set_footer(text="Für Hilfe zu spezifischen Commands schreib einfach ng!help <Command>\n<> = Pflicht                                () = Optional                                [] = Eins davon")

            e5 = discord.Embed(title="<:ngbotgames2:798673267925712966> **Spiele**", color=discord.Color.magenta())
            e5.add_field(name="<:ngbotdot:798719264869449728> **ng!8Ball <Frage>**", value="<:ngbotrs2:798673229937246218> `Beantwortet deine Frage mit Positiven, Neutralen oder Negativen antworten.`", inline=False)
            e5.add_field(name="<:ngbotdot:798719264869449728> **ng!typeracer│tr**", value="<:ngbotrs2:798673229937246218> `Gibt dir einen Text den du so schnell wie möglich abschreiben musst, am Ende werden deine wpm berechnet.`", inline=False)
            e5.set_footer(text="Für Hilfe zu spezifischen Commands schreib einfach ng!help <Command>\n<> = Pflicht                                () = Optional                                [] = Eins davon")

            e6 = discord.Embed(title="<:ngbotutility2:798673530992197662> **Utility**", color=discord.Color.magenta())
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!ping**", value="<:ngbotrs2:798673229937246218> `Zeigt die Botlatenz.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!userinfo│ui│mi│memberinfo <@User>**", value="<:ngbotrs2:798673229937246218> `Zeigt alle vefügbaren Informationen zu diesem User.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!serverinfo│si│gi│guildinfo**", value="<:ngbotrs2:798673229937246218> `Zeigt alle verfügbaren Informationen zu diesem Server.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!botinfo│status│bi│up│uptime**", value="<:ngbotrs2:798673229937246218> `Zeigt alle verfügbaren informationen zu diesem Bot.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!random│rand (Zahl 1) <Zahl 2>**", value="<:ngbotrs2:798673229937246218> `Wählt eine zufällige Zahl zwischen Zahl 1(wenn nicht genannt 0) und Zahl 2.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!random│rand user**", value="<:ngbotrs2:798673229937246218> `Wählt einen zufälligen User aus diesem Server.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!random│rand coin**", value="<:ngbotrs2:798673229937246218> `Wirft eine Münze.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!random│rand choice <etwas1> <etwas2> <etwas3>...**", value="<:ngbotrs2:798673229937246218> `Entscheidet sich zwischen <etwas1> <etwas2> <etwas3>.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!say <Text>**", value="<:ngbotrs2:798673229937246218> `Lässt den Bot etwas sagen.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!log│archieve <Anzahl>**", value="<:ngbotrs2:798673229937246218> `Archiviert eine Anzahl an Nachrichten als Textdokument.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!snipe**", value="<:ngbotrs2:798673229937246218> `Snipe eine editierte oder gelöschte Nachricht.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!clear│bomb│purge│löschen│lösch <Anzahl>**", value="<:ngbotrs2:798673229937246218> `Löscht eine Anzahl an Nachrichten.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!timer│reminder <anzahl>h│m│s (Name)**", value="<:ngbotrs2:798673229937246218> `Setzt einen Timer mit einem Namen.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!addvote│vote│addvotes│votes**", value="<:ngbotrs2:798673229937246218> `Lässt User bei der letzten Nachricht mit Ja oder Nein abstimmen.`", inline=False)
            e6.add_field(name="<:ngbotdot:798719264869449728> **ng!addvote│vote│addvotes│votes <2-10>**", value="<:ngbotrs2:798673229937246218> `Lässt User bei der letzten Nachricht mit Zahlen abstimmen.`", inline=False)
            e6.set_footer(text="Für Hilfe zu spezifischen Commands schreib einfach ng!help <Command>\n<> = Pflicht                                () = Optional                                [] = Eins davon")
            
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True, timeout=120)
            paginator.add_reaction('<:ngbotquestionmark:798559729038655488>', "page 0")
            paginator.add_reaction('<:ngbotehre2:798673244096954400>', "page 1")
            paginator.add_reaction('<:ngbotbirthday2:798673254025658368>', "page 2")
            paginator.add_reaction('<:ngbotfun2:798673280667746374>', "page 3")
            paginator.add_reaction('<:ngbotgames2:798673267925712966>', "page 4")
            paginator.add_reaction('<:ngbotutility2:798673530992197662>', "page 5")
            paginator.add_reaction('<:ngbotx:798980683989123144>', "delete")
            embeds = [e1, e2, e3, e4, e5, e6]
            await paginator.run(embeds)
        else:
            try:
                command = self.bot.get_command(commandhelp)
                await ctx.send(f"{command} {command.aliases[0]} {command.signature}")
            except:
                await ctx.send("Dieser Command existiert nicht.")

    @commands.command()
    async def listcommands(self, ctx):
        for command in self.bot.walk_commands():
            await ctx.send(str(command) + " - " + str(command.aliases))


def setup(bot):
    bot.add_cog(Help(bot))
