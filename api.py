import requests
from requests_oauthlib import OAuth1
from datamanager import DataManager as DB


class API:
    def __init__(self):
        self.__db = DB()
        self.__auth = OAuth1(*self.__db.get_auth())
        self.__url = 'https://api.twitter.com/1.1/statuses/'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__db.save()

    def __post(self, url, params=None):
        url = self.__url + url
        if params is None:
            response = requests.post(url, auth=self.__auth)
        else:
            response = requests.post(url, auth=self.__auth, params=params)
        response.raise_for_status()
        return response.json()

    def __get(self, url, params=None):
        url = self.__url + url
        if params is None:
            response = requests.get(url, auth=self.__auth)
        else:
            response = requests.get(url, auth=self.__auth, params=params)
        response.raise_for_status()
        return response.json()

    def tweet(self, message):
        url = 'update.json'
        params = {'status': message}
        self.__post(url, params)

    def reply(self, message, reply_id, reply_name):
        url = 'update.json'
        message = '@{} {}'.format(reply_name, message)
        params = {'status': message, 'in_reply_to_status_id': reply_id}
        self.__post(url, params)

    def get_mentions(self):
        url = 'mentions_timeline.json'
        last_id = self.__db.get_last_id()
        params = {'since_id': last_id} if last_id is not None else None
        mentions = self.__get(url, params)

        for mention in mentions[::-1]:
            self.__db.set_last_id(mention['id_str'])
            yield mention
