from itertools import count
import discord
from discord.ext import commands
import random
import time
from datetime import datetime
import asyncio
import json
from typing import Optional
import requests
import sys,os
from discord.ext.commands.core import check


class CogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}

    @commands.Cog.listener("on_message_delete")
    async def update_cachedelete(self, message) -> None:

        self.snipes[message.channel.id] = (
                message.author,
                message.content
                )    





    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        try:
            if self.bot.user == message.author:
                return
            if message.channel.id == 832651207478214697:
                if not message.content.startswith("#"):
                    query = {'language':'de','message': message.content,'type': 'old'}
                    headers = {'x-api-key': '7D1hgBcVikVC'}
                    try:
                        session = requests.request('GET', f'https://api.pgamerx.com/v3/ai/response',params=query,headers=headers,timeout=10)
                    except requests.exceptions.ReadTimeout:
                        session = None
                    try:
                        if session is None:
                            response = 'Timed out while getting the response'
                        else:
                            response = session.json()[0]['message']
                    except:
                        response = 'JSON decode failed'
                    await message.reply(response)
                    session.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
    


    @commands.Cog.listener("on_message_edit")
    async def update_cacheedit(self, message, before) -> None:
        #if message.content.before == message.content.after:
            #return
        self.snipes[message.channel.id] = (
                message.author,
                message.content
                )    


    @commands.command()
    async def snipe(self, ctx) -> None:

        author, content= self.snipes[ctx.channel.id]
        embed = discord.Embed(description=content,color=discord.Color.purple(), timestamp=datetime.utcnow())
        embed.set_author(name=f'{author.name}#{author.discriminator}', icon_url=author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command(aliases=["typeracer"])
    async def tr(self, ctx, member : Optional[discord.Member]):
        if member:
            embed = discord.Embed(title=f"{ctx.author.name} fordert dich heraus!", description=f"{member.mention} **reagiere mit <a:1846_tik:798295949935247430> auf diese Nachricht**\num die Herausforderung anzunehmen.", color=discord.Colour.green())
            sentembed = await ctx.send(embed=embed)
            await sentembed.add_reaction('<a:1846_tik:798295949935247430>')
            try:
                def check(reaction, user):
                    return user == member and str(reaction.emoji) == '<a:1846_tik:798295949935247430>'
                reaction = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                if reaction:
                    await sentembed.delete()
                else:
                    return
            except asyncio.TimeoutError:
                TimeoutEmbed = discord.Embed(title="Das ist aber Peinlich!", description=f"**{member.name}** hat deine Herausforderung nicht angenommen...", color=discord.Colour.red())
                await sentembed.edit(embed=TimeoutEmbed)
                await sentembed.clear_reaction('<a:1846_tik:798295949935247430>')
                return
            textt = f":green_circle: {ctx.author.name} {member.name} START!!"
        else:
            textt = f":green_circle: {ctx.author.name} START!!"
        #random settings via json
        with open("data/typeracer.json", "r") as x:
            number = random.randrange(1,12)
            load = json.load(x)
            timer = load[f"{number}"]["timer"]
            filename = load[f"{number}"]["filename"]
            answer = load[f"{number}"]["answer"]
            words = len(answer.split())
        #send embed and then embed2,file
        embed = discord.Embed(title=f"<a:countdown:804405670224855104>")
        embed.add_field(name="Zeit", value=f"{timer}s", inline=True)
        embed.add_field(name="Wörter", value=f"{words}", inline=True)
        embed2 = discord.Embed(title=textt, color=discord.Color.dark_green())
        embed2.set_image(url=f"attachment://{filename}")
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2.8)
        await msg.delete()
        file = discord.File(f"texts/{filename}", filename=filename)
        msg2 = await ctx.send(file=file, embed=embed2)
        #start timer
        starttime = time.time()
        #set "guess"
        try:
            #wait for an message for TIMER
            def check(message):
                return message.channel == ctx.channel and message.author == ctx.author or member and message.guild == ctx.guild
            guess = await self.bot.wait_for('message', check=check , timeout=timer)

            #when somebody guessed it right
            if guess.content == answer:

                #edit embed
                embed3 = discord.Embed(title=f":white_circle: {guess.author.name} hat den das Rennen erfolgreich beendet!", color=discord.Color.from_rgb(255,254,255))
                embed3.set_image(url=f"attachment://{filename}")
                await msg2.edit(embed=embed3)

                #calculate time and wpm
                fintime = time.time()
                total = fintime - starttime
                wpmraw = total / 100
                wpm = words / wpmraw

                #send new embed
                embed = discord.Embed(title=":checkered_flag: Richtig!", color=discord.Color.green())
                embed.add_field(name="Gewinner", value=f"<@{guess.author.id}>", inline=False)
                embed.add_field(name="Zeit", value=f"{round(total,2)}s", inline=True)
                embed.add_field(name="Zeitlimit", value=f"{timer}s", inline=True)
                embed.add_field(name="Geschwindigkeit", value=f"{round(wpm,2)}wpm", inline=True)
                await ctx.send(embed=embed)


            #if none of the above match 
            else:
                #edit embed and react
                await guess.add_reaction("❌")
                embedfalse = discord.Embed(title=f":red_circle: das rennen ist vorbei!", color=discord.Color.red())
                embedfalse.set_image(url=f"attachment://{filename}")
                await msg2.edit(embed=embedfalse)

                #calculate time and wpm
                fintime = time.time()
                total = fintime - starttime
                wpmraw = total / 100
                wpm = len(guess.content.split()) / wpmraw

                #send new embed
                embed = discord.Embed(title="Falsch, das Rennen wurde gestoppt!",description="Versuch es nochmal!", color=discord.Color.red())
                embed.add_field(name="Dein Text", value=f"{guess.content}", inline=True)
                embed.add_field(name="Richtiger Text", value=f"{answer}", inline=True)
                embed.add_field(name="Deine Geschwindigkeit", value=f"{round(wpm,2)}wpm")
                await ctx.send(embed=embed)

                return


        #Timer runs out
        except asyncio.TimeoutError:
            embedtimeout = discord.Embed(title=f":red_circle: das rennen ist vorbei!", color=discord.Color.red())
            embedtimeout.set_image(url=f"attachment://{filename}")
            await msg2.edit(embed=embedtimeout)
            embed = discord.Embed(title="Du hast zu lange gebraucht!", color=discord.Color.red())
            await ctx.send(embed=embed)
            fintime = time.time()
            return

    @commands.command(aliases=["thessg","tg","raten","thessgame","thessisgame"])
    async def thessasgame(self, ctx):
        await ctx.send("Errate eine Zahl zwischen 1 und 100 : ")
        GameRunning = True
        Zahl = random.randrange(1,100)
        while GameRunning:
            try:
                def check(message):
                    return message.channel == ctx.channel and message.author == ctx.author
                Gobi = await self.bot.wait_for('message', check=check , timeout=60)
                
                Gobi = str(Gobi.content)

                try:

                    if int(Gobi) == Zahl:
                        await ctx.send("toll2 dieses geniale Spiel wurde von Thess gemacht die dabei ganz viel spaß hatta komplett jaja komplett wahr auf asdhejden fall du7 huren")
                        GameRunning = False

                    elif int(Gobi)>100:
                        await ctx.send("kannst du ned lesen?")

                    elif int(Gobi)>Zahl:
                        await ctx.send("Hurensohn falsch digga mach mal kleiner")

                    elif int(Gobi)<Zahl:
                        await ctx.send("auch falsch nochmal kek mach doch grösser")

                    else:
                        await ctx.send("hilfe")

                except:
                    await ctx.send("bist du dumm?")

            except TimeoutError:
                await ctx.send("Deine Zeit ist um, probiers nochmal!")
                GameRunning = False
            
def setup(bot):
    bot.add_cog(CogName(bot))
