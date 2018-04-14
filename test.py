import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

import platform
import json
import datetime
import random
import validators
import argparse
import time

from ytsearch import youtube_search

from apiclient.discovery import build
from apiclient.errors import HttpError

def timing_function(function):

	async def wrapper():
		t1 = time.time()
		function()
		t2 = time.time()
		print(str(t2 - t1) + ' Seconds')

	return wrapper

def logger_function(function):
	
	@timing_function
	async def log():

		try:

			print('Runing function: {}'.format(function))
			function()

		except Exception as e:
			
			print('An error was encountered while running: {}'.format(function))
			print(e)

	return log

#Bot's class
class Bot(commands.Bot):
	def __init__(self, *args, **kwargs):

		def prefix_manager(bot, message):
			"""
			Returns prefixes of the message's server if set.
			If none are set or if the message's server is None
			it will return the global prefixes instead.

			Requires a Bot instance and a Message object to be
			passed as arguments.
			"""
			return bot.settings.get_prefixes(message.server)

		self.uptime = datetime.datetime.utcnow()  # Refreshed before login
		self.player = None 
		self.queue = []

		super().__init__(*args, **kwargs)

#Function for initializing the bot with a private JSON.
def run(bot):

	with open('botinfo.json') as info_file: 

		data = json.load(info_file)

	bot.run(data['bot'][0]['token'])

def screen():
	pass

#Function that deletes messages.
async def delete_message(bot, *args):
	
	for msg in args:

		await bot.delete_message(msg)

#Function for playing the requested YouTube URL.
async def play_youtube(bot, ctx, search):

	if (validators.url(search)):

		try:

			voice = None

			for x in bot.voice_clients:

				if(x.server == ctx.message.server):

					voice = x
			
			if (voice is None):
				voice = await bot.join_voice_channel(discord.Object(id = str(get_user_voice_channel(ctx.message.author))))

			bot.player = await voice.create_ytdl_player(search)
			bot.player.start()

			await bot.say('Playing {} by {} from YouTube...'.format(bot.player.title, bot.player.uploader))

		except Exception as e:
			
			print(e)
			await bot.say('There was an error while trying to play the requested song...')

	else:

		argparser = argparse.ArgumentParser()
		argparser.add_argument("--q", help="Search term", default=search)
		argparser.add_argument("--max-results", help="Max results", default=6)
		args = argparser.parse_args()

		search = []
		error = False

		try:
			search = youtube_search(args)

		except HttpError as e:

			print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
			error = True

		if (not error):

			await bot.say('I have found the following videos from YouTube:')
			
			for video in range(0, len(search) - 1):
				
				await bot.say('{}. {}'.format(video, search[video][0]))

			def check(msg):

				if (msg.content in ['0', '1', '2', '3', '4']):
					return True
				else:
					return False

			message = await bot.wait_for_message(author=ctx.message.author, check=check)

			try:

				voice = None

				for x in bot.voice_clients:

					if(x.server == ctx.message.server):

						voice = x
				
				if (voice is None):
					voice = await bot.join_voice_channel(discord.Object(id = str(get_user_voice_channel(ctx.message.author))))

				bot.player = await voice.create_ytdl_player('https://www.youtube.com/watch?v={}'.format(str(search[int(message.content)][1])))
				bot.player.start()

				await bot.say('Playing {} by {} from YouTube...'.format(bot.player.title, bot.player.uploader))

			except Exception as e:
				
				print(e)
				await bot.say('There was an error while trying to play the requested song...')

#Function that returns an user's voice channel if connected.
def get_user_voice_channel(user):
	
	try:
		
		channel = user.voice.voice_channel.id

	except Exception as e:
		
		channel = '375763075783196687'

	return channel

#Function that checks the existance of the -d modifier.
def check_deletion(arg):

	if (arg == '-d' or arg == '-D') : return True

	return False

