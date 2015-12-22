import requests


class Utils:
    def __init__(self):
        pass

    def get_wether(self):
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
        tokyo = '130010'
        params = {'city': tokyo}
        return requests.get(url, params=params).json()['forecasts']
