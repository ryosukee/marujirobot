import requests
from requests_oauthlib import OAuth1
from configparser import ConfigParser


class API:
    def __init__(self):
        keyf = 'keys.ini'
        config = ConfigParser()
        config.read(keyf)
        CK, CS, AT, AS = [config['Key'][k] for k in ['CK', 'CS', 'AT', 'AS']]

        self.auth = OAuth1(CK, CS, AT, AS)
        self.url = 'https://api.twitter.com/1.1/statuses/'

    def tweet(self, message):
        url = self.url + 'update.json'
        params = {'status': message}
        req = requests.post(url, auth=self.auth, params=params)
        if req.status_code == 200:
            print("OK")
        else:
            print("Error: %d" % req.status_code)
