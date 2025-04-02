import discord
from watchfiles import awatch
from getpass import getpass

CHANNEL_ID = input("Channel id: ")
BOT_TOKEN = getpass("Bot token: ")
LOG_PATH = './logs/latest.log'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'App initialized.')
    channel = client.get_channel(CHANNEL_ID)

    async for changes in awatch(LOG_PATH):
        
        change_type = list(changes)[0][0]
        
        # value of 2 means file was modified
        if change_type == 2:
            
            with open(LOG_PATH, 'r') as f:
            
                last_line = f.readlines()[-1]
                
                if (
                    "joined the game" in last_line or 
                    "left the game" in last_line
                ):
                    last_line_list = last_line.split(']')
                    last_line_list.pop(1)
                    last_line_list.pop(1)
                    last_line = ']'.join(last_line_list)
                    print(last_line)
                    await channel.send(
                        '```' + last_line + '```'
                    )

client.run(BOT_TOKEN)