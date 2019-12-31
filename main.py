__version__ = "1.0.3"

import discord
from discord import utils, Client
from discord.ext import commands
from discord.utils import find
from cogs.utils import checks, perms
import logging
import random
import os
import typing
import json
import datetime
import aiohttp
import sqlite3
import sys
import traceback
import asyncio
import calendar
import time
from random import randrange

client = commands.Bot(
           command_prefix=commands.when_mentioned,
           description="SuperiorBot",
           owner_id=650890049558282272,
           case_insensitive=True
)
client.remove_command('help')
token = os.getenv("TOKEN")
		
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
	print("Superior Bot is launching")
	game = discord.Game("Launchin zzz..")
	await client.change_presence(status=discord.Status.idle, activity=game)
	print("Launched sucessfully" + client.user.display_name)
	game1 = discord.Game("@mention help")
	await client.change_presence(status=discord.Status.online, activity=game1)
		
@client.event
async def on_command_error(ctx, error):
	embed = discord.Embed(title=f"🤖 An error Occured", description=f"{error}", color=discord.Color.dark_magenta())
	await ctx.send(embed=embed)
	
@client.event
async def on_guild_join(guild):
    print(f"{guild} guild is now using me")
	
@client.command()
async def help(ctx):
	embed = discord.Embed(color=discord.Color.dark_teal(), timestap=datetime.datetime.utcnow(), description=f"Hey! {ctx.message.author} to view list of commands with defination visit the [website](http://www.devhubyt.xyz/Superior/commands.html)")
	embed.add_field(name="General Commands", value="*ping | avatar | userinfo | guildinfo | myinfo | invite | welcomer | embed | bitcoin | serverstats | joined | uptime | botinfo*", inline=True)
	embed.add_field(name="Mathematics Commands", value="*add | subtract | multiply | divide*", inline=True)
	embed.add_field(name="Fun Commands", value="*meme | slap | mentionme | dice | toss | reverse | meow | hug*", inline=True)
	embed.add_field(name="Action Commands", value="*ban | unban | kick | purge | mute | unmute | softban | nuke*", inline=True)
	embed.add_field(name="Image Fun Commands", value="*calling | captcha | challenge | achievement | facts | scroll*")
	embed.add_field(name="Text Fun Commands", value="*greentext | bluetext | echo | reverse | randomnum*")               
	await ctx.send(embed=embed)
	
@client.command()
async def invite(ctx):
    await ctx.send(f"https://discordapp.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
	
@client.command()
@commands.is_owner()
async def logout(ctx):
	print('Logged Out')
	async with ctx.typing():
		await ctx.send("Logged out successfully")
		await client.logout()
		print('Done')
		
@client.command()
@commands.is_owner()
async def connect(ctx):
	print("Connecting...")
	await client.connect(reconnect=True)
	print("Connected" + (len(client.guilds)))
	
@client.command()
@commands.is_owner()
async def stats(ctx):
	await ctx.send(f"Current commands: {len(client.commands)}, Guilds: {len(client.guilds)} and Used by {len(client.users)}")
	
@client.command()
async def ping(ctx):
	msg = f"My latency is {round(client.latency * 1000)}ms"
	embed = discord.Embed(title="Pong :ping_pong:", description=msg, color=discord.Color.green())
	await ctx.send(embed=embed)
	
@client.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at}'.format(member))
    
@client.command()
async def avatar(ctx):
	show_avatar = discord.Embed(
	
	         color = discord.Color.blue()
	)
	show_avatar.set_image(url="{}".format(ctx.author.avatar_url))
	await ctx.author.send(embed=show_avatar)
	
@client.command()
async def userinfo(ctx, member: discord.Member):
	roles = [role for role in member.roles]
	
	em = discord.Embed(title=f"Userinfo - {member.name}", color=discord.Color.blurple(), timestap=datetime.datetime.utcfromtimestamp(1553629094))
	em.set_thumbnail(url=f"{member.avatar_url}")
	em.add_field(name="ID:", value=member.id)
	em.add_field(name="Nickname:", value=member.display_name)
	
	em.add_field(name="Account Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	em.add_field(name="Joined the server at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	em.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
	em.add_field(name="Top Role", value=member.top_role.mention)
	em.add_field(name="Bot?", value=member.bot)
	
	await ctx.send(embed=em)
	
@client.command()
async def myinfo(ctx):
	roles = [role for role in ctx.author.roles]
	embed = discord.Embed(title=f"About {ctx.author}", color=discord.Color.blurple())
	embed.add_field(name="ID", value=f"{ctx.author.id}", inline=True)
	embed.add_field(name="Joined at", value=ctx.author.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	embed.add_field(name="Roles", value=" ".join([role.mention for role in roles]))
	embed.add_field(name="Top Role", value=ctx.author.top_role.mention)
	embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)
	
@client.command()
async def guildinfo(ctx):
	roles = [role for role in ctx.guild.roles]
	features = ctx.guild.features
	guild_age = (ctx.message.created_at - ctx.author.guild.created_at).days
	created_at = f"Server created on {ctx.author.guild.created_at.strftime('%b %d %Y at %H:%M')}. Guild age: {guild_age}"
	online = len({m.id for m in ctx.author.guild.members if m.status is not discord.Status.offline})
	em = discord.Embed(title=f"Guild Info - {ctx.guild.name}", description=created_at, color=discord.Color.blurple())
	em.set_thumbnail(url=ctx.author.guild.icon_url)
	em.set_author(name="Guild Info", icon_url=ctx.author.guild.icon_url)
	em.add_field(name="Id:", value=ctx.author.guild.id)
	em.add_field(name="Total Members:", value=len(ctx.author.guild.members))
	em.add_field(name="Owner:", value=ctx.guild.owner)
	em.add_field(name="Roles:", value=len(roles))
	em.add_field(name="Emojis:", value=len(ctx.guild.emojis))
	em.add_field(name="Region", value=ctx.guild.region)
	em.add_field(name="Verification level", value=ctx.guild.verification_level)
	em.add_field(name="Text Channels:", value=len(ctx.guild.text_channels))
	em.add_field(name="Voice Channels:", value=len(ctx.guild.voice_channels))
	em.add_field(name="Features", value=f"`{features}`")
	em.add_field(name="Server Boost Level", value=ctx.guild.premium_tier)
	await ctx.send(embed=em)
	
@client.command()
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name="<:bitcoin:661488080817094658> Bitcoin Current Price", value="$" + response['bpi']['USD']['rate'])
        await ctx.send(embed=embed)
        
