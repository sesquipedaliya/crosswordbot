import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import constants

from bot import CrosswordBot

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get(constants.ENV_SLACK_OAUTH_BOT_KEY))

bot = CrosswordBot(app.client)


# Listens to any incoming message on the channel
@app.message(re.compile(".*"))
def handle_with_crosswordbot(message, respond):
    bot.respond_to_new_message(message)


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    bot.respond_to_new_message(body['event'])


# Start the crosswordbot
if __name__ == "__main__":
    SocketModeHandler(app, os.environ[constants.ENV_SLACK_OAUTH_APP_KEY]).start()
