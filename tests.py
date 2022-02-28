import json
import os
import unittest

from slack_bolt import App
from slack_sdk import WebClient

import constants
from bot import CrosswordBot


app = App(token=os.environ.get(constants.ENV_SLACK_OAUTH_BOT_KEY))

bot = CrosswordBot(app.client, 0)


class BotTests(unittest.TestCase):

    def test_user_joins(self):
        msg_json = {'token': 'hNr1EdaBzXINQjA8Rpyi1pXV', 'team_id': 'T2BDBKKFF', 'api_app_id': 'A02RKFU85QC',
                    'event': {'type': 'message', 'subtype': 'channel_join', 'ts': '1645382830.486329',
                              'user': 'U02MYDMN2N5', 'text': '<@U02MYDMN2N5> has joined the channel',
                              'channel': 'C02RKG29M4L', 'event_ts': '1645382830.486329', 'channel_type': 'channel'},
                    'type': 'event_callback', 'event_id': 'Ev034LAS8STA', 'event_time': 1645382830,
                    'authorizations': [{'enterprise_id': None, 'team_id': 'T2BDBKKFF', 'user_id': 'U02RC9P8F0F',
                                        'is_bot': True, 'is_enterprise_install': False}],
                    'is_ext_shared_channel': False,
                    'event_context': 'TMP'}

        is_msg_to_handle = bot.is_msg_to_handle(msg_json['event'])
        self.assertTrue(is_msg_to_handle)

    def test_user_leaves(self):
        msg_json = {'token': 'hNr1EdaBzXINQjA8Rpyi1pXV', 'team_id': 'T2BDBKKFF', 'api_app_id': 'A02RKFU85QC',
                    'event': {'type': 'message', 'subtype': 'channel_leave', 'ts': '1645382826.356069',
                              'user': 'U02MYDMN2N5', 'text': '<@U02MYDMN2N5> has left the channel',
                              'channel': 'C02RKG29M4L', 'event_ts': '1645382826.356069', 'channel_type': 'channel'},
                    'type': 'event_callback', 'event_id': 'Ev03496SMDT3', 'event_time': 1645382826,
                    'authorizations': [{'enterprise_id': None, 'team_id': 'T2BDBKKFF', 'user_id': 'U02RC9P8F0F',
                                        'is_bot': True, 'is_enterprise_install': False}],
                    'is_ext_shared_channel': False, 'event_context': 'TMP'}

        is_msg_to_handle = bot.is_msg_to_handle(msg_json['event'])
        self.assertTrue(is_msg_to_handle)


if __name__ == '__main__':
    unittest.main()