@client.command()
async def meow(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get('http://aws.random.cat/meow') as r:
			if r.status == 200:
				js = await r.json()
				url = js['file']
				embed = discord.Embed(title="Here Come's", color=discord.Color.dark_green())
				embed.set_image(url=url)
				await ctx.send(embed=embed)
			
@client.command()
async def botinfo(ctx):
	platform = sys.platform
	guilds = len(client.guilds)
	embed = discord.Embed(color=discord.Color.dark_green(), description="If you like the bot, consider support us on [Patreon](https://patreon.com/devhubyt)")
	embed.set_thumbnail(url=client.user.avatar_url)
	embed.add_field(name="Library", value=f"discord.py - {discord.__version__}")
	embed.add_field(name="Commands Injected", value=len(client.commands))
	embed.add_field(name="Platform", value=platform)
	embed.add_field(name="Guilds", value=guilds)
	embed.add_field(name="Used by", value=f"{len(client.users)} users")
	await ctx.send(embed=embed)


@client.command()
async def mentionme(ctx):
	await ctx.send(ctx.author.mention + "Mentioned You")
	
@client.command()
async def serverstats(ctx):
	online = len([m.id for m in ctx.guild.members if m.status == discord.Status.online])
	offline = len([m.id for m in ctx.guild.members if m.status == discord.Status.offline])
	dnd = len([m.id for m in ctx.guild.members if m.status == discord.Status.do_not_disturb])
	idle = len([m.id for m in ctx.guild.members if m.status == discord.Status.idle])
	bots = 0
	members = 0
	total = 0
	for x in ctx.guild.members:
		if x.bot == True:
			bots += 1
			total += 1
		else:
			members += 1
			total += 1
	embed = discord.Embed(title=f"Server Stats - {ctx.guild.name}", color=discord.Color.blurple())
	embed.set_thumbnail(url=ctx.guild.icon_url)
	embed.add_field(name="Member stats", value=f"Online - {online}\nDND - {dnd}\nIdle - {idle}\nOffline - {offline}")
	embed.add_field(name="Server Count", value=f"Humans - {members}\nBot Count - {bots}\nTotal Count - {total}")
	await ctx.send(embed=embed)
	
@client.command()
async def dice(ctx):
	await ctx.send(f"{ctx.author.display_name}, you rolled **{randrange(1, 7)}**!")
	
@client.command()
async def toss(ctx):
	choice = random.randint(1,2)
	if choice == 1:
		await ctx.send("Heads")
	else:
		await ctx.send("Tails")
		
@client.command()
async def meme(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get("https://api.reddit.com/r/me_irl/random") as r:
			data = await r.json()
			url = data[0]["data"]["children"][0]["data"]["url"]
			embed = discord.Embed(title="Here Come's meme", color=discord.Color.dark_green())
			embed.set_image(url=url)
			await ctx.send(embed=embed)
	
@client.command()
async def slap(ctx, *, member: discord.Member = None):
	if member is None:
		embed = discord.Embed(color=discord.Color.dark_teal(), title="No One to slap 🙄", description="You have to mention any member to slap")
		embed.set_thumbnail(url="https://i.imgur.com/6YToyEF.png")
		await ctx.send(embed=embed)
	elif member.id == ctx.message.author.id:
		embed = discord.Embed(title="What You want to slap you 🤔", description="No I can't slap you because you are my friend", color=discord.Color.dark_green())
		embed.set_image(url="http://4.bp.blogspot.com/-FL6mKTZOk94/UBb_9EuAYNI/AAAAAAAAOco/JWsTlyInMeQ/s400/Jean+Reno.gif")
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Slapped", description=f"**{ctx.author} slapped {member}**", color=discord.Color.dark_red())
		embed.set_image(url="https://media0.giphy.com/media/l2YOqzhYD066fAd56/giphy.gif")
		await ctx.send(embed=embed)
		
@client.command()
async def hug(ctx, *, member: discord.Member = None):
	if member is None:
		await ctx.send(f"{ctx.message.author.mention} has been hugged 💝")
	elif member.id == ctx.message.author.id:
		await ctx.send(f"{ctx.message.author.mention} hugged themselves because they are singles 👬")
	else:
		await ctx.send(f"{member.mention} was hugged by {ctx.message.author.mention} 💝")
		
client.run(token)
