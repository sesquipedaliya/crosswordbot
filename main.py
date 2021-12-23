import asyncio
import logging
import os

from slack import RTMClient, WebClient

from bot import CrosswordBot
from constants import ENV_SLACK_OAUTH_APP_KEY, ENV_SLACK_OAUTH_BOT_KEY

logging.basicConfig(level=logging.DEBUG)

rtm_loop = asyncio.new_event_loop()
rtm_client = RTMClient(token=os.environ[ENV_SLACK_OAUTH_BOT_KEY], loop=rtm_loop)

web_loop = asyncio.new_event_loop()
web_client = WebClient(token=os.environ[ENV_SLACK_OAUTH_APP_KEY], loop=web_loop)

responder_loop = asyncio.new_event_loop()
responder_client = WebClient(token=os.environ[ENV_SLACK_OAUTH_BOT_KEY], loop=responder_loop)

bot = CrosswordBot(rtm_client, web_client, responder_client)

RTMClient.on(event='message', callback=bot.on_message)
rtm_client.start()
