from discord.ext import commands
import discord
import random
import datetime
import sqlite3


class Welcomer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(
            f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}"
        )
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild
            embed = discord.Embed(
                color=discord.Color.dark_green(),
                description=str(result1[0]).format(
                    members=members, mention=mention, user=user, guild=guild
                ),
                timestap=datetime.datetime.utcfromtimestamp(1553629094),
            )
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(
                text=f"{member.guild}", icon_url=f"{member.guild.icon_url}"
            )
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.client.get_channel(int(result[0]))
            await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcomer(self, ctx):
        await ctx.send(
            "**Available Setup Commands:** welcomer set_channel <#channel> & welcomer text <text>"
        )

    @welcomer.command()
    async def set_channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(
                f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}"
            )
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO main(guild_id, channel_id) VALUES(?, ?)"
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Welcome channel set to **{channel.mention}**")
            elif result is not None:
                sql = "UPDATE main SET channel_id = ? WHERE guild_id = ?"
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Welcome channel updated to **{channel.mention}**")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @welcomer.command()
    async def set_text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO main(guild_id, msg) VALUES(?, ?)"
                val = (ctx.guild.id, text)
                await ctx.send(f"Welcome message set to **{text}**")
            elif result is not None:
                sql = "UPDATE main SET msg = ? WHERE guild_id = ?"
                val = (text, ctx.guild.id)
                await ctx.send(f"Welcome message updated to **{text}**")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()


def setup(client):
    client.add_cog(Welcomer(client))
