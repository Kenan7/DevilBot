import discord
from discord.ext import commands
import secrets
from asyncdagpi import Client
from asyncdagpi import exceptions
import asyncio, aiohttp
from discord.ext.commands.cooldowns import BucketType

API_CLIENT = Client(secrets.secrets_dagpi_token)

class dagpiCog(commands.Cog):
    """Commands that utilise Daggy's API (dagpi.tk)"""

    def __init__(self, bot):
        self.bot = bot
        self.db_conn = bot.db_conn
        self.colour = 0xff9300
        self.footer = 'Bot developed by DevilJamJar#0001\nWith a lot of help from ♿nizcomix#7532'
        self.thumb = 'https://styles.redditmedia.com/t5_3el0q/styles/communityIcon_iag4ayvh1eq41.jpg'

    @commands.command(aliases=['whosthatpokemon'])
    async def wtp(self, ctx):
        """Who's that pokemon!"""
        data = {'token': secrets.secrets_dagpi_token}
        url = 'https://dagpi.tk/api/wtp'
        async with aiohttp.ClientSession(headers=data) as cs, ctx.typing():
            async with cs.get(url) as r:
                data = await r.json()
        qimg = data['question_image']
        aimg = data['answer_image']
        name = data['pokemon']['name']
        embed = discord.Embed(
            title='Who\'s That Pokemon!',
            colour = self.colour 
        )
        embed.set_image(url = qimg)
        question = await ctx.send(embed=embed)
        def check(message : discord.Message) -> bool:
            return message.author == ctx.author and message.content.lower() == name.lower()
        try:
            await self.bot.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! It was {name}.")
            embed = discord.Embed(
                title=f'Time\'s Up! It was {name}.',
                colour = self.colour
            )
            embed.set_image(url=aimg)
            return await question.edit(embed=embed)
        else:
            await ctx.send(f'Correct! It was {name}.')
            embed = discord.Embed(
                title=f'Correct! It was {name}.',
                colour = self.colour
            )
            embed.set_image(url=aimg)
            return await question.edit(embed=embed)

    @commands.command()
    async def hitler(self, ctx, *, image_url=None):
        try:
            image_url = int(image_url)
            try:
                a = self.bot.get_user(image_url)
                image_url = str(a.avatar_url)
            except:
                raise commands.BadArgument('Unknown User')
        except:
            if not image_url:
                image_url = str(ctx.author.avatar_url)
        try:
            response = await API_CLIENT.staticimage('hitler',image_url)
            await ctx.send(response)
        except Exception as e:
            raise commands.BadArgument(str(e))

def setup(bot):
    bot.add_cog(dagpiCog(bot))
