import discord
import requests
import time
import json

with open("config.json", "r") as f:
    config = json.load(f)

DISCORD_TOKEN = config["discord_token"]
CHANNEL_ID = int(config["channel_id"])
ADDRESS = config["account"]

API = f"https://l2-scan.iost.io/api/addresses/{ADDRESS}/transactions"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_tx = None

@client.event
async def on_ready():
    global last_tx
    print(f"Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    while True:
        try:
            r = requests.get(API)
            data = r.json()

            txs = data.get("data", [])
            if txs:
                tx = txs[0]
                txhash = tx.get("txHash")

                if txhash != last_tx:
                    last_tx = txhash

                    amount = tx.get("amount")
                    sender = tx.get("from")
                    receiver = tx.get("to")

                    await channel.send(
                        f"💰 New Deposit\n"
                        f"Amount: {amount}\n"
                        f"From: {sender}\n"
                        f"To: {receiver}\n"
                        f"Tx: {txhash}"
                    )

        except Exception as e:
            print(e)

        time.sleep(10)

client.run(DISCORD_TOKEN)
print(DISCORD_TOKEN[:10])
