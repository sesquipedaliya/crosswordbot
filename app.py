import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Listens to any incoming message on the channel
@app.message(re.compile(".*"))
def message_hello(message, respond):
    # say() sends a message to the channel where the event was triggered
    app.client.reactions_add(channel=message['channel'], name="joy", timestamp=message['ts'])


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
