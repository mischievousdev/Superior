import discord
from discord.ext import commands

class ImageFun(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		
	@commands.command()
	async def calling(self, ctx, txt: str):
		embed = discord.Embed(title="calling", color=discord.Color.dark_green())
		embed.set_image(url=f"https://api.alexflipnote.dev/calling?text=hi")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def captcha(self, ctx, txt: str):
		embed = discord.Embed(title="captcha", color=discord.Color.dark_green())
		embed.set_image(url=f"https://api.alexflipnote.dev/captcha?text={txt}")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def challenge(self, ctx, txt: str):
		embed = discord.Embed(title="challenge", color=discord.Color.dark_green())
		embed.set_image(url=f"https://api.alexflipnote.dev/challenge?text={txt}")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def achievement(self, ctx, txt: str):
		embed = discord.Embed(title="achievement", color=discord.Color.dark_green())
		embed.set_image(url=f"https://api.alexflipnote.dev/achievement?text={txt}")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def facts(self, ctx, txt: str):
		embed = discord.Embed(title="facts", color=discord.Color.dark_green())
		embed.set_image(url=f"https://api.alexflipnote.dev/facts?text={txt}")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def scroll(self, ctx, txt: str):
		embed = discord.Embed(title="scroll", color=discord.Color.dark_green())
		embed.set_image(url=f"https://api.alexflipnote.dev/scroll?text={txt}")
		await ctx.send(embed=embed)
		
def setup(client):
	client.add_cog(ImageFun(client))