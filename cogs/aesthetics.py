import datetime
import re
import statistics
import random
import sqlite3
import markovify
import string
import discord
import aiohttp

from collections import Counter
from io import BytesIO
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


smallcaps_alphabet = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ1234567890"

uppercase_fraktur = "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"
lowercase_fraktur = "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷1234567890"

uppercase_boldfraktur = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
lowercase_boldfraktur = "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟1234567890"


double_uppercase = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"

double_lowercase = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"

bold_fancy_lowercase = "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃1234567890"
bold_fancy_uppercase = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"

fancy_lowercase = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
fancy_uppercase ="𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"



alphabet = dict(zip("abcdefghijklmnopqrstuvwxyz1234567890", range(0, 36)))
uppercase_alphabet = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(0, 26)))
punctuation = dict(
    zip("§½!\"#¤%&/()=?`´@£$€{[]}\\^¨~'*<>|,.-_:", range(0, 37)))
space = " "
aesthetic_space = '\u3000'
aesthetic_punctuation = "§½！\"＃¤％＆／（）＝？`´＠£＄€｛［］｝＼＾¨~＇＊＜＞|，．－＿："
aesthetic_lowercase = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ１２３４５６７８９０"
aesthetic_uppercase = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"


def clean_string(string):
    string = re.sub('@', '@\u200b', string)
    string = re.sub('#', '#\u200b', string)
    return string

def aesthetics(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += aesthetic_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += aesthetic_uppercase[uppercase_alphabet[letter]]
            elif letter in punctuation:
                returnthis += aesthetic_punctuation[punctuation[letter]]
            elif letter == space:
                returnthis += aesthetic_space
            else:
                returnthis += letter
    return returnthis

def double_font(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += double_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += double_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis

def fraktur(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += lowercase_fraktur[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += uppercase_fraktur[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis

def bold_fraktur(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += lowercase_boldfraktur[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += uppercase_boldfraktur[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis

def fancy(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += fancy_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += fancy_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis

def bold_fancy(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += bold_fancy_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += bold_fancy_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis

def smallcaps(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += smallcaps_alphabet[alphabet[letter]]
            else:
                returnthis += letter
    return returnthis

class Aesthetic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()


    @commands.Cog.listener()
    async def on_ready(self):
        print("aesthetic.py working...")

    @commands.command(name='aesthetics', aliases=['ae'])
    async def _aesthetics(self, ctx, *, sentence: str):
        embed = discord.Embed(title="aesthetics", description=aesthetics(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)

    @commands.command(name='fraktur')
    async def _fraktur(self, ctx, *, sentence: str):
        embed = discord.Embed(title="fraktur", description=fraktur(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)

    @commands.command(name='boldfraktur', aliases=['boldfaktur', 'bf'])
    async def _boldfraktur(self, ctx, *, sentence: str):
        embed = discord.Embed(title="boldfraktur", description=bold_fraktur(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)

    @commands.command(name='fancy', aliases=['ff'])
    async def _fancy(self, ctx, *, sentence: str):
        embed = discord.Embed(title="fancy", description=fancy(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)

    @commands.command(name='boldfancy', aliases=['bff'])
    async def _bold_fancy(self, ctx, *, sentence: str):
        embed = discord.Embed(title="boldfancy", description=bold_fancy(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)

    @commands.command(name='double', aliases=['ds', 'doublestruck'])
    async def _doublestruck(self, ctx, *, sentence: str):
        embed = discord.Embed(title="doublestruck", description=double_font(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)

    @commands.command(name='smallcaps', aliases=['sc'])
    async def _smallcaps(self, ctx, *, sentence: str):
        embed = discord.Embed(title="smallcaps", description=smallcaps(sentence), color=discord.Color.magenta())
        await ctx.send(embed = embed)


    @commands.command(hidden=True)
    async def aesthetictest(self, ctx):
        await ctx.message.add_reaction('\u2705')


def setup(bot):
    bot.add_cog(Aesthetic(bot))