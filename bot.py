#imports
import traceback, discord, asyncio, random, config, datetime, os, json, time, youtube_dl
from pathlib import Path
from discord.ext import tasks, commands
from discord import Member
from discord.voice_client import VoiceClient
from collections import Counter

###This file only loads all cogs(extensions) and does basic setups###

#define current version
__version__ = 'b1.6.2'

#makes "get_prefix" the prefix from the json file
def getprefix(bot, message):
    with open("data/prefixes.json","r") as f:
        prefixes = json.load(f)

    return commands.when_mentioned_or(*prefixes[str(message.guild.id)])(bot, message)


#sets bot as the definition and sets the prefix to get_prefix then loads the jishaku extension for debugging
bot = commands.Bot(case_insensitive=True, command_prefix = getprefix, help_command=None,intents = discord.Intents.all(), owner_id=178525733600100352)
bot.load_extension('jishaku')

#remove already imported help command to replace it with a custom one
bot.remove_command("help")

#a custom user check
def yuma_check(ctx):
    return ctx.message.author.id == 178525733600100352

#write guild id plus no channel for birthday in json
@bot.event
async def on_guild_join(guild):
    #set prefix to standard
    with open("data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    #standard prefix
    prefixes[str(guild.id)] = ["ng!","Ng!","nG!","NG!","ng?","Ng?","nG?","NG?","ng ","Ng ","nG ","NG ","ng","Ng","nG","NG","nicolaeguta!"]
    with open("data/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    #set birthdaychannel to None
    with open("data/birthdaychannel.json", "r") as f:
        birthdaychannel = json.load(f)
    birthdaychannel[str(guild.id)] = 'None'
    with open("data/birthdaychannel.json", "w") as f:
        json.dump(birthdaychannel, f, indent=4)

#on guild leave remove that guild from the list (birthdays and prefixes)
@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    with open("data/birthdaychannel.json", "r") as f:
        birthdaychannel = json.load(f)
    birthdaychannel.pop(str(guild.id))
    with open("data/birthdaychannel.json", "w") as f:
        json.dump(birthdaychannel, f, indent=4)

#status change loop (unnecessarily long and messy but no need to make a function for this atm)
async def status_task():
    while True:
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Gigolo"), status=discord.Status.online)
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="la mai du-te la"), status=discord.Status.do_not_disturb)
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Hai in Mercedes,hai in avion"), status=discord.Status.online)
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Fara tine sunt OK"), status=discord.Status.do_not_disturb)
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="De la 1 pana la 10"), status=discord.Status.online)
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Politia"), status=discord.Status.do_not_disturb)
        await asyncio.sleep(120)
        await bot.change_presence(activity=discord.Game(name=f"{__version__} | yumα#2402"), status=discord.Status.idle)
        await asyncio.sleep(120)

#command for simply sending the botinvite
@bot.command()
async def invite(ctx):
    e = discord.Embed(color=discord.Color.green()).add_field(name="**Invite**", value="https://discord.com/oauth2/authorize?client_id=784215168561184788&scope=bot&permissions=8")
    await ctx.send(embed=e)

#restart the bot
@bot.command()
@commands.check(yuma_check)
async def restart(ctx):
    e1 = discord.Embed(color=ctx.author.color).add_field(name="**Restarting!**", value="Im Restarting the Bot!\nWatch the Status...")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the restart..."), status=discord.Status.do_not_disturb)
    await ctx.send(embed=e1)
    await bot.logout()
    await asyncio.sleep(1)
    await bot.login()

