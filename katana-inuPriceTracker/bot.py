import asyncio
import json
from http import client
from pickle import TRUE
import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
import requests


load_dotenv(Path("secretKey.env"))
BotSecret = os.getenv('KBOTSECRET')

intents = discord.Intents.default()

intents.messages = True
intents.presences = False
intents.messages = True
intents.guilds = True


# Global variable
last_price = 0.0
Last_difference = 0.0
data = json
stringDiff = "0.00"


# getting json data from coingecko.com
def getCryptoPrice():
    global last_price
    global data
    URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=katana-inu'
   # Use variable for coin ID or just hard coded it.
    r = requests.get(url=URL)
    data = r.json()
   # print(data[0]['current_price'])


getCryptoPrice()  # Use different coin ID for different coin


client = discord.Client(commands_prefix = '.', intents=intents)


# Sending message to server
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!creator'):
        await message.channel.send('Created By @Harsh Gaur | DNPL')



# keep_alive()

@client.event
async def on_ready():
    print('Bot is ready')


client.run(BotSecret)