#Main function.
def main(bot_class = Bot):

	bot = bot_class(description="DxD's custom BOT, use (/) for commands", command_prefix="/", pm_help = True)

	@bot.event
	async def on_ready():

		print("--- ⱭxD server's BOT ---\n")
		print('------------------------\n')
		print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()) + '\n')
		print('------------------------\n')
		print('Use link below to invite de BOT to the server...')
		print('https://discordapp.com/oauth2/authorize?bot_id={}&scope=bot&permissions=8'.format(bot.user.id) + '\n')
		print('------------------------\n')
		print('Created with <3 by https://github.com/profran with help of https://github.com/Habchy/BasicBot/wiki\n')

		await bot.change_presence(game=discord.Game(name='Python'))

	@bot.event
	async def on_member_update(*args):

		msg_options = (', Say hi to him/her!', ', Hope he/she brought pizza', "...I'm sure he wants to play Payday", ' Greetings from the command line! ;)')

		if (str(args[1].status) != 'offline' and str(args[0].status) == 'offline'):
			
			await bot.send_message(discord.Object('375763075783196684'), "<@{}> is {}{}".format(str(args[1].id), str(args[1].status), random.choice(msg_options)))
	'''
	@bot.event
	async def on_message(message):

		nsfw = ('bitch', 'dick', 'cock', 'slut', 'vagina', 'porn', 'penis', 'pussy', 'succ', 'felatio', 'pene', 'pija', 'concha')

		for x in message.content.split():

			if x in nsfw:

				await bot.send_message(discord.Object('375763075783196684'), '<@{}> This is not an NSFW Channel, please calm down...'.format(message.author.id))
	'''
	@bot.command(pass_context = True)
	async def ping(ctx):

		#now = datetime.datetime.utcnow()
		#now = (now.days * 86400000) + (now.seconds * 1000) + (now.microseconds / 1000)
		msg = ctx.message.timestamp
		msg = (msg.days * 86400000) + (msg.seconds * 1000) + (msg.microseconds / 1000) - now
		await bot.say('{}ms ;)'.format(msg))

	@bot.command()
	async def test(*args):

		await bot.say("Working fine...")

	@bot.command()
	async def summon(*args):

		try:
			await bot.join_voice_channel(discord.Object(id='375763075783196687'))

		except Exception as e:

			print(e)

	@bot.command(pass_context = True)
	async def leave(ctx):
		
		for x in bot.voice_clients:

			if(x.server == ctx.message.server):

				return await x.disconnect()

	@bot.command(pass_context = True)
	async def play(ctx, *args):

		if (check_deletion(args[0])):

			await delete_message(bot, ctx.message)

			await play_youtube(bot, ctx, ' '.join(args[1:]))

			#await bot.say('Playing {} by {} from YouTube...'.format(bot.player.title, bot.player.uploader))

		else: 

			await play_youtube(bot, ctx, ' '.join(args[0:]))

		#attrs = vars(voice)
		# {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
		# now dump this in some way or another
		#print(', '.join("%s: %s" % item for item in attrs.items()))
		
		#print(attrs)
		#dir(voice)

	@bot.command(pass_context = True)
	async def pause(ctx, *args):

		try:

			bot.player.pause()

		except Exception as e:

			print(e)
			await bot.say('There was an error while trying to pause the requested song...(No song?)')

	@bot.command()
	async def resume(*args):

		try:

			bot.player.resume()
			await bot.say('Resuming...')

		except Exception as e:

			print(e)
			await bot.say('There was an error while trying to resume the requested song...(No song?)')

	@bot.command()
	async def stop(*args):

		try:

			bot.player.stop()

		except Exception as e:

			print(e)
			await bot.say('There was an error while trying to stop the requested song...(No song?)')

	@bot.command()
	async def volume(*args):
		
		try:

			bot.player.volume = float(float(int(args[0])) / float(100))

		except Exception as e:

			print(e)
			await bot.say('There was an error while trying to set volume...(No song?)')

	@bot.command(pass_context = True)
	@logger_function
	async def say(ctx, *args):

		if (check_deletion(args[0])):

			await delete_message(bot, ctx.message)

			await bot.say(' '.join(args[1:]))

		else:
			
			await bot.say(' '.join(args))
	
	@bot.command(pass_context = True)
	async def sayd(ctx, *args):

		await bot.delete_message(ctx.message)			
		await bot.say(' '.join(args))

	@bot.command(pass_context = True)
	async def status(ctx, *args):

		if (ctx.message.author.id == '367823768153882635'):

			await bot.change_presence(game = discord.Game(name = (' '.join(args))))
			print('Status changed to {}'.format(' '.join(args)))

		else:

			await bot.say("<@{}> you don't have enough permissions to do that...".format(ctx.message.author.id))

	@bot.command(pass_context = True)
	async def clean(ctx, *args):

		async for msg in bot.logs_from(ctx.message.channel, limit = 100):

			if (msg.author.id == bot.user.id):

				await bot.delete_message(msg)

		await bot.say(':thumbsup: Succesfully cleaned all my messages...')

	@bot.command()
	async def secure(*args):

		await bot.say('⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n⠀⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n⠀⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n⠀⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n⠀⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n ⠀\n⠀Secure :thumbsup:')
			
	run(bot)

if __name__ == '__main__':
	main()

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False".