import discord
from discord.ext import commands
import json
from typing import Optional, Union

from discord.ext.commands.errors import CommandInvokeError


class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, payload):
        with open('data/votechannels.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['channel'] == payload.channel.id:
                    await payload.add_reaction('✅')
                    await payload.add_reaction('❌')
                else:
                    return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            pass

        else:
            with open('data/reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == str(payload.emoji.name):
                        if x['message_id'] == payload.message_id:
                            role = discord.utils.get(self.bot.get_guild(
                                payload.guild_id).roles, id=x['role_id'])

                            await payload.member.add_roles(role)

                            if x['text'] != "ZERO":
                                user = self.bot.get_user(payload.user_id)
                                await user.send(x['text'])
                            else:
                                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        with open('data/reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == str(payload.emoji.name):
                    if x['message_id'] == payload.message_id:
                        role = discord.utils.get(self.bot.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                        
                        await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


    @commands.command(aliases=["arr"])
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def addreactionrole(self, ctx, msg: Optional[discord.Message] , emoji: Union[discord.Emoji, discord.PartialEmoji, str], role: discord.Role, *, text: Optional[str]):
        if msg == None:
            msg = await ctx.channel.history(limit=1, before=ctx.message).flatten()
            msg = msg[0]

        await msg.add_reaction(emoji)

        if text == None:
            text = "ZERO"

        with open('data/reactrole.json') as json_file:
            data = json.load(json_file)

            try:
                new_react_role = {'role_name': role.name, 
                'role_id': role.id,
                'emoji': emoji.name,
                'message_id': msg.id,
                'text': text}
            except AttributeError:
                new_react_role = {'role_name': role.name, 
                'role_id': role.id,
                'emoji': emoji,
                'message_id': msg.id,
                'text': text}

            data.append(new_react_role)

        with open('data/reactrole.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.channel.purge(limit=1)

    @commands.command(aliases=["avc"])
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def addvotechannel(self, ctx):
        channel = ctx.channel
        with open('data/votechannels.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['channel'] == channel.id:
                    return
                else:
                    with open('data/votechannels.json') as json_file:
                        data = json.load(json_file)

                        new_vote_channel = {'channel': channel.id}

                        data.append(new_vote_channel)

                    with open('data/votechannels.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    await ctx.send(f"Ich habe {channel} zu den Vote-Channels hinzugefügt.\nAlle Nachrichten die in diesem Channel kommen werden bewertet werden können.")

def setup(bot):
    bot.add_cog(ReactionRole(bot))
