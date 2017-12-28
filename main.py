import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

import platform

import json

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot", command_prefix="~", pm_help = True)

@client.event
async def on_ready():

	print("--- ⱭxD server's BOT ---\n")
	print('------------------------\n')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()) + '\n')
	print('------------------------\n')
	print('Use link below to invite de BOT to the server...')
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id) + '\n')
	print('------------------------\n')
	print('Created with <3 by https://github.com/profran with help of https://github.com/Habchy/BasicBot/wiki\n')


@client.command()
async def ping(*args):

	await client.say("Ping function is on development...")

@client.command()
async def test(*args):

	await client.say("Working fine...")

def run():

	with open('botinfo.json') as info_file:    
		data = json.load(info_file)

	client.run(data['bot'][0]['token'])

run()


# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.