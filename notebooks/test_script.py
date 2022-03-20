import discord
import requests
import re
import yaml
import paypalrestsdk

with open('config.yml', "r") as f:
    config = yaml.safe_load(f)

paypal_cid = config['Paypal Client ID']
paypal_cis = config['Paypal Client Secret']

token = config['Discord Bot Token']
client = discord.Client()

auth_url = 'http://127.0.0.1:8000/'

paypal_endpoint = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
response = requests.get(paypal_endpoint)

################################


def init_payment(amount):

    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": paypal_cid,
        "client_secret": paypal_cis})

    api_client = paypalrestsdk.Api({
        'mode': 'sandbox',
        "client_id": paypal_cid,
        "client_secret": paypal_cis})

    payment = paypalrestsdk.Payment({
        "intent": "order",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": auth_url + "payment/execute",  # link to tipship site
            "cancel_url": auth_url},  # link to tipship site
        "transactions": [{
            "amount": {
                "total": amount,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]},
        api=api_client)

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    return [link['href'] for link in payment['links'] if link['rel'] == 'approval_url'][0]


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

        if len(message.raw_mentions) > 1:
            await message.channel.send('Please mention a single user.')
            await message.add_reaction('\N{THUMBS DOWN SIGN}')
        else:
            paying_user = message.author
            target_user = await client.fetch_user(message.raw_mentions[0])
            amount = message.content.split(' ')[-1]

            auth_link = init_payment(amount)

            # pattern = r'\$pay [A-Za-z]+\#[0-9]{4} '
            # removed_embed_tag = [re.sub(pattern, '', i) for i in cleaned_lyrics]

            # print(message.channel) # can use this to only look at messages in a specific channel...

            await message.add_reaction('\N{THUMBS UP SIGN}')

            await paying_user.send(auth_link)
            await message.channel.send('Link sent to you!')

client.run(token)
