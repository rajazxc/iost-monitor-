import discord
import os
import requests
import asyncio
from flask import Flask
from threading import Thread
from discord.ext import tasks

# Web server for Render to stay online
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Load environment variables
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = os.environ.get("channel_id")
ADDRESS = os.environ.get("account")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_tx_hash = None

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Monitoring address: {ADDRESS}")
    check_transactions.start()

# Loop to check IOST Blockchain every 30 seconds
@tasks.loop(seconds=30)
async def check_transactions():
    global last_tx_hash
    
    if not CHANNEL_ID or not ADDRESS:
        return

    try:
        url = f"https://iostabc.com{ADDRESS}/txs?page=1&size=5"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            txs = []
            if isinstance(raw_data, dict):
                txs = raw_data.get("data", [])
                if isinstance(txs, dict): 
                    txs = txs.get("txs", [])
            elif isinstance(raw_data, list):
                txs = raw_data

            if not txs or not isinstance(txs, list):
                return
                
            latest_tx = txs[0]
            tx_hash = latest_tx.get("hash")
            
            if not tx_hash:
                return

            if last_tx_hash is None:
                last_tx_hash = tx_hash
                print(f"Baseline set. Latest TX Hash: {last_tx_hash}. Awaiting new live deposits...")
                return
                
            if tx_hash != last_tx_hash:
                last_tx_hash = tx_hash
                
                channel = client.get_channel(int(CHANNEL_ID))
                if channel:
                    embed = discord.Embed(title="💰 New Deposit Detected", color=0x00ff00)
                    embed.add_field(name="To Account:", value=ADDRESS, inline=False)
                    embed.add_field(name="Tx Hash:", value=f"[{tx_hash[:15]}...](https://iostabc.com{tx_hash})", inline=False)
                    embed.set_footer(text="IOST Monitor Bot")
                    
                    await channel.send(embed=embed)
                    print(f"Live alert dispatched successfully for TX: {tx_hash}")
                    
    except Exception as e:
        print(f"Error checking blockchain: {e}")

if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN environment variable missing.")
else:
    try:
        keep_alive()
        client.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"Bot failed to start. Error: {e}")
