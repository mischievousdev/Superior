import discord
import sys
import os
import datetime
import psutil
from discord.ext import commands
from discord import Embed

class Info(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.process = psutil.Process(os.getpid())
		self.launch_time = datetime.datetime.utcnow()
		
	def get_uptime(self, *, brief=False):
		uptime = datetime.datetime.utcnow() - self.launch_time
		(hours, remainder) = divmod(int(uptime.total_seconds()), 3600)
		(minutes, seconds) = divmod(remainder, 60)
		(days, hours) = divmod(hours, 24)
		
		if not brief:
			if days:
				fmt = '{d} days, {h} hours, {m}minutes, {s} seconds'
			else:
				fmt = '{h} hours, {m} minutes, {s} seconds'
		else:
			fmt = '{h}h {m}m {s}s'
			if days:
				fmt = '{d}d' + fmt
				
		return fmt.format(d=days, h=hours, m=minutes, s=seconds)
		
	@commands.command(aliases=['av'])
	async def avatar(self, ctx, *, member: discord.Member=None):
		if not member:
			member = ctx.author
			
		url = member.avatar_url
		embed = Embed(color=member.top_role.color)
		embed.set_image(url=url)
		await ctx.send(embed=embed)
		
	@commands.command(aliases=['ui'])
	async def testui(self, ctx, *, member: discord.Member=None):
		if not member:
			member = ctx.author
		
		roles = [role for role in member.roles]
		perms = '|'.join(perm for perm, value in member.guild_permissions if value)
		embed = discord.Embed(color=member.top_role.color)
		embed.set_author(name=f"User Info - {member.display_name}", icon_url=member.avatar_url)
		embed.add_field(name="Id", value=f"`{member.id}`")
		embed.add_field(name="Account Created on", value=f'`{member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`')
		embed.add_field(name=f"{member.display_name} Joined the Guild on", value=f'`{member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`')
		embed.add_field(name="Bot?", value=f"`{member.bot}`")
		embed.add_field(name=f"Roles ({len(roles)})", value="".join([role.mention for role in roles]))
		embed.add_field(name=f"Top Roles", value=member.top_role.mention)
		embed.add_field(name="Permissions", value=f"`{perms}`")
		
		await ctx.send(embed=embed)
		
	@commands.command(aliases=["si"])
	async def serverinfo(self, ctx):
		online = len([m.id for m in ctx.guild.members if m.status == discord.Status.online])
		idle = len([m.id for m in ctx.guild.members if m.status == discord.Status.idle])
		dnd = len([m.id for m in ctx.guild.members if m.status == discord.Status.dnd])
		offline = len([m.id for m in ctx.guild.members if m.status == discord.Status.offline])
		bot = 0
		humans = 0
		total = 0
		for x in ctx.guild.members:
			if x.bot == True:
				bot += 1
				total += 1
			else:
				humans += 1
				total += 1
		roles = [role for role in ctx.guild.roles]
		boostlevel = ctx.guild.premium_tier
		embed = Embed(color=ctx.author.top_role.color, description=f"Server created on {ctx.author.guild.created_at.strftime('%b %d %Y at %H:%M')}")
		embed.set_author(name=f"Server Info - {ctx.guild}", icon_url=ctx.guild.icon_url)
		embed.add_field(name='\uFEFF', value=f"Humans - {humans}\nBots - {bot}\nTotal Count - {total}")
		embed.add_field(name="Guild Id", value=f"`{ctx.guild.id}`")
		embed.add_field(name="Guild Region", value=f"`{ctx.guild.region}`")
		embed.add_field(name="Guild Owner", value=f"`{ctx.guild.owner}`")
		embed.add_field(name="Text & Voice Channels", value=f"`Text Channels - {len(ctx.guild.text_channels)}\nVoice Channels - {len(ctx.guild.voice_channels)}`")
		embed.add_field(name="Roles & Emojis", value=f"`Roles Count - {len(roles)}\nEmojis Count - {len(ctx.guild.emojis)}`")
		embed.add_field(name="Members Status", value=f"<:online:661854185440018432> `Online - {online} members`\n<:idle:661854125033652224> `Idle - {idle} members`\n<:dnd:661854153227763722> `DND - {dnd} members`\n<:offline:661862443286265887> `Offline - {offline} members`")
		embed.add_field(name="Verification Level", value=f"`{ctx.guild.verification_level}`")
		embed.add_field(name="Server Boosting", value=f"`Boost Level - {ctx.guild.premium_tier}`")
		await ctx.send(embed=embed)
		
	@commands.command(aliases=["ei"])
	async def emojistats(self, ctx, emoji: discord.Emoji):
		embed = Embed(color=ctx.author.top_role.color, title=f"{emoji.name.title()} stats")
		embed.add_field(name="Emoji Id", value=f"`{emoji.id}`")
		embed.add_field(name="Emoji Created at", value=f'`{emoji.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`')
		embed.add_field(name="Animated ?", value=f"`{emoji.animated}`")
		embed.add_field(name="Available for use ?", value=f"`{emoji.available}`")
		embed.add_field(name="Guild that belongs to this emoj", value=f"{emoji.guild} `({emoji.guild_id})`")
		await ctx.send(embed=embed)
		
	"""@commands.command()
	@commands.is_owner()
	async def id(self, ctx, emoji: discord.Emoji): # this is just for fun
		await ctx.send(emoji.id)"""
		
	@commands.command(aliases=["ri"])
	async def roleinfo(self, ctx, role: discord.Role):
		embed = discord.Embed(color=role.color, title=f"{role.name} Stats")
		embed.add_field(name="Role Id", value=f"`{role.id}`")
		embed.add_field(name="Role Position", value=f"`{role.position}`")
		embed.add_field(name="Role Hoist", value=f"`{role.hoist}`")
		embed.add_field(name="Mentionable ?", value=f"`{role.mentionable}`")
		embed.add_field(name="Role Created at", value=f'`{role.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}`')
		await ctx.send(embed=embed)
		
	@commands.command(aliases=["bi"])
	async def botinfo(self, ctx):
		ramUsage = self.process.memory_full_info().rss / 1024**2
		uptime = self.get_uptime(brief=True)
		platform = sys.platform
		embed = discord.Embed(color=ctx.author.top_role.color, title=f"Information about {self.client.user.name}")
		embed.add_field(name="Bot Owner", value="`devhubyt#0597`")
		embed.add_field(name="Bot Librarary", value=f"`Discord.py-1.2.5`")
		embed.add_field(name="Bot is used by", value=f"`Users - {len(self.client.users)} users\nGuilds - {len(self.client.guilds)}`")
		embed.add_field(name="Ram Usage", value=f"`{ramUsage:.2f} MB`")
		embed.add_field(name="CPU Usage", value=f"`{psutil.cpu_percent()}% CPU`")
		embed.add_field(name="Uptime", value=f"`{uptime}`")
		embed.set_footer(text=f"Supeior Bot - v1.0.3 | Thanks {ctx.author.name}! for showing interest to know about me")
		await ctx.send(embed=embed)
	
def setup(client):
	client.add_cog(Info(client))
