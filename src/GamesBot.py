#imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import random
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description="Games Group CS_1530 Discord Utility Bot", intents=intents)

@bot.event
async def on_ready():
	print("logged in")

@bot.command()
async def roll(ctx, dice: str):
	try:
		rolls, limit = map(int, dice.split('d'))
	except Exception:
		await ctx.send('Must be NdN')
		return

	result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
	await ctx.send(result)

@bot.command()
async def flip(ctx):
	flips = ['heads' , 'tails']
	await ctx.send(random.choice(flips))


bot.run(os.environ.get('token'))
