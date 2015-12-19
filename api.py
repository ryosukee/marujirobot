import requests
from requests_oauthlib import OAuth1
from datamanager import DataManager


class API:
    def __init__(self):
        self.db = DataManager()
        self.auth = OAuth1(*self.db.get_auth())
        self.url = 'https://api.twitter.com/1.1/statuses/'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.save()

    def __post(self, url, params=None):
        if params is None:
            response = requests.post(url, auth=self.auth)
        else:
            response = requests.post(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

    def __get(self, url, params=None):
        if params is None:
            response = requests.get(url, auth=self.auth)
        else:
            response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

    def tweet(self, message):
        url = self.url + 'update.json'
        params = {'status': message}
        self.__post(url, params)

    def reply(self, message, reply_id, reply_name):
        url = self.url + 'update.json'
        message = '@{} {}'.format(reply_name, message)
        params = {'status': message, 'in_reply_to_status_id': reply_id}
        self.__post(url, params)

    def get_mentions(self):
        url = self.url + 'mentions_timeline.json'
        last_id = self.db.get_last_id()
        if last_id is None:
            mentions = self.__get(url)
        else:
            params = {'since_id': last_id}
            mentions = self.__get(url, params)

        for mention in mentions[::-1]:
            yield mention
        self.db.set_last_id(mention['id_str'])