#load cogs
@bot.command()
@commands.check(yuma_check)
async def load(ctx,cog=None):
    if not cog:
        embed = discord.Embed(
            title="Loading cogs...",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        )
        # No cog, means we reload all cogs
        async with ctx.typing():
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Loaded: `{ext}`",
                            value='`No errors!`',
                            inline=True
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to load: `{ext}`",
                            value=e,
                            inline=True
                        )
                    await asyncio.sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # reload the specific cog
        async with ctx.typing():
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                embed = discord.Embed(
                    title="Loading cog...",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                # if the file does not exist
                embed.add_field(
                    name=f"Failed to load: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    bot.load_extension(f"cogs.{ext[:-3]}")
                    embed = discord.Embed(
                        title="Loading cog...",
                        color=discord.Color.green(),
                        timestamp=ctx.message.created_at
                    )
                    embed.add_field(
                        name=f"Loaded: `{ext}`",
                        value='`No errors!`',
                        inline=False
                    )
                except Exception as e:
                    embed = discord.Embed(
                        title="Loading cog....",
                        color=discord.Color.red(),
                        timestamp=ctx.message.created_at
                    )
                    embed.add_field(
                        name=f"Failed to load: `{ext}`",
                        value=e,
                        inline=False
                    )
            await ctx.send(embed=embed)


#unload cog
@bot.command(name='unload')
@commands.check(yuma_check)
async def unload(ctx, cog=None):
    if not cog:
        embed = discord.Embed(
            title="Unloading cogs...",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at
        )
        # No cog, means we reload all cogs
        async with ctx.typing():
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        bot.unload_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Unloaded: `{ext}`",
                            value='`No errors!`',
                            inline=True
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to unload: `{ext}`",
                            value=e,
                            inline=True
                        )
                    await asyncio.sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # reload the specific cog
        async with ctx.typing():
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                # if the file does not exist
                embed = discord.Embed(
                    title="Unlading cog...",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                embed.add_field(
                    name=f"Failed to unload: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    embed = discord.Embed(
                        title="Unlading cog...",
                        color=discord.Color.green(),
                        timestamp=ctx.message.created_at
                    )
                    bot.unload_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Unloaded: `{ext}`",
                        value='`No errors!`',
                        inline=False
                    )
                except Exception as e:
                    embed = discord.Embed(
                        title="Unlading cog...",
                        color=discord.Color.red(),
                        timestamp=ctx.message.created_at
                    )
                    embed.add_field(
                        name=f"Failed to unload: `{ext}`",
                        value=e,
                        inline=False
                    )
            await ctx.send(embed=embed)


#reload cog
@bot.command(name='reload',aliases=["rl","re"])
@commands.check(yuma_check)
async def reload(ctx, cog=None):
    if not cog:
        # No cog, means we reload all cogs
        embed = discord.Embed(
            title="Relading cogs...",
            color=discord.Color.purple(),
            timestamp=ctx.message.created_at
        )
        async with ctx.typing():
            for ext in os.listdir("./cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        bot.unload_extension(f"cogs.{ext[:-3]}")
                        bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='`No errors!`',
                            inline=False
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=e,
                            inline=False
                        )
                    await asyncio.sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # reload the specific cog
        async with ctx.typing():
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                # if the file does not exist
                embed = discord.Embed(
                    title="Relading cog...",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                embed.add_field(
                    name=f"Failed to reload: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    embed = discord.Embed(
                        title="Relading cog...",
                        color=discord.Color.green(),
                        timestamp=ctx.message.created_at
                    )
                    bot.unload_extension(f"cogs.{ext[:-3]}")
                    bot.load_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Reloaded: `{ext}`",
                        value='`No errors!`',
                        inline=False
                    )
                except Exception as e:
                    embed = discord.Embed(
                        title="Relading cog...",
                        color=discord.Color.red(),
                        timestamp=ctx.message.created_at
                    )
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value=e,
                        inline=False
                    )

            await ctx.send(embed=embed)



#simply repeat what the user types
@bot.command(aliases=['repeat','send'])
async def say(ctx, *, args):
    await ctx.message.delete()
    await ctx.send(args)
#errorhandling for the say command
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="<a:ngnoo:794406650210942977> ERROR:", description="ng!say <satz>", color=discord.Color.red())
        await ctx.send(embed=embed)


#8ball command
@bot.command(aliases=["8ball"],  description="test")
async def _8Ball(ctx, *, question):
    responses = ["Mit Sicherheit.",
                 "Ja.",
                 "Ohne Zweifel!",
                 "Ja - definitiv.",
                 "Du kannst dich drauf verlassen.",
                 "Höchstwahrscheinlich.",
                 "Sieht gut aus.",
                 "die Zeichen deuten auf Ja.",
                 "Hai in mercedes,hai in avion",
                 "Frag später noch einmal.",
                 "Sag ich dir lieber nicht.",
                 "Kann ich nicht sagen.",
                 "Konzentrier dich und Frage nochmal.",
                 "Verlass dich nicht drauf.",
                 "Meine Antwort ist Nein.",
                 "Meine Quellen sagen Nein.",
                 "Sieht nicht gut aus.",
                 "Sehr Zweifelhaft"]
    embed = discord.Embed(title=question, description=f"**{random.choice(responses)}**", color=discord.Color.magenta())
    await ctx.send(embed=embed)
@_8Ball.error
async def achtball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="<a:ngnoo:794406650210942977> ERROR:", description="ng!8ball <frage>", color=discord.Color.red())
        await ctx.send(embed=embed)

###load all cogs in cog directory
for filename in os.listdir("./cogs"):
    try:
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename} initialized...")
    except Exception as e:
        print(f"{filename} caused this : {e}")
        
#triggers as soon as bot completely loaded
@bot.event
async def on_ready():
    await asyncio.sleep(0.2)
    users = 0
    channel = 0
    for guild in bot.guilds:
        users += len(guild.members)
        channel += len(guild.channels)
    bot.startTime = time.time()
    bot.commands_used = Counter()
    bot.botVersion = __version__
    await bot.change_presence(activity=discord.Game(name="STARTED!"), status=discord.Status.online)
    print(f'o--------------------------------------o\n     name : Nicolae Guta#5765\n     version : {__version__}\n     guilds : {len(bot.guilds)}\n     users : {users}\n     channels : {channel}\no--------------------------------------o')

#on command usage add to the commands_used counter
@bot.event
async def on_command(ctx):
    bot.commands_used[ctx.command.name] += 1
    msg = ctx.message

#start bot via the token in the config and starts status task
bot.loop.create_task(status_task())
bot.run(config.TOKEN)
