import discord
from discord.ext import commands
import random

# Colors are taken from discord.js lib

colors = {
    "DEFAULT": 0x000000,
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "GREY": 0x95A5A6,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_GREY": 0x979C9F,
    "DARKER_GREY": 0x7F8C8D,
    "LIGHT_GREY": 0xBCC0C0,
    "DARK_NAVY": 0x2C3E50,
    "BLURPLE": 0x7289DA,
    "GREYPLE": 0x99AAB5,
    "DARK_BUT_NOT_BLACK": 0x2C2F33,
    "NOT_QUITE_BLACK": 0x23272A,
}


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def embed(self, ctx):
        await ctx.send("What is the title of the Embed?")
        msg = await self.client.wait_for("message")
        title = msg.content

        await ctx.send("What would be the description of the embed?")
        msg = await self.client.wait_for("message")
        description = msg.content

        await ctx.send("What would be the author of the embed?")
        msg = await self.client.wait_for("message")
        author = msg.content

        await ctx.send("What would the thumbnail of the Embed?")
        msg = await self.client.wait_for("message")
        turl = msg.content

        msg = await ctx.send("Generating the embed...")

        clist = [c for c in colors.values()]

        embed = discord.Embed(
            title=title, description=description, color=random.choice(clist)
        )
        embed.set_thumbnail(url=turl)
        embed.set_author(name=author)

        await msg.edit(embed=embed, content=None)

        return


def setup(client):
    client.add_cog(Embed(client))
