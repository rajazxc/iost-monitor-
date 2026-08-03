import os
import sys
import asyncio
from threading import Thread

import discord
import requests
from flask import Flask

# ---------------- Flask ----------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# ---------------- Environment Variables ----------------

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
ADDRESS = os.environ.get("account")
CHANNEL_ID = os.environ.get("channel_id")

if not DISCORD_TOKEN or not ADDRESS or not CHANNEL_ID:
    print("Missing environment variables!")
    sys.exit(1)

CHANNEL_ID = int(CHANNEL_ID)

API = f"https://l2-scan.iost.io/api/addresses/{ADDRESS}/transactions"

# ---------------- Discord ----------------

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_tx = None

@client.event
async def on_ready():
    global last_tx

    print(f"Logged in as {client.user}")

    channel = await client.fetch_channel(CHANNEL_ID)
await channel.send("✅ Bot is online!")
    while True:
        try:
            response = requests.get(API, timeout=10)

            if response.status_code == 200:
                data = response.json()
                txs = data.get("data", [])

                if txs:
                    tx = txs[0]
                    txhash = tx.get("txHash")

                    if txhash and txhash != last_tx:

                        if last_tx is None:
                            last_tx = txhash
                        else:
                            last_tx = txhash

                            amount = tx.get("amount", "Unknown")
                            sender = tx.get("from", "Unknown")
                            receiver = tx.get("to", "Unknown")

                            await channel.send(
                                f"🔔 **New Deposit Detected!**\n\n"
                                f"💰 Amount: {amount}\n"
                                f"📤 From: {sender}\n"
                                f"📥 To: {receiver}\n"
                                f"🔗 Tx Hash: `{txhash}`"
                            )

        except Exception as e:
            print(e)

        await asyncio.sleep(10)

# ---------------- Start ----------------

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    client.run(DISCORD_TOKEN)