import discord
from discord.ext import commands

import time, datetime
import os, asyncio
import collections

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=0xff9300)
            await destination.send(embed=emby)

class infoCog(commands.Cog):
    """Info and Help commands"""

    def __init__(self, bot):
        self.bot = bot

        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

        self.colour = 0xff9300
        self.footer = 'Bot developed by DevilJamJar#0001\nWith a lot of help from ♿nizcomix#7532'
        self.thumb = 'https://styles.redditmedia.com/t5_3el0q/styles/communityIcon_iag4ayvh1eq41.jpg'

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command()
    async def cogs(self, ctx):
        """Shows all of the bot's cogs"""
        cogs = []
        for cog in self.bot.cogs:
            cogs.append(
                f"`{cog}` • {self.bot.cogs[cog].__doc__}")  # adds cogs and their description to list. if the cog doesnt have a description it will return as "None"
        await ctx.send(embed=discord.Embed(colour=self.colour, title=f"All Cogs ({len(self.bot.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to know more about them!\nhttps://bit.ly/help-command-by-niztg" + "\n\n" + "\n".join(
                                               cogs)))  # joins each item in the list with a new line

    @commands.command()
    async def ping(self, ctx):
        """Displays latency and response time"""
        begin = time.perf_counter()
        embed = discord.Embed(colour=self.colour, description=f'```fix\nLATENCY: {round(self.bot.latency * 1000)}\n```')
        pong = await ctx.send(embed=embed)
        end = time.perf_counter()
        response = round((end - begin) * 1000)
        embed = discord.Embed(colour=self.colour, description=f'```fix\nLATENCY: {round(self.bot.latency * 1000)}ms\nRESPONSE TIME: {response}ms```')
        await pong.edit(embed=embed)

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """Displays invite link"""

        embed = discord.Embed(title='Invite me to your server! My default prefix is \'ow!\'',
                              url='https://discord.com/api/oauth2/authorize?client_id=720229743974285312&permissions=2113924179&scope=bot',
                              color=self.colour)
        await ctx.send(embed=embed)

    @commands.command(aliases=['src'])
    async def source(self, ctx, command:str=None):
        """Shows source code"""
        # Code used from Rapptz' R.Danny repository provided by the MIT License
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        # Copyright (c) 2015 Rapptz
        
        # Code used from niztg's CyberTron5000 GitHub Repository Provided by the MIT License
        # https://github.com/niztg/CyberTron5000/blob/master/CyberTron5000/cogs/meta.py#L95-L140
        # Copyright (c) 2020 niztg
        
        u = '\u200b'
        if not command:
            embed = discord.Embed(title='View my source code on GitHub!', url='https://github.com/DevilJamJar/DevilBot', colour=self.colour,\
                                  description=':scales: `License:` **[Apache-2.0](https://opensource.org/licenses/Apache-2.0)**')
            return await ctx.send(embed=embed)

        if command == 'help':
            embed = discord.Embed(title='View this command on GitHub!', url='https://github.com/DevilJamJar/DevilBot/blob/master/cogs/info.py#L10-L26', colour=self.colour,\
                                  description=':scales: `License:` **[Apache-2.0](https://opensource.org/licenses/Apache-2.0)**')
            return await ctx.send(embed=embed)

        try:
            src = f"```py\n{str(__import__('inspect').getsource(self.bot.get_command(command).callback)).replace('```', f'{u}')}```"
        except:
            return await ctx.send('Command not found!')
        if len(src) > 2000:
            cmd = self.bot.get_command(command)
            if not cmd:
                return await ctx.send("Command not found.")
            file = cmd.callback.__code__.co_filename
            location = os.path.relpath(file)
            try:
                total, fl = __import__('inspect').getsourcelines(cmd.callback)
            except:
                return await ctx.send('Command not found!')
            ll = fl + (len(total) - 1)
            url = f"https://github.com/DevilJamJar/DevilBot/blob/master/{location}#L{fl}-L{ll}"
            if not cmd.aliases:
                char = '\u200b'
            else:
                char = '/'
            embed = discord.Embed(color=self.colour,
                                  title=f"View this command on GitHub: {cmd.name}{char}{'/'.join(cmd.aliases)}",
                                  url=url)
            embed.description = ":scales: `License:` **[Apache-2.0](https://opensource.org/licenses/Apache-2.0)**"
            await ctx.send(embed=embed)

        else:
            await ctx.send(src)

    @commands.command(aliases=['server', 'guildinfo', 'guild', 'gi', 'si'])
    async def serverinfo(self, ctx):
        '''Get information about the server.'''

        statuses = collections.Counter([m.status for m in ctx.guild.members])

        embed = discord.Embed(colour=self.colour, title=f"{ctx.guild.name}")
        embed.description = ctx.guild.description if ctx.guild.description else None
        embed.add_field(name='**General:**',
                        value=f'Owner: **{ctx.guild.owner}**\n'
                              f'Created on: **{datetime.datetime.strftime(ctx.guild.created_at, "%A %d %B %Y at %H:%M")}**\n'
                              f'<:member:716339965771907099> **{ctx.guild.member_count}**\n'
                              f'<:online:726127263401246832> **{statuses[discord.Status.online]:,}**\n'
                              f'<:idle:726127192165187594> **{statuses[discord.Status.idle]:,}**\n'
                              f'<:dnd:726127192001478746> **{statuses[discord.Status.dnd]:,}**\n'
                              f'<:offline:726127263203983440> **{statuses[discord.Status.offline]:,}**\n'
                              f'<:nitro:731722710283190332> **Tier {ctx.guild.premium_tier}**\n'
                              f'Boosters: **{ctx.guild.premium_subscription_count}**\n'
                              f'Max File Size: **{round(ctx.guild.filesize_limit / 1048576)} MB**\n'
                              f'Bitrate: **{round(ctx.guild.bitrate_limit / 1000)} kbps**\n'
                              f'Max Emojis: **{ctx.guild.emoji_limit}**\n', inline=False)

        embed.add_field(name='**Channel Information:**',
                        value=f'`AFK timeout:` **{int(ctx.guild.afk_timeout / 60)}m**\n'
                              f'`AFK channel:` **{ctx.guild.afk_channel}**\n'
                              f'`Text channels:` **{len(ctx.guild.text_channels)}**\n'
                              f'`Voice channels:` **{len(ctx.guild.voice_channels)}**\n', inline = False)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_image(url=ctx.guild.banner_url)
        embed.set_footer(text=f'Guild ID: {ctx.guild.id}  |  Requested by: {ctx.author.name}#{ctx.author.discriminator}')

        return await ctx.send(embed=embed)

    @commands.command(aliases=['user', 'ui'])
    async def userinfo(self, ctx, *, member: discord.Member = None):
        '''Get information about a member.'''
        if member is None:
            member = ctx.author

        if len(member.activities) > 0:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    activity = 'Listening to `Spotify`'
                elif isinstance(activity, discord.Game):
                    activity = f'Playing `{activity.name}``'
                elif isinstance(activity, discord.Streaming):
                    activity = f'Streaming `{activity.name}`'
                else:
                    activity = '`None`'
        else:
            activity = '`None`'
        embed = discord.Embed(title=f"{member}", colour=self.colour)
        embed.add_field(name='**General:**',
                        value=f'Name: `{member}`\n'
                              f'Activity: {activity}\n'
                              f'Desktop Status: `{member.desktop_status}`\n'
                              f'Mobile Status: `{member.mobile_status}`\n'
                              f'Browser Status: `{member.web_status}`\n'
                              f'Created on: `{datetime.datetime.strftime(member.created_at, "%A %d %B %Y at %H:%M")}`', inline=False)

        embed.add_field(name='**Guild related information:**',
                        value=f'Joined guild: `{datetime.datetime.strftime(member.joined_at, "%A %d %B %Y at %H:%M")}`\n'
                              f'Nickname: `{member.nick}`\n'
                              f'Top role: {member.top_role.mention}', inline=False)

        embed.set_thumbnail(url=member.avatar_url_as(static_format='png'))
        embed.set_footer(text=f'Member ID: {member.id}  |  Requested by: {ctx.author.name}#{ctx.author.discriminator}')

        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(infoCog(bot))
