from google.oauth2 import service_account
from googleapiclient import discovery, errors
from discord.ext import tasks
import discord
import os

key_file = "key-file.json"          # ATTENTION: YOU WILL NEED TO GET THIS FILE FROM A SERVICE ACCOUNT IN GOOGLE CLOUD
project_id = "satisfactory-383822"  # CHANGE ME
zone = "us-central1-a"              # CHANGE ME
vm_name = "satisfactory-server"     # CHANGE ME

# Set up the Discord bot with an API key stored in an environment variable
discord_api_key=os.environ["SatisfactoryBotAPIKey"]
bot=discord.Client()

# Set up the Google Cloud credentials using the JSON key file
gcp_credentials = service_account.Credentials.from_service_account_file(key_file)
compute = discovery.build("compute", "v1", credentials=gcp_credentials)

# For keeping track of how many hours the server has been running
hours = 0

# Start the VM
async def start_server(channel):
    await channel.send("Starting the VM...")
    try:
        start_request = compute.instances().start(project=project_id, zone=zone, instance=vm_name)
        start_response = start_request.execute()
        await channel.send(f"VM started.  Response:\n```json\n{start_response}```")
    except errors.HttpError as e:
        await channel.send(f"An error occurred while starting the VM: {e}")
        await channel.send(f"Response\n```json\n{start_response}```")

# Stop the VM
async def stop_server(channel):
    await channel.send("Stopping the VM...")
    try:
        stop_request = compute.instances().stop(project=project_id, zone=zone, instance=vm_name)
        stop_response = stop_request.execute()
        await channel.send(f"VM stopped.  Response:\n```json\n{stop_response}```")
    except errors.HttpError as e:
        await channel.send(f"An error occurred while stopping the VM: {e}")
        await channel.send(f"Response\n```json\n{stop_response}```")

@tasks.loop(minutes = 1.0)
async def runLoop():
    global hours
    if hours == 1:
        await runLoop.channel.send(f"@everyone Server has been running for {hours} hour.\nDon't forget to do `!stop` when you're finished to avoid incurring extra charges.")
    elif hours >= 2:
        await runLoop.channel.send(f"@everyone Server has been running for {hours} hours.\nDon't forget to do `!stop` when you're finished to avoid incurring extra charges.")
    hours += 1

@bot.event
async def on_message(message):
    channel = message.channel
    #if message.channel.id != 1096994664353120349:  # If you want the bot in only a single channel, uncomment this and put the channel_id here.
    #    return
    if len(message.content) < 1:
        return
    splitMessage=message.content.split()
    if splitMessage[0].lower() == "!start":
        global hours
        hours = 0
        await start_server(channel)
        runLoop.channel = channel
        runLoop.start()
    elif splitMessage[0].lower() == "!stop":
        await stop_server(channel)
        runLoop.stop()
    elif splitMessage[0][0] == '!':
        await channel.send(f"ERROR: Invalid command.")

@bot.event
async def on_ready():
    print("Bot is alive.")

if __name__ == "__main__":
    bot.run(discord_api_key)
