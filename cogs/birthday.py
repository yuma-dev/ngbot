import discord, datetime, json, random
from discord.client import _cancel_tasks
from discord.ext import commands,tasks
from threading import Timer
import aioschedule as schedule
from typing import Optional


def getbdchannel(self, guildid):
    try:
        with open("data/birthdaychannel.json","r") as f:
            channels = json.load(f)

        return channels[str(guildid)]
    except KeyError:
        channels = 'None'

        return channels

def getprefix(self, guildid):
    with open("data/prefixes.json","r") as f:
        prefixes = json.load(f)

    return prefixes[str(guildid)]

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sometask.start()



    @tasks.loop(seconds=1)
    async def sometask(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S") # deutsche zeit : 12:00 - bot zeit : 11:00
        '''print("Current Time =", current_time)''' #DEBUG
        if(current_time == '09:53:00'):
            print("checking for birthdays...") #DEBUG
            with open("data/birthdays.json", "r") as x:
                load = json.load(x)
                today = datetime.date.today()
                format = "%d.%m"
                ftoday = today.strftime("%d.%m")
                
                for guild in self.bot.guilds:
                    channelid = getbdchannel(self, guild.id)
                    if channelid == "None":
                        print("no birthday channel set") #DEBUG
                    else:
                        channel = self.bot.get_channel(int(channelid))
                        for userid, birthday in load.items():
                            #for member in guildcheck.members:
                                #print(member) (didnt print anything)
                            if load[f'{userid}']['birthday'] == ftoday:
                                #print(f'userr = {userr.name} guildcheck = {guildcheck.name}')
                                if guild.get_member(int(userid)):
                                    print(f"{load[f'{userid}']} hat heute ({load[f'{userid}']['birthday']}) geburtstag!") #DEBUG
                                    user = self.bot.get_user(int(userid))
                                    await channel.send("@everyone eine Person hat Geburtstag!", delete_after=1)
                                    embed = discord.Embed(title=f"<a:6286_tada_animated:798299215881175050> {user.name}'s Geburtstag", description=f"<@{userid}> **hat heute Geburtstag!**\nSeid lieb und wünscht alles Gute. ", color=discord.Colour.from_hsv(random.random(), 1, 1))
                                    await channel.send(embed=embed)
                            else:
                                print(f"{userid} checked but not today.") #DEBUG
        else:
            return

    #change prefix in json
    @commands.command(aliases=["prefix","setprefix"])
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def config(self, ctx, type, argument : Optional[discord.TextChannel], prefix : Optional[str]):
        pconfignames = ['prefix','p','serverprefix']
        cconfignames = ['channel','Channel','birthdaychannel','bdchannel','c','bdc','channels','Channels','C','Birthdaychannel','BirthdayChannel','BDChannel','BdChannel']
        resetnames = ['reset','r','no','standard','normal']
        if type.casefold() in map(str.casefold, cconfignames):
            if argument:
                """Setzt den bdChannel des Servers."""
                with open("data/birthdaychannel.json", "r") as f:
                    channels = json.load(f)

                channels[str(ctx.guild.id)] = f"{argument.id}"

                with open("data/birthdaychannel.json", "w") as f:
                    json.dump(channels, f, indent=4)

                embed = discord.Embed(title=f"<a:ngyess:794406566107414569> der Geburtstag's Channel wurde geändert", description=f"Neuer Channel : {argument.mention}", color=discord.Colour.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"<a:ngnoo:794406650210942977> ERROR!", description=f"Kein Channel\nGib einen Channel mit `ng!config channel #channelmention` an", color=discord.Colour.red())
                await ctx.send(embed=embed)
        elif type.casefold() in map(str.casefold, pconfignames):
            if prefix:
                message = prefix
                if prefix.casefold() in map(str.casefold, resetnames):
                    prefix = ["ng!","Ng!","nG!","NG!","ng?","Ng?","nG?","NG?","ng ","Ng ","nG ","NG ","ng","Ng","nG","NG","nicolaeguta!"]
                    message = 'dem Standard'
                """Setzt den Prefix des Servers."""
                with open("prefixes.json", "r") as f:
                    prefixes = json.load(f)

                if prefix == ["ng!","Ng!","nG!","NG!","ng?","Ng?","nG?","NG?","ng ","Ng ","nG ","NG ","ng","Ng","nG","NG","nicolaeguta!"]:
                    prefixes[str(ctx.guild.id)] = prefix
                else:
                    prefixes[str(ctx.guild.id)] = [prefix]

                with open("prefixes.json", "w") as f:
                    json.dump(prefixes, f, indent=4)
                embed = discord.Embed(title=f"<a:ngyess:794406566107414569> der Prefix wurde zu `{message}` geändert", color=discord.Colour.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"<a:ngnoo:794406650210942977> ERROR!", description=f"Kein Prefix\nGib einen Prefix mit `ng!config prefix TEST` an", color=discord.Colour.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"<a:ngnoo:794406650210942977> ERROR!", description=f"Unbekannte Config", color=discord.Colour.red())
            await ctx.send(embed=embed)

    @config.error
    async def config_errorhandler(self,ctx, error):
        embed = discord.Embed(title=f"<:ngbotutility:798544515618570281> {ctx.guild.name}'s Config!", color=discord.Colour.purple())

        channelid = getbdchannel(self, ctx.guild.id)
        prefix = getprefix(self, ctx.guild.id)


        if channelid == 'None':
            channel = 'Kein Channel eingestellt!\nmit `ng!config channel #channelmention` setzt du den Channel.'
        else:
            channel = self.bot.get_channel(int(channelid))
            channel = channel.mention
        embed.add_field(name="Geburtstag's Channel", value=channel, inline=False)

        if prefix == ["ng!","Ng!","nG!","NG!","ng?","Ng?","nG?","NG?","ng ","Ng ","nG ","NG ","ng","Ng","nG","NG","nicolaeguta!"]:
            prefix = 'Standart Prefix eingestellt!\nGib einen neuen Prefix mit `ng!config prefix TEST` an.'
        else:
            prefix = f'`{prefix}`'
        embed.add_field(name="Prefix", value=prefix, inline=False)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def birthdayformat(self, ctx):
        await ctx.send("@test eine Person hat Geburtstag!", delete_after=1)
        embed = discord.Embed(title=f"<a:6286_tada_animated:798299215881175050> {ctx.author.name}'s Geburtstag ", description=f"<@{ctx.author.id}> **hat heute Geburtstag!**\nSeid lieb und wünscht alles Gute. ", color=discord.Colour.from_hsv(random.random(), 1, 1))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        self.daily.start()

    async def cog_unload(self):
        await self.daily.cancel()

    async def get_birthdays(self):
        with open("data/birthdays.json","r") as f:
            users = json.load(f)

        return users

    @commands.Cog.listener()
    async def on_ready(self):
        print("Birthday.py working...")

    @commands.command(aliases=["bdays","geburtstage","bds"])
    async def birthdays(self, ctx):
        with open("data/birthdays.json", "r") as x:
            load = json.load(x)
            today = datetime.date.today()
            format = "%d.%m"
            ftoday = today.strftime("%d.%m")
            pages = 1
            embed = discord.Embed(title="Alle Geburtstage", color=discord.Colour.magenta())
            count = 0
            for userid, birthday in load.items():
                if ctx.guild.get_member(int(userid)):
                    count =+ 1
                    user = self.bot.get_user(int(userid))
                    if count > 6:
                        pages = pages + 1
                    if load[f'{userid}']['birthday'] == ftoday:
                        embed.add_field(name=f"{user.name}", value="hat heute Geburtstag!", inline=False)
                    else:
                        embed.add_field(name=f"{user.name}", value=load[f'{userid}']['birthday'], inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=["istheutemeingeburtstag","geburtstagtest"])
    async def isitmybirthday(self, ctx):
        users = await self.get_birthdays()
        today = datetime.date.today()
        format = "%d.%m"
        ftoday = today.strftime("%d.%m")
        
        try:
            birthday = users[str(ctx.author.id)]["birthday"]
            if birthday == ftoday:
                await ctx.send("heute ist dein Geburtstag!")
            else:
                await ctx.send("heute ist nicht dein Geburtstag!")
        except KeyError:
            await ctx.send("du hast noch keinen eingetragegen Geburtstag!")

    @commands.command(aliases=["bd","geburtstag","bday"])
    async def birthday(self, ctx, user: Optional[discord.Member]=None, bd=None):
        #defining ["today","format","ftoday"]
        today = datetime.date.today()
        format = "%d.%m"
        ftoday = today.strftime("%d.%m")

        if user == None:
            #if no birthday is given
            if not bd:
                try:
                    users = await self.get_birthdays()
                    birthday = users[str(ctx.author.id)]["birthday"]
                    embed = discord.Embed(title="Dein Geburtstag!", description=f"Dein eingetragener Geburstag ist am {birthday}", color=discord.Color.magenta())
                    await ctx.send(embed=embed)
                except KeyError:
                    embed = discord.Embed(title="Error", description="Dein Datum war nicht richtig!\nVersuche es mit (Tag).(Monat) in Zahlen", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                if bd == 'remove':
                    try:
                        with open("data/birthdays.json", "r") as f:
                            birthday = json.load(f)

                        birthday.pop(str(ctx.author.id))

                        with open("data/birthdays.json", "w") as f:
                            json.dump(birthday, f, indent=4)
                        embed = discord.Embed(title="Success:", description="Dein Geburtstag wurde entfernt!", color=discord.Color.green())
                        await ctx.send(embed=embed)
                        return
                    except Exception:
                        embed = discord.Embed(title="Error:", description="Dein Geburtstag wurde noch nicht eingetragen!", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return
                try:
                    datetime.datetime.strptime(bd, format)
                    #current date and given date (debug message)
                    '''await ctx.send(f"das heutige datum ist: **{ftoday}**\nDein angegebenes Datum ist: **{bd}**")'''
    
                    users = await self.get_birthdays()

                    if str(ctx.author.id) in users:
                        #user already exists
                        users[str(ctx.author.id)]["birthday"] = bd
                        embed = discord.Embed(title="Error:", description="Dein Geburtstag wurde bereits eingetragen\nZum ändern eines Geburtstages bitte yuma kontaktieren!", color=discord.Color.red())
                        embed.add_field(name="Dein Geburtstag:",value=f"{bd}")
                        await ctx.send(embed=embed)
                    else:
                        #create user with birthday
                        users[str(ctx.author.id)] = {}
                        users[str(ctx.author.id)]["birthday"] = bd
                        embed = discord.Embed(title="Geburtstag", description="Dein Geburtstag wurde eingetragen!\nZum Ändern deines Geburtstages kontaktiere bitte yuma", color=discord.Color.magenta())
                        embed.add_field(name="**ID**", value=f"{ctx.author.id}")
                        embed.add_field(name="**Datum**", value=f"{bd}")
                        await ctx.send(embed = embed)
                        with open("data/birthdays.json","w") as f:
                            json.dump(users,f,indent=4)
                except ValueError:
                    #date doesnt match the date format
                    embed = discord.Embed(title="Error", description="Dein Datum war nicht richtig!\nVersuche es mit (Tag).(Monat) in Zahlen", color=discord.Color.red())
                    await ctx.send(embed=embed)

        else:
            if not bd:
                try:
                    users = await self.get_birthdays()
                    birthday = users[str(user.id)]["birthday"]
                    embed = discord.Embed(title=f"{user}'s Geburtstag!", description=f"Der eingetragene Geburstag ist am **{birthday}**", color=discord.Color.magenta())
                    await ctx.send(embed=embed)
                except KeyError:
                    embed = discord.Embed(title="Error", description="Dein Datum war nicht richtig!\nVersuche es mit (Tag).(Monat) in Zahlen", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                try:
                    datetime.datetime.strptime(bd, format)
                    #current date and given date (debug message)
                    '''await ctx.send(f"das heutige datum ist: **{ftoday}**\nDein angegebenes Datum ist: **{bd}**")'''
    
                    users = await self.get_birthdays()

                    if str(user.id) in users:
                        #user already exists
                        users[str(user.id)]["birthday"] = bd
                        embed = discord.Embed(title=f"Error :", description="Der Geburtstag wurde bereits eingetragen\nZum ändern eines Geburtstages bitte yuma kontaktieren!", color=discord.Color.red())
                        embed.add_field(name=f"{user}'s eingetragener Geburtstag:",value=f"{bd}")
                        await ctx.send(embed=embed)
                    else:
                        #create user with birthday
                        users[str(user.id)] = {}
                        users[str(user.id)]["birthday"] = bd
                        embed = discord.Embed(title=f"{user}'s Geburtstag", description=f"{user.mention}, dein Geburtstag wurde für dich von {ctx.author.mention} eingetragen!\nZum Ändern deines Geburtstages kontaktiere bitte yuma", color=discord.Color.magenta())
                        embed.add_field(name="**ID**", value=f"{user.id}")
                        embed.add_field(name="**Datum**", value=f"{bd}")
                        await ctx.send(embed = embed)
                        with open("data/birthdays.json","w") as f:
                            json.dump(users,f,indent=4)
                except ValueError:
                    #date doesnt match the date format
                    embed = discord.Embed(title="Error", description="Dein Datum war nicht richtig!\nVersuche es mit (Tag).(Monat) in Zahlen", color=discord.Color.red())
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Birthday(bot))

