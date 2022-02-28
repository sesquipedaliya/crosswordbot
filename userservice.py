from slack_sdk import WebClient


class UserService:
    def __init__(self, responder_client: WebClient):
        self.responder_client = responder_client
        self.user_cache = dict()
        self.identity_cache = None

    def lookup_name(self, user_id):
        user_name = self.user_cache.get(user_id)
        if user_name is None:
            response = self.responder_client.users_info(user=user_id)
            user_name = response['user']['name']
            self.user_cache[user_id] = user_name
        return user_name

    def my_id(self):
        if self.identity_cache is None:
            response = self.responder_client.auth_test()
            self.identity_cache = response.get('user_id')
        return self.identity_cache
