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
	embed.add_field(name="Info commands", value="*userinfo(alias=ui) [member](member is optional) | serverinfo(salias=si) | emojiinfo | roleinfo | botinfo*")
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
	async with ctx.typing()
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
	msg = f"My latency is `{round(client.latency * 1000)}ms`"
	embed = discord.Embed(title="Pong!", description=msg, color=discord.Color.green())
	await ctx.send(embed=embed)
	
@client.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at}'.format(member))
	
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
async def mentionme(ctx):
	await ctx.send(ctx.author.mention + "Mentioned You")
	
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
