import discord
import requests

with open('config.txt', 'r') as file:
    data = file.readlines()

token = data[2].split(":")[1].replace("\n", "")
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)