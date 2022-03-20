import discord
import requests
import re

with open('key.txt', 'r') as file:
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

    if message.content.startswith('$pay'):

        sender = message.author.nick + '#' + message.author.discriminator

        #message_content = message.content

        # pattern = r'\$pay [A-Za-z]+\#[0-9]{4} '
        #removed_embed_tag = [re.sub(pattern, '', i) for i in cleaned_lyrics]

        # print(message.channel) # can use this to only look at messages in a specific channel...

        print(message.role_mentions)
        print(message.raw_mentions)
        print(message.mentions)
        print()
        print(message)
        # print(type(message.content))

        await message.add_reaction('\N{THUMBS UP SIGN}')

        await message.channel.send(sender)

client.run(token)
