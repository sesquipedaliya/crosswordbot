from constants import TWINS_LIST, LONGEST_POSSIBLE_TIME, SHORTEST_POSSIBLE_TIME
from timehandler import TimeHandler


class Message:
    def __init__(self, message, user_service):
        self.user = message.get("user")
        self.name = user_service.lookup_name(self.user)
        self.text = message.get("text")
        self.timestamp = message.get("ts")
        self.curr_date = TimeHandler.process_date_from_str(self.timestamp)
        self.orig_message = message

        self.time = self.parse_time(self.text)
        self.is_dnf = self.is_dnf(self.text)
        self.is_join = self.is_join(message)
        self.is_leave = self.is_leave(message)
        self.is_not_parsable = not self.time and not self.is_dnf and not self.is_join and not self.is_leave

        self.twin_emoji = None  # initialized in process_reactions
        self.reactions = self.process_reactions(message.get("reactions"), user_service)

    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}".format(self.name, self.text, self.time, self.curr_date, self.twin_emoji)

    def add_reaction(self, emoji):
        self.reactions.add(emoji)
        if emoji in TWINS_LIST:
            self.twin_emoji = emoji
            return

    @staticmethod
    def parse_time(text):
        if len(text) > 0 and text[0] == ":":  # Felisa hack for :seconds format
            text = "0" + text
        split_text = text.split(":")
        if len(split_text) != 2:
            return None
        try:
            minutes = int(split_text[0].strip()) * 60
            seconds = int(split_text[1].strip())
            total_seconds = minutes + seconds
            if total_seconds > LONGEST_POSSIBLE_TIME or total_seconds < SHORTEST_POSSIBLE_TIME:
                return None
            return total_seconds
        except:
            return None

    @staticmethod
    def is_dnf(text):
        return "dnf" in text.lower()

    def process_reactions(self, reactions_list, user_service):
        # [{'name': 'heavy_check_mark', 'users': ['U4B2232AW'], 'count': 1}]
        my_reactions = set()
        if not reactions_list:
            return my_reactions

        my_id = user_service.my_id()
        for reaction in reactions_list:
            if my_id in reaction['users']:
                my_reactions.add(reaction['name'])
                if reaction in TWINS_LIST:
                    self.twin_emoji = reaction
        return my_reactions

    @staticmethod
    def is_join(message):
        return message.get("subtype") == "channel_join"

    @staticmethod
    def is_leave(message):
        return message.get("subtype") == "channel_leave"
