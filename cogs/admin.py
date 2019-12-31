import discord
import asyncio
from discord.ext import commands

class Admin(commands.Cog):
	def __init__(self, client):
		self.client = client
		
	async def run_cmd(self, cmd: str) -> str: # add this right under the class
         process =\
         await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
         results = await process.communicate()
         return "".join(x.decode("utf-8") for x in results)
         
	@commands.command(hidden=True)
	@commands.is_owner() # double protection
	async def pull(self, ctx):
		if ctx.author.id == "650890049558282272":
			shell = await self.run_cmd('git pull Superior --no-commit --no-edit --ff-only master')
			shell = str(shell)
			embed = discord.Embed(description=shell)
			embed.set_author(name="Pulled from Git", icon_url="https://avatars0.githubusercontent.com/u/9919?s=280&v=4")
			await ctx.send(embed=embed)
		else:
			pass
	
	@commands.command()
	@commands.is_owner()
	async def load(self, ctx, extension):
		self.client.load_extension(f"cogs.{extension}")
		embed = discord.Embed(color=discord.Color.blurple())
		embed.add_field(name=":inbox_tray: `Input`", value=f"`Requested for loading cogs.{extension}`", inline=True)
		embed.add_field(name=":outbox_tray: `Output`", value=f"`Successfully loaded cogs.{extension}`", inline=True)
		await ctx.send(embed=embed)
	
	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, extension):
		self.client.unload_extension(f"cogs.{extension}")
		embed = discord.Embed(color=discord.Color.blurple())
		embed.add_field(name=":inbox_tray: `Input`", value=f"`Requested for unloading cogs.{extension}`", inline=True)
		embed.add_field(name=":outbox_tray: `Output`", value=f"`Successfully unloaded cogs.{extension}`", inline=True)
		await ctx.send(embed=embed)
		
	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, extension):
		self.client.unload_extension(f"cogs.{extension}")
		self.client.load_extension(f"cogs.{extension}")
		embed = discord.Embed(color=discord.Color.blurple())
		embed.add_field(name=":inbox_tray: `Input`", value=f"`Requested for re-loading cogs.{extension}`", inline=True)
		embed.add_field(name=":outbox_tray: `Output`", value=f"`Successfully re-loaded cogs.{extension}`", inline=True)
		await ctx.send(embed=embed)
					
def setup(client):
	client.add_cog(Admin(client))
