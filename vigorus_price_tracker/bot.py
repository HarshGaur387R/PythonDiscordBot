import asyncio
from itertools import cycle
import json
from http import client
from pickle import TRUE
from telnetlib import STATUS
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import tasks
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
from os import system
import requests
# import webserver
# from webserver import keep_alive


load_dotenv(Path("secretKey.env"))
BotSecret = os.getenv('VBOTSECRET')


intents = discord.Intents.all()

intents.messages = True
intents.presences = False
intents.messages = True
intents.guilds = True

# Global variable
last_price = 0.0
Last_difference = 0.0
data = json
stringDiff = "0.00"
current_price = 0


# getting json data from coingecko.com
def getCryptoPrice():
    global last_price
    global data
    global current_price
    URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=vigorus'
    # Use variable for coin ID or just hard coded it.
    r = requests.get(url=URL)
    data = r.json()
    current_price = '1KATA: ₹' + str(data[0]['current_price'])
    print(current_price)


# client = discord.Client(commands_prefix='.', intents=intents)
client = commands.Bot(command_prefix='.',intents=intents)

@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')


@client.command()
async def creator(ctx):
    await ctx.send("Created by (Harsh | DN#0506)")


@tasks.loop(seconds=10)
async def change_status():
   getCryptoPrice()
   await client.change_presence(activity=discord.Game(current_price))

# keep_alive()

try:
 client.run(BotSecret)
except discord.errors.HTTPException:
   print(discord.errors.HTTPException)
  #  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  #  system("python restarter.py")