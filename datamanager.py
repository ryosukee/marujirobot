import os
from configparser import ConfigParser
import pickle


class DataManager:
    def __init__(self):
        self.__file = './data.pkl'
        self.__data = dict()
        if not os.path.exists(self.__file):
            keyf = 'keys.ini'
            config = ConfigParser()
            config.read(keyf)
            auth = [config['Key'][k] for k in ['CK', 'CS', 'AT', 'AS']]
            self.__data['auth'] = auth
            self.__data['last_id'] = None
        else:
            self.load()

    def get_auth(self):
        return self.__data['auth']

    def get_last_id(self):
        return self.__data['last_id']

    def set_last_id(self, last_id):
        self.__data['last_id'] = last_id

    def save(self):
        pickle.dump(self.__data, open(self.__file, 'wb'))

    def load(self):
        self.__data = pickle.load(open(self.__file, 'rb'))
