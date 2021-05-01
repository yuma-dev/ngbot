import discord
from discord.ext import commands
import json
import os
import asyncio
import random
from discord.ext.commands import has_role
from typing import Optional
from discord.utils import get
from collections import Counter
import logging
import datetime
import traceback

def yuma_check(ctx):
    return ctx.message.author.id == 178525733600100352

class Ehre(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ehre.py working...")

    async def get_ehre(self):
        with open("data/ehre.json","r") as f:
            users = json.load(f)

        return users

    async def open_account(self, user, ctx):
        users = await self.get_ehre()
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)]["ehre"] = 10
        await self.update_bank(user)
        with open("data/ehre.json","w") as f:
            json.dump(users,f)
        return True


    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if not message.guild:
                return
            if message.guild.get_role(787136980030455809) in message.author.roles:
                await message.add_reaction('\U0001f1f1')
            else:
                return
        except AttributeError:
            return

    @commands.group(invoke_without_command=True)
    async def ehre(self, ctx, member: Optional[discord.Member]):
        if member is None:
            member = ctx.author

        user = member
        users = await self.get_ehre()
        ehre_amt = users[str(user.id)]["ehre"]

        #send embed with user's ehre
        em = discord.Embed(title = f"`• {member.display_name}'s Ehre •`",color = discord.Color.red())
        em.add_field(name="\u200b", value="\u200b", inline=True)
        em.add_field(name = "\u200b",value = f"`Ehre : {ehre_amt}`",inline=True)
        em.add_field(name="\u200b", value="\u200b", inline=True)
        await ctx.send(embed = em)

        print(users[str(user.id)]["ehre"])

        #if user.id has "ehre" under 0, add trash role and change nickname
        if users[str(user.id)]["ehre"] < 0:
            role = get(member.guild.roles, name="trash")
            '''await bot.add_roles(user, role)'''
            await member.add_roles(role)
            try:
                await member.edit(nick=member.name + "(ehrenlos)")
            finally:
                print(f"updated an user to under 0")
                return

        #if user.id has "ehre" above or equal to 0, remove trash role and remove nickname change
        if users[str(user.id)]["ehre"] >= 0:
            role = get(member.guild.roles, name="trash")
            '''await bot.add_roles(user, role)'''
            await member.remove_roles(role)
            try:
                await member.edit(nick=member.name)
            finally:
                print(f"updated an user to above 0")
                return

    @ehre.command(aliases=['gib', 'geben', 'give', 'an', 'für'])
    async def pay(self,ctx,member:discord.Member,amount = None):
        await self.open_account(ctx.author,ctx)
        await self.open_account(member,ctx)

        '''if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("`ERROR: Bitte Nutzer angeben`")'''

        if amount == None:
            await ctx.send("`♦` `ERROR: Bitte gib eine Anzahl an!` `♦`")


        amount = int(amount)

        await self.update_bank(ctx.author,-1*amount,"ehre")
        await self.update_bank(member,+1*amount,"ehre")

        await ctx.send(f"`♦` Du hast **{member.name} {amount} Ehre** gegeben `♦`")

    @ehre.command()
    @has_role("💠│Family")
    async def add(self,ctx,member:discord.Member,amount = None):
        await self.open_account(ctx.author,ctx)
        await self.open_account(member,ctx)

        if member == None:
            await ctx.send("`♦` `ERROR: Bitte Nutzer angeben` `♦`")

        if amount == None:
            await ctx.send("`♦` `ERROR: Bitte gib eine Anzahl an!` `♦`")


        amount = int(amount)

        await self.update_bank(member,amount,"ehre")

        await ctx.send(f"`♦` **{member.name}** hat **{amount} Ehre** bekommen! `♦`")

    @add.error
    async def add_error(self,ctx,error):
        if isinstance(error, commands.errors.MissingRole):
            await ctx.send("`♦` `Aus Sicherheitsgründen dürfen nur 💠│Family member Ehre nehmen` `♦`")

    @ehre.command()
    @has_role("💠│Family")
    async def remove(self,ctx,member:discord.Member,amount = None):
        await self.open_account(ctx.author,ctx)
        await self.open_account(member,ctx)

        if member == None:
            await ctx.send("`♦` `ERROR: Bitte Nutzer angeben` `♦`")

        if amount == None:
            await ctx.send("`♦` `ERROR: Bitte gib eine Anzahl an!` `♦`")


        amount = int(amount)

        await self.update_bank(member,-1*amount,"ehre")

        await ctx.send(f"`♦` **{member}** wurde **{amount} Ehre** genommen! `♦`")

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            await ctx.send("`♦` `Aus Sicherheitsgründen dürfen nur 💠│Family member Ehre nehmen!` `♦`")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("`♦` `ERROR: Bitte gib einen Nutzer an!` `♦`")
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("`♦` `ERROR: Dieser Member wurde nicht gefunden!` `♦`")


    @pay.error
    async def error_pay(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send ("`♦` `ERROR: Wem möchtest du ehre geben und wie viel? <User> <Amount>` `♦`")

    async def update_bank(self, user, change = 0, mode = "ehre"):
        users = await self.get_ehre()

        users[str(user.id)][mode] += change

        with open("data/ehre.json","w") as f:
            json.dump(users,f)

        if users[str(user.id)]["ehre"] < 0:
            role = get(user.guild.roles, name="trash")
            '''await bot.add_roles(user, role)'''
            await user.add_roles(role)
            try:
                await user.edit(nick=user.name + "(ehrenlos)")
            finally:
                print(f"updated user to under 0")
                return

        if users[str(user.id)]["ehre"] >= 0:
            role = get(user.guild.roles, name="trash")
            '''await bot.add_roles(user, role)'''
            await user.remove_roles(role)
            try:
                await user.edit(nick=user.name)
            finally:
                print(f"updated user to above 0")
                return

    @commands.command()
    async def top(self,ctx,x = 10):
        users = await self.get_ehre()
        top = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["ehre"]
            top[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)

        em = discord.Embed(title = f"Top {x} Ehrenvolle Leute" , description = "Dies wird entschieden durch die Rohe anzahl an Ehre die ihr euch erarbeitet habt.",color = discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = top[amt]
            member = self.bot.get_user(id_)
            name = member.name
            em.add_field(name = f"{index}. {name}" , value = f"{amt}", inline = False)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Ehre(bot))