import os
import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONSTANTS_PATH = os.path.join(ROOT_DIR, "constants.yaml")

with open(CONSTANTS_PATH) as config_file:
    CONSTANTS = yaml.safe_load(config_file)


'''Env constants'''
ENV_SLACK_OAUTH_APP_KEY = "SLACK_APP_TOKEN"
ENV_SLACK_OAUTH_BOT_KEY = "SLACK_BOT_TOKEN"

'''Channel ids'''
CROSSWORD_CHANNEL_ID = CONSTANTS['channels']['prod_channel']
TEST_CHANNEL_ID = CONSTANTS['channels']['test_channel']

'''Time handling constants'''
NYT_TIMEZONE = 'US/Eastern'
DAYS_THAT_RELEASE_AT_6PM = {6, 0}  # Sunday and Monday puzzles release at 6 PM Eastern of the day before
SIX_PM_HOUR = 6 + 12
TEN_PM_HOUR = 10 + 12

'''Crossword length constants'''
LONGEST_POSSIBLE_TIME = 30 * 60
SHORTEST_POSSIBLE_TIME = 1

'''Emoji constants'''
emoji_constants = CONSTANTS['emojis']

JOIN_EMOJI = emoji_constants['join']
LEAVE_EMOJI = emoji_constants['leave']

CONFUSED_EMOJI = emoji_constants['confused']
DNF_EMOJI = emoji_constants['dnf']
CHECK_EMOJI = emoji_constants['check_mark']
MIN_EMOJI = emoji_constants['min_time']

EQUAL_TO: dict = emoji_constants['equal_to']

GREATER_THAN: dict = emoji_constants['greater_than']

LESS_THAN: dict = emoji_constants['less_than']

TWINS_LIST: list = emoji_constants['twins']

ALL_EMOJIS = {JOIN_EMOJI, LEAVE_EMOJI, CONFUSED_EMOJI, DNF_EMOJI, CHECK_EMOJI, MIN_EMOJI} \
             | set(EQUAL_TO.values()) \
             | set(GREATER_THAN.values()) \
             | set(LESS_THAN.values()) \
             | set(TWINS_LIST)
