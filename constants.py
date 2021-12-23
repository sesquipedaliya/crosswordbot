
'''Env constants'''
ENV_SLACK_OAUTH_APP_KEY = "SLACK_OAUTH_APP"
ENV_SLACK_OAUTH_BOT_KEY = "SLACK_OAUTH_BOT"

'''Time handling constants'''
NYT_TIMEZONE = 'US/Eastern'
DAYS_THAT_RELEASE_AT_6PM = {6, 0}  # Sunday and Monday puzzles release at 6 PM Eastern of the day before
SIX_PM_HOUR = 6 + 12
TEN_PM_HOUR = 10 + 12

'''Crossword length constants'''
LONGEST_POSSIBLE_TIME = 30 * 60
SHORTEST_POSSIBLE_TIME = 1

'''Emoji constants'''
BLEAKLEY_EMOJI = "bleakley"
CHECK_EMOJI = "white_check_mark"
CONFUSED_EMOJI = "confused_dog"
DNF_EMOJI = "dnf"
FORTY_TWO_EMOJI = "milky_way"
FORTY_SEVEN_EMOJI = "cecil"
HONEST_ABE_EMOJI = "honest-abe"
MIN_EMOJI = "crown"
SIXTEEN_EMOJI = "party-foursquare"
WAVE_EMOJI = "wave"
TWINS_0 = "twins-parrot"
TWINS_1 = "gemini"
TWINS_2 = "woman-with-bunny-ears-partying"
TWINS_3 = "man-with-bunny-ears-partying"
TWINS_4 = "handshake"
TWINS_5 = "spiderman_pointing"
TWINS_LIST = [TWINS_0, TWINS_1, TWINS_2, TWINS_3, TWINS_4, TWINS_5]
ALL_EMOJIS = {BLEAKLEY_EMOJI, CHECK_EMOJI, CONFUSED_EMOJI, DNF_EMOJI, FORTY_TWO_EMOJI, FORTY_SEVEN_EMOJI,
              HONEST_ABE_EMOJI, MIN_EMOJI, SIXTEEN_EMOJI, TWINS_0, TWINS_1, TWINS_2, TWINS_3, TWINS_4, TWINS_5,
              WAVE_EMOJI}
