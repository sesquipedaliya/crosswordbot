import os

DEVELOPMENT_FLAG = "dev"
PRODUCTION_FLAG = "prod"

# crossword
CROSSWORD_CHANNEL_ID = 'C0120L5EV7E'

# test-crossword
TEST_CHANNEL_ID = 'C0175TUUGV6'

ENV_ENVIRONMENT = "ENV"
ENV_CHANNEL = "CHANNEL"


class Env:
    @staticmethod
    def channel_id():
        return os.getenv(ENV_CHANNEL, TEST_CHANNEL_ID)

    @staticmethod
    def is_production():
        return Env.get_environment() == PRODUCTION_FLAG and Env.channel_id() == CROSSWORD_CHANNEL_ID

    @staticmethod
    def get_environment():
        return os.getenv(ENV_ENVIRONMENT, DEVELOPMENT_FLAG)
