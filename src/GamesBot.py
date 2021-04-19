#imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import random
import os
import asyncio
import time as timeModule
from datetime import datetime

load_dotenv()

#Default intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description="Games Group CS_1530 Discord Utility Bot", intents=intents)
wordBL = set()

@bot.event
async def on_ready():
	print("logged in")

@bot.event
async def on_message(message):
    text = message.content
    #text = text.translate(str.maketrans(table))
    author_id = message.author.id

    if author_id != bot.user.id:
        isClean = True
        message_word_list = text.split()
        for word in message_word_list:
            if word in wordBL:
                isClean = False
                break
        if not isClean:
       		await message.author.ban()
        	await message.channel.send(chide_user(author_id))

#------------Commands Go Here-----------------

ongoingEvents = {}
cmdSettings = {}

@bot.command()
async def banword(ctx, word):
	if ctx.message.author.server_permissions.administrator:
		add_or_remove_word(ctx, word)
	else:
		await ctx.send("Only admins may edit the blacklist.")


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

# adapted from @author AnimeHasFallen@github.com
@bot.group(pass_context=True, alisases=["E","e"], brief="This is where all commands are, !help event")
async def event(ctx):
	if ctx.invoked_subcommand is None:
		await ctx.send(defaultEventErrorMessage)	

@event.command(pass_context=True, brief="This is where all commands are, !help event")
async def emoji(ctx, emoji: str):
	await ctx.send('Emoji set to {}'.format(emoji))
	if not ctx.message.author.id in cmdSettings:
		cmdSettings[ctx.message.author.id] ={}
	cmdSettings[ctx.message.author.id]['emoji'] = emoji

@event.command(pass_context=True, brief = "Time that the event starts")
async def time(ctx, time: int):
	if time > 0:
		await ctx.send('Time set to {}'.format(time))
		if not ctx.message.author.id in cmdSettings:
			cmdSettings[ctx.message.author.id] = {}
		cmdSettings[ctx.message.author.id]['time'] = str(time)
	else:
		await ctx.send("Error invalid time format")

@event.command(pass_context=True, brief="Message shown for event")
async def message(ctx, *args):
	arg = ' '.join(args)
	await ctx.send('Message set to {}'.format(arg))
	if not ctx.message.author.id in cmdSettings:
			cmdSettings[ctx.message.author.id] = {}
	cmdSettings[ctx.message.author.id]['message'] = arg

#@event.command(pass_context=True, brief="Channel event is in")
#async def channel(ctx, arg: str):
#	eventChannel = commands.ChannelConverter(ctx, arg).convert()
#	if not ctx.message.author.id in cmdSettings:
#			cmdSettings[ctx.message.author.id] = {}
#	cmdSettings[ctx.message.author.id]['channel'] = eventChannel.id
#	await ctx.send('Channel set to {}'.format(eventChannel.name))

@event.command(pass_context=True, brief='All in one')
async def doAll(ctx, theEmoji: str, theTime: int):
	await emoji.callback(ctx, theEmoji)
	await time.callback(ctx, theTime)
#	await channel.callback(ctx, theChannel)
	await start.callback(ctx)

@event.command(pass_context=True, brief='Start Event')
async def start(ctx):
	ready = True

	if ctx.message.author.id in cmdSettings:

		if not 'emoji' in cmdSettings[ctx.message.author.id]:
			ready = False
			await ctx.send("Error reaction not set")

		if not 'time' in cmdSettings[ctx.message.author.id]:
			ready = False
			await ctx.send("Error time not set")

		#if not 'channel' in cmdSettings[ctx.message.author.id]:
		#	ready = False
		#	await ctx.send("Error channel not set")
	else:
		ready = False
		await ctx.send('Error: not yet configured')

	if ready:
		now = timeModule.time()
		endTime = now + int(cmdSettings[ctx.message.author.id]['time'])
		endDate = datetime.fromtimestamp(endTime)

		infomessage = "React to join event"
		if 'message' in cmdSettings[ctx.message.author.id]:
			infomessage = cmdSettings[ctx.message.author.id]['message']

		embed = await createEmbed(infomessage, cmdSettings[ctx.message.author.id]['emoji'], endDate, 'Event')
		theMessage = await ctx.send(None, embed=embed)

		ongoingEvents[theMessage.id] = {}
		ongoingEvents[theMessage.id]['emoji'] = cmdSettings[ctx.message.author.id]['emoji']
		ongoingEvents[theMessage.id]['message'] = infomessage
		ongoingEvents[theMessage.id]['endDate'] = endDate
		#ongoingEvents[theMessage.id]['channel'] = cmdsettings[ctx.message.author.id]['channel']
		#ongoingEvents[theMessage.id]['server'] = theMessage.server.id
		
		#ongoingEvents[theMessage.id]['task'] = bot.loop.create_task(reactionChecker(theMessage.id,theMessage.channel.id,theMessage.server.id,int(cmdsettings[ctx.message.author.id]['time'])))
		await theMessage.add_reaction(ongoingEvents[theMessage.id]['emoji'])
		#await reactionChecker(ctx, theMessage, int(cmdSettings[ctx.message.author.id]['time']))

		await asyncio.sleep(int(cmdSettings[ctx.message.author.id]['time']))

		#print(discord.utils.get(bot.cached_messages, id = theMessage.id).reactions)
		theReaction = discord.utils.get(bot.cached_messages, id = theMessage.id).reactions[0]

		async for user in theReaction.users():
			if user.id != bot.user.id:
				await dmUser(user)

		del ongoingEvents[theMessage.id]


async def dmUser(user):
	await user.send("Your event is starting")


async def createEmbed(msg, emoji, time, title):
	embed = discord.Embed(color = 0x3fca1, title = title)
	info = "React with " + emoji + " on this message to be notified"

	embed.add_field(name = 'Creator Message', value = msg, inline = False)
	embed.add_field(name = 'Info', value = info, inline = False)
	embed.add_field(name = 'Event Time', value = time, inline = False)

	return embed


async def build_wordBL():
	with open("database/wordblacklist.txt", 'r') as file:
		for line in file:
			line = line.strip()
			wordBL.add(line)


async def add_or_remove_word(ctx, word):
	if word in wordBL:
		wordBL.remove(word)
		file = open("database/wordblacklist.txt", 'w')
		for item in wordBL:
			file.write(item)
		file.close()
		await ctx.send("{} was removed from the blacklist.".format(word))
	else:
		wordBL.add(word)
		file = open("database/wordblacklist.txt", 'a')
		file.write(word)
		file.close()
		await ctx.send("{} was added to the blacklist.".format(word))


async def chide_user(user_id):
    user_id = '<@' + str(user_id) + '>'
    responses = [
        "You kiss your mother with that mouth, {}?",
        "That's some colorful language, {}.",
        "Come on now, {}. Did you really need to say that?",
        "{} - LANGUAGE!",
        "Hey now {}, watch your mouth.",
        "We don't use that kind of language here, {}."
    ]

    choice = random.choice(responses)
    choice = choice.format(user_id)

    return choice


bot.run(os.environ.get('token'))
