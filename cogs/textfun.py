import discord
import random
from discord.ext import commands

class TextFun(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		
	@commands.command()
	async def greentext(self, ctx, txt: str):
		msg = f"```yml\n{txt}\n```"
		await ctx.send(msg)
		
	@commands.command()
	async def reverse(self, ctx, *, text):
		text = "".join(reversed(str(text)))
		await ctx.send(text)
		
	@commands.command()
	async def bluetext(self, ctx, text: str):
		msg = f"```md\n{text}\n```"
		await ctx.send(msg)
		
	@commands.command()
	async def echo(self, ctx, *, text=None):
		if text == None:
			await ctx.send("No text given")
		else:
			await ctx.send(text)
			
	@commands.command()
	async def randomnum(self, ctx):
		num = random.randint(0, 6)
		await ctx.send(f"You got **{num}**")
		
def setup(client):
	client.add_cog(TextFun(client))