import asyncio
from glob import glob
import imp
import json
from locale import format_string
from multiprocessing.connection import Client
from os import wait3
import string
import discord
import requests
import threading
import random
from discord.ext import tasks
from sqlalchemy import JSON
from webserver import keep_alive
import os

# json data from https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=vigorus


def wait():
    threading.Timer(3.0, wait).start()


# Global variable
last_price = 0.0
Last_difference = 0.0
data = json
stringDiff = "0.00"
# getting json data from coingecko.com


def getCryptoPrice(crypto):
    global last_price
    global data
    URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=vigorus'
    r = requests.get(url=URL)
    data = r.json()
   # print(data[0]['current_price'])


getCryptoPrice('vigorus')


# instatiate discord client
client = discord.Client()

# ===========Creating loop for getting data from coingecko.com every minute==============


@tasks.loop(seconds=7)
async def my_background_task():
    price_change_percentage = 0.00
    formatted_string = format_string
    global stringDiff
    global last_price
    """A background task that gets invoked every 1 minutes."""
    getCryptoPrice('vigorus')
    price_change_percentage = "{:.2f}".format(data[0]['price_change_percentage_24h']) 
    if(last_price != data[0]['current_price']):
        formatted_string = "{:.5f}".format(data[0]['current_price'] - last_price)
        stringDiff = str(formatted_string)
        print("last_price:", last_price, " current_price:",data[0]['current_price'], " difference:", stringDiff)

    await client.change_presence(activity=discord.Game(name="₹ "+str(last_price)+" | "+price_change_percentage+"%"))
    last_price = data[0]['current_price']


@my_background_task.before_loop
async def my_background_task_before_loop():
    await client.wait_until_ready()
# ==========================================================================================


@client.event
async def on_ready():
    print('Bot Logged In {client}')


# Sending message to server
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!creator'):
        await message.channel.send('Created By @Harsh Gaur | DNPL')


my_background_task.start()
keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
client.run(my_secret)