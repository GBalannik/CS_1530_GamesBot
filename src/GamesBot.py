from discord.ext import commands
from dotenv import load_dotenv

#imports
import discord
import logging
import random
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description="Games Group CS_1530 Discord Utility Bot", intents=intents)

client = discord.Client()

@bot.event
async def on_ready():
	print("logged in")

@bot.command
async def roll(ctx, dice: str):
	try:
		rolls, limit = map(int, dice.split('d'))
	except Exception:
		await ctx.send('Must be NdN')
		return



bot.run(os.environ.get('token'))
