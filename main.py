import discord
import json

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
CHANNEL_ID = config["channel_id"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(TOKEN)
