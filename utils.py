import requests
from janome.tokenizer import Tokenizer


class Utils:
    def __init__(self):
        self.__tokenizer = Tokenizer()

    def get_wether(self):
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
        tokyo = '130010'
        params = {'city': tokyo}
        return requests.get(url, params=params).json()['forecasts']

    def morph_parse(self, text):
        for tok in self.__tokenizer.tokenize(text):
            yield tok
