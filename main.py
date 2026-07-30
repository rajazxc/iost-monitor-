import discord
import os
import requests
import json

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("channel_id", 0))
ADDRESS = os.environ.get("account")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

if not DISCORD_TOKEN:
    print("Error: discord_token environment variable missing.")
else:
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"Bot failed to start. Error: {e}")
        if DISCORD_TOKEN:
            print(f"Loaded Token Length: {len(DISCORD_TOKEN)}")
            print(f"Token starts with: {DISCORD_TOKEN[:10]}")
        else:
            print("Token is completely empty.")

