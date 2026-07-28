import discord
import requests
import json

with open("config.json", "r") as f:
    config = json.load(f)

DISCORD_TOKEN = config["discord_token"]
CHANNEL_ID = int(config["channel_id"])
ADDRESS = config["account"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
print(repr(DISCORD_TOKEN))
print(len(DISCORD_TOKEN))

client.run(DISCORD_TOKEN)