import discord
from discord.ext import commands
from os import system
import asyncio
import time
import random


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #ping command
    @commands.command()
    async def ping(self, ctx):
        start = time.time()
        """Zeigt die latency vom Bot zum Discord Server an."""
        embed = discord.Embed(title="<a:ngloading:794671186314264586> loading..",color=discord.Color.light_grey())
        end = time.time()
        embed2 = discord.Embed(title="<a:ngyess:794406566107414569> Done!",color=discord.Color.green())
        error = discord.Embed(title="<a:ngnoo:794406650210942977> ERROR!", description="The latency failed!\nMaybe I had a Timeout?", color=discord.Color.red())
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(random.random())
        try:
            a = end - start
            a = a * 1000
            embed2.add_field(name="<:ngdpy:794423032289558538> │ websocket", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
            embed2.add_field(name="<a:ngtyping:794406403523084339> │ client", value=f"`{round(a,2)}ms`", inline=True)
            await msg.edit(embed=embed2)
        except Exception:
            await msg.edit(embed=error)

def setup(bot):
    bot.add_cog(ping(bot))
