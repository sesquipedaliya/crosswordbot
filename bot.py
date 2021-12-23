import random
from datetime import date
from datetime import timedelta
from itertools import groupby
from operator import attrgetter

from slack import RTMClient, WebClient

from constants import LONGEST_POSSIBLE_TIME, CHECK_EMOJI, CONFUSED_EMOJI, DNF_EMOJI, FORTY_TWO_EMOJI, \
    FORTY_SEVEN_EMOJI, HONEST_ABE_EMOJI, MIN_EMOJI, SIXTEEN_EMOJI, TWINS_LIST, WAVE_EMOJI, BLEAKLEY_EMOJI
from environment import Env
from influx import Reporter
from message import Message
from timehandler import TimeHandler
from userservice import UserService


class CrosswordBot:
    def __init__(self,
                 rtm_client: RTMClient,         # responds to new messages; uses bot token
                 history_client: WebClient,     # looks up past messages; uses app token
                 responder_client: WebClient,   # reacts to messages; uses bot token
                 days_to_post_compute=1,
                 channel_id=Env.channel_id()):
        self.channel_id = channel_id
        self.messages = list()

        self.rtm_client = rtm_client
        self.history_client = history_client
        self.responder_client = responder_client
        self.users = UserService(responder_client)
        self.reporter = Reporter()
        self.log_init()

        # post compute on init if you want to populate days back in time
        self.post_compute(days_to_post_compute)

    def post_compute(self, num_days):
        for i in reversed(range(num_days)):
            this_date = TimeHandler.get_today() - timedelta(i)
            print(f"post compute {this_date}")
            self.get_messages(this_date)
            # this should remove all responses but there may be a bug with adding reactions back
            # for m in self.messages:
            #     self.remove_all_responses(m)

            self.respond()

    @staticmethod
    def is_parent(message):
        return "thread_ts" not in message or message["thread_ts"] == message["ts"]

    def is_new_message(self, message):
        return self.is_parent(message) and \
               "user" in message and \
               message.get("channel") == self.channel_id

    def get_parsed_messages(self, messages):
        parsed_messages = []
        for message in messages:
            message["channel"] = self.channel_id
            if self.is_new_message(message):
                parsed_messages.append(Message(message, self.users))
        return parsed_messages

    def get_messages(self, curr_date: date):
        start_timestamp, end_timestamp = self.get_start_and_end_timestamp(curr_date)

        response = self.history_client.conversations_history(channel=self.channel_id,
                                                         limit=1000,
                                                         inclusive=0,
                                                         oldest=str(start_timestamp),
                                                         latest=str(end_timestamp))
        # todo look back in time for more than 1000 messages
        messages = response["messages"]
        parsed_responses = [m for m in self.get_parsed_messages(messages) if m.curr_date == curr_date]
        self.messages = parsed_responses

    @staticmethod
    def get_start_and_end_timestamp(curr_date):
        start_datetime = TimeHandler.get_begin_datetime_for_date(curr_date)
        end_datetime = TimeHandler.get_end_datetime_for_date(curr_date)
        start_timestamp = TimeHandler.get_timestamp_from_datetime(start_datetime)
        end_timestamp = TimeHandler.get_timestamp_from_datetime(end_datetime)
        print("date: {}\nstart timestamp: {}\nend timestamp: {}".format(curr_date, start_datetime, end_datetime))
        return start_timestamp, end_timestamp

    def append_to_messages(self, message):
        messages = [m for m in self.messages if m.curr_date == message.curr_date]
        self.log_time()
        self.log_messages()
        messages.append(message)
        self.messages = messages

    def respond_to_message_with(self, message: Message, emoji):
        try:
            if emoji not in message.reactions:
                self.responder_client.reactions_add(channel=self.channel_id, timestamp=message.timestamp, name=emoji)
                message.reactions.add(emoji)
                if emoji in TWINS_LIST:
                    message.twin_emoji = emoji
        except Exception as e:
            print(e)
            pass

    def hard_remove_response(self, message, emoji):
        try:
            self.responder_client.reactions_remove(channel=self.channel_id, timestamp=message.timestamp, name=emoji)
        except Exception as e:
            print(e, message, emoji)
            pass

    def remove_response_with(self, message, emoji):
        try:
            if emoji in message.reactions:
                self.hard_remove_response(message, emoji)
                message.reactions.remove(emoji)
                if message.twin_emoji and message.twin_emoji == emoji:
                    message.twin_emoji = None
        except Exception as e:
            print(e, message, emoji)
            pass

    def respond_to_message(self, message: Message, fastest_time):
        if message.isNotParsable:
            print("not parsable", message)
            self.respond_to_message_with(message, CONFUSED_EMOJI)
        elif message.isJoin:
            self.respond_to_message_with(message, WAVE_EMOJI)
        elif message.isLeave:
            self.respond_to_message_with(message, BLEAKLEY_EMOJI)
        elif message.isDNF:
            self.respond_to_message_with(message, DNF_EMOJI)
            self.respond_to_message_with(message, CHECK_EMOJI)
        else:
            if message.time > fastest_time:
                self.remove_response_with(message, MIN_EMOJI)
            else:
                self.respond_to_message_with(message, MIN_EMOJI)

            if message.time == 16:
                self.respond_to_message_with(message, SIXTEEN_EMOJI)
            if message.time == 42:
                self.respond_to_message_with(message, FORTY_TWO_EMOJI)
            if message.time == 47:
                self.respond_to_message_with(message, FORTY_SEVEN_EMOJI)
            if message.time >= 4 * 60:
                self.respond_to_message_with(message, HONEST_ABE_EMOJI)
            self.respond_to_message_with(message, CHECK_EMOJI)

    @staticmethod
    def compute_twin_emoji(message_list):
        for message in message_list:
            if message.twin_emoji:
                return message.twin_emoji
        return random.choice(TWINS_LIST)

    def respond_to_twins(self, timed_messages):
        timed_messages.sort(key=lambda m: m.time)
        grouped_messages = groupby(timed_messages, lambda m: m.time)
        for i, j in grouped_messages:
            message_list = list(j)
            print("GROUP")
            for message in message_list:
                print(message)
            if len(message_list) == 1 and message_list[0].twin_emoji:  # remove twin emoji if a singleton
                message = message_list[0]
                self.remove_response_with(message, message.twin_emoji)
            elif len(message_list) > 1:
                twin_emoji = self.compute_twin_emoji(message_list)
                for message in message_list:
                    if message.twin_emoji and message.twin_emoji != twin_emoji:
                        self.remove_response_with(message, message.twin_emoji)
                    self.respond_to_message_with(message, twin_emoji)

    def respond(self):
        timed_messages = [m for m in self.messages if m.time]

        try:
            min_time = min(timed_messages, key=attrgetter('time')).time
        except:
            min_time = LONGEST_POSSIBLE_TIME

        for m in self.messages:
            self.influx_report(m)
            self.respond_to_message(m, min_time)

        self.respond_to_twins(timed_messages)

    def influx_report(self, message):
        if message.time:
            self.reporter.report(name=message.name, timestamp=message.timestamp, time_sec=message.time,
                                 channel_id=self.channel_id)

    @staticmethod
    def is_deleted_message(message_json):
        return message_json.get("subtype") == "message_deleted"

    @staticmethod
    def is_edited_message(message_json):
        return message_json.get("subtype") == "message_changed"

    def remove_message_by_timestamp(self, timestamp):
        self.messages = [m for m in self.messages if m.timestamp != timestamp]

    def handle_new_message(self, message_json):
        message_to_add = None
        timestamp_to_delete = None
        if self.is_new_message(message_json):
            message_to_add = Message(message_json, self.users)
        elif self.is_deleted_message(message_json):
            timestamp_to_delete = message_json["previous_message"]["ts"]
        elif self.is_edited_message(message_json):
            message_to_add = Message(message_json["message"], self.users)
            self.remove_all_responses(message_to_add)  # remove hidden emojis from original message to recompute
            timestamp_to_delete = message_json["previous_message"]["ts"]

        if timestamp_to_delete:
            self.remove_message_by_timestamp(timestamp_to_delete)
            return True
        if message_to_add:
            self.append_to_messages(message_to_add)
            return True
        return False

    def remove_all_responses(self, message):
        for emoji in message.reactions:
            self.hard_remove_response(message, emoji)
        message.twin_emoji = None

    def log_init(self):
        print("channel_id: ", self.channel_id)

    @staticmethod
    def log_time():
        print(TimeHandler.get_today())

    def log_messages(self):
        print("current messages:")
        for m in self.messages:
            print(m)

    def on_message(self, **payload):
        print(payload['data'])
        if self.handle_new_message(payload['data']):
            self.respond()
