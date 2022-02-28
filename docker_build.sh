#!/bin/bash

set -fueo pipefail

IMAGE=registry.prod.factual.com/crossword-bot:latest
docker build -t $IMAGE .

# example of how to run
#docker run --rm -it -e SLACK_OAUTH_APP=$(cat credentials-app.txt) -e SLACK_OAUTH_BOT=$(cat credentials-bot.txt) -e ENV=dev $IMAGE

docker push $IMAGE
