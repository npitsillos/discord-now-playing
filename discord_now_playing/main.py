import os
import discord
import logging
import asyncio
import requests
import base64

from discord.ext.commands import Bot
from discord_now_playing import __version__
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NO_GAME_IMAGE = "data:image/gif;base64,R0lGODlhAQABAPAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
NO_GAME_STYLE = "border-radius:6px;background:#FFF;border:1px solid #e1e4e8;"
GAME_STYLE = "box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 3px 10px rgba(0,0,0,0.05);"


load_dotenv()
DISCORD_USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")

game_name = None
game_state = None
image_url = None

app = FastAPI()
client = discord.Client()

@app.on_event("startup")
async def setup_bot():
    asyncio.create_task(client.start(TOKEN))
    
@app.get("/")
def root():
    if image_url is not None:
        res = requests.get(image_url)
        base_64_str = "data:image/png;base64,"  + base64.b64encode(res.content).decode("utf-8") 
        data = "<svg fill='none' width='256' height='64' viewBox='0 0 256 64' xmlns='http://www.w3.org/2000/svg'><foreignObject width='256' height='64'><div xmlns='http://www.w3.org/1999/xhtml'><img src='{0}' style='{1}' alt='{2}' width='48' height='48'></img> {3} </div></foreignObject></svg>".format(base_64_str, GAME_STYLE, game_name.replace(' ', ''), game_name)
    else:
        data = "<svg fill='none' width='256' height='64' viewBox='0 0 256 64' xmlns='http://www.w3.org/2000/svg'><foreignObject width='256' height='64'><div xmlns='http://www.w3.org/1999/xhtml'><img src='{0}' style='{1}' width='48' height='48'></img>Nothing Playing</div></foreignObject></svg>".format(NO_GAME_IMAGE, NO_GAME_STYLE)
    return Response(content=data,  media_type="image/svg+xml")

@client.event
async def on_ready():
    global game_name
    global game_state
    global image_url
    logger.info("discordpy: {0}".format(discord.__version__))
    logger.info(client.user.name + " is online...")
    logger.info(__version__)

    members = client.guilds[0].members
    me = list(filter(lambda x: x.name == DISCORD_USERNAME, members))[0]
    if len(me.activities) > 0:
        game_name = me.activities[0].name
        game_state = me.activities[0].state
        image_url = me.activities[0].large_image_url

@client.event
async def on_member_update(member_before, member_after):
    global game_name
    global game_state
    global image_url
    if (isinstance(member_after, discord.Member)):
        activities = member_after.activities
        if len(activities) > 0:
            activity = activities[0]
            game_name = activity.name
            game_state = activity.state
            image_url = activity.large_image_url