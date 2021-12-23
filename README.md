# crosswordbot

The crosswordbot listens for completion times in the #crossword Slack channel
and inserts them into InfluxDB. For each message it successfully inserts, it
adds a customizable reaction emoji.

## Usage

```
export SLACK_OAUTH_APP=<insert app token, begins with xoxp>
export SLACK_OAUTH_BOT=<insert bot token, begins with xoxb>

python main.py
```

You can obtain the tokens through marathon or from a previous crosswordbot contributor.
The bot token is needed for the RTM client (listening to the channel) and the reacting Web Client (reacting to posts). 
The app token is needed for the history WebClient (fetching historical posts).

Running `main.py` will start a crosswordbot server listening to the #test-crossword channel for testing.

Most of the crosswordbot's behavior is defined by environment variables.
See the source code for a complete list of these.

## Deploying

1. Build and deploy the dockerfile `registry.prod.factual.com/crossword-bot:latest` via

```./docker_build.sh```

2. Go to [marathon](https://olympiad.prod.factual.com/#/apps/%2Fhr%2Fcrossword)
and restart the crossword bot.

3. Validate that the restart was successful.
