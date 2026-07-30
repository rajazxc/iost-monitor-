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
    client.run(DISCORD_TOKEN)
