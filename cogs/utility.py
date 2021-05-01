import time
import platform
import re
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import asyncio
import os
import requests
import shutil
import random
from typing import Optional



class TimeParser:
    def __init__(self, argument):
        compiled = re.compile(r"(?:(?P<hours>[0-9]{1,5})h)?(?:(?P<minutes>[0-9]{1,5})m)?(?:(?P<seconds>[0-9]{1,5})s)?$")
        self.original = argument
        try:
            self.seconds = int(argument)
        except ValueError as e:
            match = compiled.match(argument)
            if match is None or not match.group(0):
                raise commands.BadArgument('Falsche Zeit angegeben, gültig sind z.B. `4h`, `3m` oder `2s`') from e

            self.seconds = 0
            hours = match.group('hours')
            if hours is not None:
                self.seconds += int(hours) * 3600
            minutes = match.group('minutes')
            if minutes is not None:
                self.seconds += int(minutes) * 60
            seconds = match.group('seconds')
            if seconds is not None:
                self.seconds += int(seconds)

        if self.seconds <= 0:
            raise commands.BadArgument('Zu wenig Zeit angegeben, gültig sind z.B. `4h`, `3m` oder `2s`')

        if self.seconds > 604800:  # 7 days
            raise commands.BadArgument('7 Tage sind eine lange Zeit, denkst du nicht auch?')

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @staticmethod
    def human_timedelta(dt):
        now = datetime.utcnow()
        delta = now - dt
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)

        if days:
            if hours:
                return '%s und %s' % (Plural(Tag=days), Plural(Stunde=hours))
            return Plural(day=days)

        if hours:
            if minutes:
                return '%s und %s' % (Plural(Stunde=hours), Plural(Minute=minutes))
            return Plural(hour=hours)

        if minutes:
            if seconds:
                return '%s und %s' % (Plural(Minute=minutes), Plural(Sekunde=seconds))
            return Plural(Minute=minutes)
        return Plural(Sekunde=seconds)


