#imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import random
import os

load_dotenv()

#Default intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description="Games Group CS_1530 Discord Utility Bot", intents=intents)

@bot.event
async def on_ready():
	print("logged in")

@bot.event
async def on_message(self, message):
	return


#------------Commands Go Here-----------------

ongoingEvents = {}
cmdSettings = {}

# @author Discord.py API team
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

defaultEventErrorMessage = "Example of Server Event:\n !event time 1100\n emoji :watermelon\n"

@bot.group(pass_context=True, brief="This is where all commands are, !help event")
async def event(ctx, msg, time):
	if ctx.invoked_subcommand is None:
		await bot.say(defaultEventErrorMessage)	

@event.command(pass_context=True, brief="This is where all commands are, !help event")
async def emoji(ctx, emoji: str):
	await bot.say('Emoji set to {}'.format(emoji))
	if not ctx.message.author.id in cmdSettings:
		cmdSettings[ctx.message.author.id] ={}
	cmdSettings[ctx.message.author.id]['emoji'] = emoji

@event.command(pass_context=True, brief = "Time that the event starts")
async def time(ctx, time: int):
	if time > 0:
		await bot.say('Time set to {}'.format(time))
		if not ctx.message.author.id in cmdSettings:
			cmdSettings[ctx.message.author.id] = {}
		cmdSettings[ctx.message.author.id]['time'] = str(time)
	else:
		await bot.say("Error invalid time format")

@event.command(pass_context=True, brief="Message shown for event")
async def message(ctx, *args):
	arg = ' '.join(args)
	await bot.say('Message set to {}'.format(arg))
	if not ctx.message.author.id in cmdSettings:
			cmdSettings[ctx.message.author.id] = {}
	cmdSettings[ctx.message.author.id]['message'] = arg

@event.command(pass_context=True, brief="Channel event is in")
async def channel(ctx, arg: str):
	eventChannel = commands.ChannelConverter(ctx, arg).convert()
	if not ctx.message.author.id in cmdSettings:
			cmdSettings[ctx.message.author.id] = {}
	cmdSettings[ctx.message.author.id]['channel'] = eventChannel.id
	await bot.say('Channel set to {}'.format(eventChannel.name))

@event.command(pass_context=True, brief='All in one')
async def doAll(ctx, theEmoji: str, theTime: int, theChannel: str)
	await emoji.callback(ctx, theEmoji)
	await time.callback(ctx, theTime)
	await channel;.callback(ctx, theChannel)
	await start.callback(ctx)

@event.command(pass_context=True, brief='Start Event')
async def start(ctx)
	ready = True

	if not str(ctx.message.id) in cmdSettings:
		ready = False
		await bot.say('Not yet configured')

	else:
		if not e'emoji' in cmdSettings[ctx.message.author.id]:
			ready = False
			await bot.say("Error reaction not set")

		if not e'time' in cmdSettings[ctx.message.author.id]:
			ready = False
			await bot.say("Error time not set")

		if not e'channel' in cmdSettings[ctx.message.author.id]:
			ready = False
			await bot.say("Error channel not set")

	if ready:
		now = timeModule.time()
		endTime = now + int(cmdSettings[ctx.message.author.id])
		endDate = datetime.fromtimestamp(endTime)

		infomessage = "React to join event"
		if 'message' in cmdSettings[ctx.message.author.id]:
			infomessage = cmdSettings[ctx.message.author.id]['message']

		embed = await createEmbed(infomessage, cmdSettings[ctx.message.author.id]['emoji'], endDate, 'Event')\
		theMessage = await bot.send_message(cmdsettings[ctx.message.author.id]['channel'], None, embed=embed)



	

async def createEmbed(msg, emoji, time, title):
	embed = discord.Embed(color = 0x3fca1, title = title)
	info = "React with " + emoji + " on this message to be notified"

	embed.add_field(name = 'Creator Message', value = msg, inline = False)
	embed.add_field(name = 'Info', value = info, inline = False)
	embed.add_field(name = 'Event Time', value = time, inline = False)

	return embed

bot.run(os.environ.get('token'))
