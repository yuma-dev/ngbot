import discord
from discord.ext import commands
from termcolor import colored

class errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("errorhandling.py working...")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e = None):
        print(colored(' \n                                                              --= ERROR : =--', 'red'))
        print(colored(f'{e}', attrs=['bold']))
        print(colored('                                                              ----= END =----\n ', 'red'))
        if isinstance(e,commands.MissingPermissions):
            embed = discord.Embed(title=f"<a:ngnoo:794406650210942977> ERROR!", description=f"Keine Berechtigung!\nWenn du denkst das dass ein Fehler ist melde dich bei einem Admin", color=discord.Colour.red())
            await ctx.send(embed=embed)
            await ctx.message.delete()
        elif isinstance(e,commands.CommandNotFound):
            if ctx.guild.id == 336642139381301249:
                return
            else:
                await ctx.message.add_reaction("<:1666_Question:798522297023463444>")

def setup(bot):
    bot.add_cog(errorhandler(bot))