class Plural:
    def __init__(self, **attr):
        iterator = attr.items()
        self.name, self.value = next(iter(iterator))

    def __str__(self):
        v = self.value
        if v > 1:
            return '%s %sn' % (v, self.name)
        return '%s %s' % (v, self.name)

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles[::-1]:
            if not role.is_default():
                string += f'{role.mention}, '
        if string == '':
            return 'None'
        else:
            return string[:-2]

    @staticmethod
    def _getEmojis(emojis):
        string = ''
        for emoji in emojis:
            string += str(emoji)
        if string == '':
            return 'None'
        else:
            return string[:1000]  #The maximum allowed charcter amount for embed fields

    @commands.command(aliases=['pfp','profilepicture','profileimage'])
    async def avatar(self, ctx, member : Optional[discord.Member]):
        if not member:
            member = ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar!", color=discord.Color.green())
        embed.add_field(name='User', value=member.name)
        embed.add_field(name='Animiert?', value=member.is_avatar_animated())
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['archive'])
    @commands.cooldown(1, 60, commands.cooldowns.BucketType.channel)
    async def log(self, ctx, *limit: int):
        '''Archiviert den Log des derzeitigen Channels und läd diesen als Attachment hoch
        Beispiel:
        -----------
        :log 100
        '''
        if not limit:
            limit = 10
        else:
            limit = limit[0]
        logFile = f'{ctx.channel}.log'
        counter = 0
        with open(logFile, 'w', encoding='UTF-8') as f:
            f.write(f'Archivierte Nachrichten vom Channel: {ctx.channel} am {ctx.message.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n')
            async for message in ctx.channel.history(limit=limit, before=ctx.message):
                try:
                    attachment = '[Angehängte Datei: {}]'.format(message.attachments[0].url)
                except IndexError:
                    attachment = ''
                f.write('{} {!s:20s}: {} {}\r\n'.format(message.created_at.strftime('%d.%m.%Y %H:%M:%S'), message.author, message.clean_content, attachment))
                counter += 1
        msg = f':ok: {counter} Nachrichten wurden archiviert!'
        f = discord.File(logFile)
        await ctx.send(file=f, content=msg)
        os.remove(logFile)

    @log.error
    async def log_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await ctx.send(f':alarm_clock: Cooldown! Versuche es in {seconds} erneut') 

    @commands.command(aliases=['uptime', 'up', 'bi', 'botinfo'])
    async def status(self, ctx):
        '''Infos über den Bot'''
        timeUp = time.time() - self.bot.startTime
        hours = timeUp / 3600
        minutes = (timeUp / 60) % 60
        seconds = timeUp % 60
        admin = "<@178525733600100352>"
        botname = self.bot.user.name
        botid = self.bot.user.id
        stream = os.popen('vcgencmd measure_temp')
        gputemp = stream.read()
        stream = os.popen('iwconfig wlan0 | grep -i --color signal')
        signal = stream.read()
        signalquality = signal[23:-25]
        signallevel = signal[43:]

        users = 0
        channel = 0
        if len(self.bot.commands_used.items()):
            commandsChart = sorted(self.bot.commands_used.items(), key=lambda t: t[1], reverse=False)
            topCommand = commandsChart.pop()
            commandsInfo = '{} (Top: {})'.format(sum(self.bot.commands_used.values()), topCommand[0])
        else:
            commandsInfo = str(sum(self.bot.commands_used.values()))
        for guild in self.bot.guilds:
            users += len(guild.members)
            channel += len(guild.channels)

        embed = discord.Embed(color=discord.Colour.from_hsv(random.random(), 1, 1))
        embed.set_footer(text='Dieser Bot ist in der Entwicklung und hat noch viele bugs.\nFür eine Liste der Commands : ng!help')
        embed.set_thumbnail(url=ctx.me.avatar_url)
        embed.add_field(name='Dev', value=admin, inline=False)
        embed.add_field(name='Botname', value=botname, inline=True)
        embed.add_field(name='Botid', value=botid,inline=True)
        embed.add_field(name='Uptime', value='{0:.0f} Stunden, {1:.0f} Minuten und {2:.0f} Sekunden\n'.format(hours, minutes, seconds), inline=False)
        embed.add_field(name='Beobachtete Benutzer', value=users, inline=True)
        embed.add_field(name='Beobachtete Server', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='Beobachtete Channel', value=channel, inline=True)
        embed.add_field(name='Ausgeführte Commands', value=commandsInfo, inline=True)
        embed.add_field(name='Bot Version', value=self.bot.botVersion, inline=True)
        embed.add_field(name='Discord.py Version', value=discord.__version__, inline=True)
        embed.add_field(name='Python Version', value=platform.python_version(), inline=True)
        # embed.add_field(name='Speicher Auslastung', value=f'{round(memory_usage(-1)[0], 3)} MB', inline=True)
        embed.add_field(name='Betriebssystem', value=f'{platform.system()} {platform.release()}', inline=True)
        embed.add_field(name='CPU Temperatur', value=f'{gputemp[5:]}', inline=True)
        embed.add_field(name='Wlan Qualität', value=signalquality, inline=True)
        embed.add_field(name='Wlan Stärke', value=signallevel, inline=True)
        await ctx.send('**:information_source:** Informationen über diesen Bot:', embed=embed)

    @commands.command(aliases=['emotes'])
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def emojis(self, ctx):
        '''Gibt alle Emojis aus auf welche der Bot Zugriff hat'''
        msg = ''
        for emoji in self.bot.emojis:
            if len(msg) + len(str(emoji)) > 1000:
                await ctx.send(msg)
                msg = ''
            msg += str(emoji) + f" │ `{emoji}`\n"
        await ctx.send(msg)

    @commands.command(aliases=["bomb", "purge", "löschen", "lösch"])
    @commands.check_any(commands.has_permissions(manage_messages=True))
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=1)
        msg = await ctx.send("<a:7412_agooglebomb:798299231772606464>", delete_after=2.9)
        await asyncio.sleep(1.6)
        def check(m):
            return m != msg
        await ctx.channel.purge(limit=amount+1, check=check)

    @commands.command(aliases=['reminder','remind','time','erinnerung','wecker'])
    async def timer(self, ctx, time : TimeParser, *, message=''):
        '''Setzt einen Timer und benachrichtigt einen dann
        Beispiel:
        -----------
        :timer 13m Pizza
        :timer 2h Stream startet
        '''
        reminder = None
        completed = None
        message = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')

        if not message:
            reminder = '{0.name}, Ich stelle einen Timer auf {1}.'
            completed = '{0.name}! Dein Timer ist abgelaufen.'
        else:
            reminder = '{0.name}, Ich stelle einen Timer für `{2}` auf {1}.'
            completed = '{0.name}! Dein Timer für `{1}` ist abgelaufen.'

        human_time = datetime.utcnow() - timedelta(seconds=time.seconds)
        human_time = TimeParser.human_timedelta(human_time)
        #await ctx.send(reminder.format(ctx.author, human_time, message))
        setupembed = discord.Embed(title=f":clock1: Ok", description=reminder.format(ctx.author, human_time, message), color=discord.Color.magenta())
        setupmessage = await ctx.send(embed=setupembed)
        await asyncio.sleep(time.seconds)
        rememberembed = discord.Embed(title=f":alarm_clock: {completed.format(ctx.author, message, human_time)}", color=discord.Color.green())
        await ctx.reply(embed=rememberembed)
        await setupmessage.delete()


    @commands.command()
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def channels(self, ctx, serverid: int = None):
        """Shows ALL channels, use wisely!"""

        if serverid is None:
            server = ctx.guild
        else:
            server = discord.utils.get(self.bot.guilds, id=serverid)
            if server is None:
                return await ctx.send('Server not found!')

        e = discord.Embed()

        voice = ''
        text = ''
        categories = ''

        for channel in server.voice_channels:
            voice += f'\U0001f508 {channel}\n'
        for channel in server.categories:
            categories += f'\U0001f4da {channel}\n'
        for channel in server.text_channels:
            text += f'\U0001f4dd {channel}\n'

        if len(server.text_channels) > 0:
            e.add_field(name='Text Channels', value=f'```{text}```')
        if len(server.categories) > 0:
            e.add_field(name='Categories', value=f'```{categories}```')
        if len(server.voice_channels) > 0:
            e.add_field(name='Voice Channels', value=f'```{voice}```')

        try:
            await ctx.send(embed=e)
        except discord.HTTPException:
            em_list = await embedtobox.etb(e)
            for page in em_list:
                await ctx.send(page)

    @commands.command(aliases=['vote', 'addvotes', 'votes'])
    async def addvote(self, ctx, votecount = 'bool'):
        '''Fügt Emotes als Reactions hinzu für Abstimmungen/Umfragen'''
        if votecount.lower() == 'bool':
            emote_list = ['✅', '❌']
        elif votecount in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            #emotes = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            #for whatever reason, the above won't work
            emotes = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']
            emote_list = []
            for i in range (0, int(votecount)):
                emote_list.append(emotes[i])
        else:
            ctx.say(':x: Bitte gib eine Zahl zwischen 2 und 10 an')

        message = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        try:
            await ctx.message.delete()
        except:
            pass

        for emote in emote_list:
            await message[0].add_reaction(emote)

    @commands.Cog.listener()
    async def on_ready(self):
        print("utility.py working...")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id == 781976578413690880:
            await member.kick()
        else:
            return


def setup(bot):
    bot.add_cog(Utility(bot))