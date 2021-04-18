from discord.ext import commands
from dotenv import load_dotenv

#imports
import discord
import logging
import random
import os

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
	print("logged in")

@client.event
async def on_message(message):
	return;

client.run(os.environ.get('token'))
