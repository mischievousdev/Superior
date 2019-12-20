import dbl
import discord
import os
from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API to post server count"""

    def __init__(self, client):
        self.client = client
        self.token = os.getenv("API_KEY")
        self.dblpy = dbl.DBLClient(self.client, self.token, autopost=True)

    async def on_guild_post():
        print("Server count posted successfully")

def setup(client):
    client.add_cog(TopGG(client))
