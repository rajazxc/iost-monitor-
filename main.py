import os
import sys
import discord
import requests
import asyncio
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Your service is live"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
ADDRESS = os.environ.get("account")
channel_id_env = os.environ.get("channel_id")
CHANNEL_ID = int(channel_id_env) if channel_id_env else None

if not DISCORD_TOKEN or not CHANNEL_ID or not ADDRESS:
    print("Error: Missing Environment Variables")
    sys.exit(1)

API = f"https://iost.io{ADDRESS}/transactions"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_tx = None

@client.event
async def on_ready():
    global last_tx
    print(f"Logged in as {client.user}")
    
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Error: Channel {CHANNEL_ID} not found.")
        await client.close()
        sys.exit(1)

    while True:
        try:
            r = requests.get(API, timeout=10)
            if r.status_code == 200:
                data = r.json()
                txs = data.get("data", [])
                
                if txs and len(txs) > 0:
                    tx = txs[0]
                    txhash = tx.get("txhash")

                    if txhash != last_tx:
                        if last_tx is None:
                            last_tx = txhash
                            print(f"Initial tx set to: {txhash}")
                            continue

                        last_tx = txhash

                        amount = tx.get("amount")
                        sender = tx.get("from")
                        receiver = tx.get("to")

                        await channel.send(
                            f"🔔 **New Deposit Detected!**\n"
                            f"📝 **Amount:** {amount}\n"
                            f"📤 **From:** {sender}\n"
                            f"📥 **To:** {receiver}\n"
                            f"🔗 **Tx Hash:** {txhash}"
                        )
                        print(f"Alert sent for tx: {txhash}")
            else:
                print(f"API Error: Status code {r.status_code}")

        except Exception as e:
            print(f"Loop Exception: {e}")

        await asyncio.sleep(10)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    try:
        client.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("Error: Invalid DISCORD_TOKEN")
