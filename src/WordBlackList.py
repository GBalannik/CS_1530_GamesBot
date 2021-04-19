import os
import discord
import random
from dotenv import load_dotenv

wordBL = set()

def build_dictionary():
	file = open("database/wordblacklist.txt", 'r')

	for line in file:
		line = line.strip()
		wordBL.add(line)

	file.close()


def add_or_remove_word(ctx, word):
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


def chide_user(user_id):
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


@client.command()
async def banword(ctx, word):
	if ctx.message.author.server_permissions.administrator:
		add_or_remove_word(ctx, word)
	else:
		await ctx.send("Only admins may edit the blacklist.")


@client.event
async def on_message(message):
    text = message.content
    text = text.translate(str.maketrans(table))
    author_id = message.author.id

    if author_id != 756276859225768057:
        isClean = True
        message_word_list = text.split()
        for word in message_word_list:
            if word in wordBL:
                isClean = False
                break
        if not isClean:
        	await message.author.ban()
            await message.channel.send(chide_user(author_id))