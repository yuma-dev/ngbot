import random,asyncio,discord,json,requests
from datetime import datetime
from collections import Counter
from discord.ext import commands
import xml.etree.ElementTree as ET
from typing import Optional

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def userOnline(self, memberList):
        online = []
        for i in memberList:
            if i.status == discord.Status.online and i.bot == False:
                online.append(i)
        return online

    def checkRole(self, user, roleRec):
        ok = False
        for all in list(user.roles):
            if all.name == roleRec:
                ok = True
        return ok

    @commands.command(aliases=['wetter','temp','temperatur'])
    async def weather(self, ctx,state):
        data = requests.request('GET', f'https://api.openweathermap.org/data/2.5/weather?q={state}&lang=de&units=metric&appid=090e84661d1e4bfdb2aeb4fd3b57d916').json()
        if str(data['cod'])=='200':
            em = discord.Embed(title=f"Wetter in {data['name']}",color=discord.Color.magenta())
            em.add_field(name="Wetter", value=f"{data['weather'][0]['description']}", inline=False)
            em.add_field(name="Temperatur", value=f"{data['main']['temp']}°C", inline=False)
            em.add_field(name="Gefühlte Temperatur", value=f"{data['main']['feels_like']}°C", inline=False)
            
            await ctx.reply(embed=em)
        else:
            embed = discord.Embed(title=f"<a:ngnoo:794406650210942977> ERROR!", description=f"Daten konnten nicht geladen werden!\nBitte überprüfe deinen angegebenen Ort.", color=discord.Colour.red())
            await ctx.reply(embed=embed)
            
    @commands.command()
    async def apitest(self,ctx,type):
        gifurl = requests.request("GET", "https://anime-reactions.uzairashraf.dev/api/reactions/random", params={'category': f"{type}"}).json()['reaction']
        embed = discord.Embed(title=f"{type}'s response!", color=discord.Color.magenta())
        embed.set_image(url=gifurl)
        await ctx.message.reply(embed=embed)        

    @commands.command()
    async def mlem(self, ctx):
        gifurl = requests.request("GET", "https://mlemapi.p.rapidapi.com/randommlem", headers={'x-rapidapi-key': "6b479c1fedmsh3f6ca5b936647b9p1e018fjsn17685d7ed76f",'x-rapidapi-host': "mlemapi.p.rapidapi.com"}).json()['url']
        embed = discord.Embed(title="Mlem!", color=discord.Color.magenta())
        embed.set_image(url=gifurl)
        await ctx.message.reply(embed=embed)

    @commands.command(aliases=['wave', 'hi', 'ohaiyo'])
    async def hello(self, ctx):
        '''Nonsense gifs zum Hallo sagen'''
        gifs = ['https://cdn.discordapp.com/attachments/102817255661772800/219512763607678976/large_1.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219512898563735552/large.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518948251664384/WgQWD.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518717426532352/tumblr_lnttzfSUM41qgcvsy.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519191290478592/tumblr_mf76erIF6s1qj96p1o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519729604231168/giphy_3.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519737971867649/63953d32c650703cded875ac601e765778ce90d0_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519738781368321/17201a4342e901e5f1bc2a03ad487219c0434c22_hq.gif',
                'https://media.discordapp.net/attachments/614549835017748491/784915358472863785/68794837-352-k448198.png?width=173&height=270']
        embed = discord.Embed(title="<a:2112_wave_animated:798295966331174972>", color=discord.Color.magenta())
        embed.set_image(url=random.choice(gifs))
        await ctx.send(embed=embed)

    #WIP
    @commands.command(aliases=['customize', 'custom'])
    async def personalize(self, ctx):
        embed = discord.Embed(title="Personalize your Profile!", description="Wähle von eine dieser Farben:\nBlau, Gold, Grün, Orange, Random und Rot", color=discord.Colour.magenta())
        embed1 = await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author 
        
        try:
            message = await self.bot.wait_for('message', timeout=30, check=check)
            embed = discord.Embed(title="Deine Personalisierung:", color=discord.Colour.magenta())
            if message.content == "Blau":
                personalcolor = discord.Color.blue()
                colorname = "Blau"
            if message.content == "Gold":
                personalcolor = discord.Color.gold()
                colorname = "Gold"
            if message.content == "Grün":
                personalcolor = discord.Color.green()
                colorname = "Grün"
            if message.content == "Orange":
                personalcolor = discord.Color.orange()
                colorname = "Orange"
            if message.content == "Random":
                personalcolor = discord.Color.random()
                colorname = discord.Colour.from_hsv(random.random(), 1, 1)
            if message.content == "Rot":
                personalcolor = discord.Color.red()
                colorname = "Rot"
            else:
                embed = discord.Embed(title="!!!!!!", description="Scheint so als hättest du eine Falsche Farbe angegeben", color=discord.Colour.red())
                await embed1.edit(embed=embed)
                return
                
            embed.add_field(name="Deine Farbe : ", value=colorname)
            await embed1.edit(embed=embed)

            ###part 2###

            embed = discord.Embed(title="Personalize your Profile!", description="Wähle von eines dieser Emojis:\n🌻 🔥 🐸 🐹 ❤️ 💮 ☣️ 🎴 🃏 🐣 🐲 🐢 ", color=discord.Colour.gold())
            embed2 = await ctx.send(embed=embed)

            def check(message):
                return message.author == ctx.author 
            try:
                message2 = await self.bot.wait_for('message', timeout=30, check=check)
                embed = discord.Embed(title="Deine Personalisierung:", color=discord.Colour.magenta())
                embed.add_field(name="Deine Farbe : ", value=colorname)
                if message2.content == "🌻":
                    emoji = "🌻"
                if message2.content == "🔥":
                    emoji = "🔥"
                if message2.content == "🐸":
                    emoji = "🐸"
                if message2.content == "🐹":
                    emoji = "🐹"
                if message2.content == "❤️":
                    emoji = "❤️"
                if message2.content == "💮":
                    emoji = "💮"
                if message2.content == "☣️":
                    emoji = "☣️"
                if message2.content == "🎴":
                    emoji = "🎴"
                if message2.content == "🃏":
                    emoji = "🃏"
                if message2.content == "🐣":
                    emoji = "🐣"
                if message2.content == "🐲":
                    emoji = "🐲"
                if message2.content == "🐢":
                    emoji = "🐢"
                else:
                    embed = discord.Embed(title="!!!!!!", description="Scheint so als hättest du ein Falsches Emoji angegeben", color=discord.Colour.red())
                    await embed1.edit(embed=embed)
                    await embed2.purge()
                embed.add_field(name="Dein Emoji : ", value=emoji)
                await embed1.edit(embed=embed)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout!", description="Ich habe keine Antwort bekommen :c", color=discord.Colour.red())
                await embed1.edit(embed=embed)
                await embed2.purge()
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Timeout!", description="Ich habe keine Antwort bekommen :c", color=discord.Color.red())
            await embed1.edit(embed=embed)

    @commands.command(aliases=['headpat'])
    async def pat(self, ctx, member: discord.Member = None):
        '''/r/headpats Pat Pat Pat :3
        Beispiel:
        -----------
        ng!pat @yuma#8840
        '''
        gifs = ['https://thumbs.gfycat.com/FabulousCavernousAegeancat-max-1mb.gif',
                'https://community.gamepress.gg/uploads/default/original/3X/6/6/664e58e013a8d2c3c3c8a4684aaeb192d1def025.gif',
                'https://i.kym-cdn.com/photos/images/newsfeed/001/211/282/46f.gif',
                'https://64.media.tumblr.com/1105ec75e8c13d44531e1f36ddd1bfeb/tumblr_plqphoZeni1th206io1_400.gifv',
                'https://thumbs.gfycat.com/FlimsyDeafeningGrassspider-size_restricted.gif',
                'https://media.giphy.com/media/N0CIxcyPLputW/giphy.gif',
                'https://media1.tenor.com/images/098a45951c569edc25ea744135f97ccf/tenor.gif',
                'https://i.pinimg.com/originals/ec/b8/7f/ecb87fb2827a022884d5165046f6608a.gif',
                'https://data.whicdn.com/images/314492875/original.gif',
                'https://i.gifer.com/KJ42.gif',
                'https://media.tenor.com/images/1d37a873edfeb81a1f5403f4a3bfa185/tenor.gif',
                'https://i.imgur.com/IqGRUu4.gif',
                'https://68.media.tumblr.com/f95f14437809dfec8057b2bd525e6b4a/tumblr_omvkl2SzeK1ql0375o1_500.gif',
                'https://i.imgur.com/UWbKpx8.gif',
                'https://64.media.tumblr.com/cadf248febe96afdd6869b7a95600abb/tumblr_onjo4cGrZE1vhnny1o1_500.gifv',
                'https://i.pinimg.com/originals/c2/34/cd/c234cdcb3af7bed21ccbba2293470b8c.gif',
                'https://media.tenor.com/images/ad8357e58d35c1d63b570ab7e587f212/tenor.gif',
                'https://media1.tenor.com/images/bb5608910848ba61808c8f28caf6ec7d/tenor.gif',
                'https://thumbs.gfycat.com/BlushingDeepBlacknorwegianelkhound-small.gif',
                'https://i.pinimg.com/originals/2e/27/d5/2e27d5d124bc2a62ddeb5dc9e7a73dd8.gif',
                'https://media.discordapp.net/attachments/614549835017748491/784915653718573076/uh_uh_ah_ah_fuxk_yes_sexy_monk.jpg?width=911&height=683']

        if member == ctx.me:
            embed = discord.Embed(title="<a:5634_kenma_squishy:798497657483427850>", description=f'HAI IN MERCEDESS , DANKE DANKE {ctx.author.mention}', color=discord.Color.magenta())
            embed.set_image(url="https://cdn.knd.ro/media/521/2861/35027/16364310/2/media-144854897040129900.jpg")
            await ctx.send(embed=embed)
        elif member is not None:
            embed = discord.Embed(title="<a:5634_kenma_squishy:798497657483427850>", description=f"{ctx.author.mention} tätschelt dich {member.mention}", color=discord.Color.magenta())
            embed.set_image(url=random.choice(gifs))
            await ctx.send(embed=embed)

    @commands.command(aliases=['rand'])
    async def random(self, ctx, *arg):
        '''Gibt eine zufällige Zahl oder Member aus
        Benutzung:
        -----------
        :random
            Gibt eine zufällige Zahl zwischen 1 und 100 aus
        :random coin
            Wirft eine Münze (Kopf oder Zahl)
        :random 6
            Gibt eine zufällige Zahl zwischen 1 und 6 aus
        :random 10 20
            Gibt eine zufällige Zahl zwischen 10 und 20 aus
        :random user
            Gibt einen zufällige Benutzer der gerade online ist aus

        :random choice Dani Eddy Shinobu
            Wählt aus der vorgegebenen Liste einen Namen aus
        '''
        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['Kopf', 'Zahl']
                embed = discord.Embed(title="<:9243_DiscordCoin:798499968468910101>", description=f"{random.choice(coin)}", color=discord.Color.magenta())
                await ctx.send(embed=embed)
                return
            elif arg[0] == 'choice':
                choices = list(arg)
                choices.pop(0)
                embed = discord.Embed(title="<a:6286_tada_animated:798299215881175050>", description=f"Der Gewinner ist {random.choice(choices)}", color=discord.Color.magenta())
                await ctx.send(embed=embed)
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.guild.members)
                randomuser = random.choice(online)
                if ctx.channel.permissions_for(ctx.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                embed = discord.Embed(title="<a:6286_tada_animated:798299215881175050>", description=f"Der Gewinner ist {user}", color=discord.Color.magenta())
                await ctx.send(embed=embed)
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) == 2:
                start = int(arg[0])
                end = int(arg[1])
            embed = discord.Embed(title="<a:3339_loading:798295984626991136>", description=f"Zufällige Zahl ({start} - {end}): {random.randint(start, end)}", color=discord.Color.magenta())
            await ctx.send(embed=embed)



    @commands.command()
    async def praise(self, ctx):
        '''Praise the Sun'''
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')


    @commands.Cog.listener()
    async def on_ready(self):
        print("fun.py working...")

    @commands.command()
    async def profile(self, ctx, user: Optional[discord.User]):
        #mongo_url = "mongodb+srv://yuma:96209245@ngbot.qb425.mongodb.net/<dbname>?retryWrites=true&w=majority"
        #cluster = MongoClient(mongo_url)
        #db = cluster["ngdatabase"]
        #collection = db["level"]

        if user is None:
            user = ctx.author
        #user_id = {"_id": user.id}
        #exp = collection.find(user_id)

        #for xp in exp:
            #cur_xp = xp["Messages"]
        with open('data/claimed.json') as react_file:
            data = json.load(react_file)
            claimers = " " 
            for x in data:
                if x['claimed'] == user.id:
                    cuser = await self.bot.fetch_user(x['by'])
                    claimers += str("\n") + str(cuser.mention)
        if claimers == " ":
            claimers = "Niemand\n_claime jemanden mit ng!claim <@784215168561184788>_"

        embed = discord.Embed(title=f"{user.name}'s Profile", color=discord.Color.magenta(), timestamp=datetime.utcnow())
        embed.add_field(name="Name", value=user.name, inline=False)
        embed.add_field(name="Geclaimed von :", value=claimers, inline=False)
        embed.set_thumbnail(url=user.avatar_url)

        birthdayy = False
        with open("data/birthdays.json","r") as f:
            users = json.load(f)
            print("defining x")
            for x in users:
                print("testing x")
                print(f"{x}")
                print(f"{user.id}")
                if f"{x}" == f"{user.id}":
                    print("x == user.id")
                    embed.add_field(name="Geburtstag", value=users[x]['birthday'],inline=True)
                    birthdayy = True
                else:
                    print("\n")
        if birthdayy == False:
            embed.add_field(name="Geburtstag", value="Nicht Eingetragen\n_trage dich mit ng!bd DD.MM ein._",inline=True)

        #embed.add_field(name="Nachrichten", value=cur_xp, inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def unclaim(self, ctx, user: Optional[discord.User]):
        if user is None:
            await ctx.send("Gib einen User an.")
            
        if user.id == 178525733600100352:
            with open('data/claimed.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['claimed'] == user.id:
                        if x['by'] == ctx.author.id:
                            pop(x['by'])
                            pop(x['claimed'])
                            await ctx.send("deleted.")
                    if x['claimed'] == ctx.author.id:
                        if x['by'] == user.id:
                            del x['by']
                            del x['claimed']
                            await ctx.send("deleted.")
                        else:
                            print("\n")
                    else:
                        print("\n")
            with open('data/claimed.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            await ctx.send("`:warning: Der Command ist noch nicht fertig! :warning:`")

    @commands.command()
    async def claim(self, ctx, user: Optional[discord.User]):
        claimed = False
        if user is None:
            await ctx.send("Bitte gib einen User an den du Claimen willst.")
            claimed = True
        if user.id is ctx.author.id:
            await ctx.send("das ist ziemlich traurig...")
            claimed = True
        elif user:
            with open('data/claimed.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['claimed'] == user.id:
                        await ctx.send("Dieser User wurde bereits geclaimed")
                        claimed = True
                    else:
                        print("\n")

                        
                        
            if claimed == False:
                embed = discord.Embed(title="Claim", description=f"{user.mention},{ctx.author.mention} versucht dich zu claimen.\nWenn du dies möchtest Reagiere mit <a:8783_AprovedAnimated:798499981262061580>", color=discord.Color.magenta())
                msg = await ctx.send(embed=embed)
                await msg.add_reaction('<a:8783_AprovedAnimated:798499981262061580>')


                def check(reaction, member):
                    return user == member and str(reaction.emoji) == '<a:8783_AprovedAnimated:798499981262061580>'
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                except asyncio.TimeoutError:
                    timeout = discord.Embed(title="Timeout!", description="Scheint so als bleibe jemand single.", color=discord.Color.red())
                    await ctx.send(embed = timeout)
                else:
                    claimed = discord.Embed(title="Claimed!!", description=f"{ctx.author.mention}, {user.mention} hat deine Anfrage angenommen!\nHerzlichen Glückwunsch!\nSiehe dir dein Profil mit `ng!profile` an.", color=discord.Color.green())
                    await ctx.send(embed = claimed)
                    with open('data/claimed.json') as json_file:
                        data = json.load(json_file)
                        claiming = {'claimed': user.id, 
                        'by': ctx.author.id}

                        data.append(claiming)
                    with open('data/claimed.json', 'w') as f:
                        json.dump(data, f, indent=4)
            else:
                return

def setup(bot):
    bot.add_cog(Fun(bot))