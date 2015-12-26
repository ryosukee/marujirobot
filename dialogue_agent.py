import sys
from utils import Utils


class DialogueAgent:
    def __init__(self, is_terminal, twiapi):
        self.__is_terminal = is_terminal
        self.__utils = Utils()
        self.__twiapi = twiapi

    def get_weather(self, day=0):
        # jsonの情報の取得
        wethers = self.__utils.get_wether()
        # 整理
        date = wethers[day]['date']
        date_label = wethers[day]['dateLabel']
        date = '{}月{}日'.format(date.split('-')[1], date.split('-')[2])
        telop = wethers[day]['telop']
        maxt = wethers[day]['temperature']['max']
        mint = wethers[day]['temperature']['min']

        # テキストの生成
        content = '{}({})の天気は{}'.format(date_label, date, telop)
        if mint is not None:
            content += ', \n最低気温は{}℃'.format(mint['celsius'])
        if maxt is not None:
            content += ',\n最高気温は{}℃'.format(maxt['celsius'])
        content += 'です！\n'
        return content

    def speech(self, text):
        if self.__is_terminal:
            print(text)
        else:
            self.__twiapi.tweet(text)

    def reply(self):
        # TODO: list
        def printkv(item, count=0):
            for k, v in item.items():
                if isinstance(v, dict):
                    print('{}{}: '.format(' '*count, k))
                    printkv(v, count + 1)
                else:
                    print('{}{}: {}'.format(' '*count, k, v))

        if self.__is_terminal:
            for line in iter(sys.stdin.readline, '\n'):
                printkv(self.__twiapi.search(line.strip()))
        else:
            # リプを取得
            for mention in self.__twiapi.get_mentions():
                text = mention['text']
                tweet_id = mention['id_str']
                screen_name = mention['user']['screen_name']
                # ユーザ情報(プロフィール)
                name = mention['user']['name']
                zone = mention['user']['time_zone']
                location = mention['user']['location']
                description = mention['user']['description']

                # echo
                content = ' '.join(text.split()[1:])

                # リプを返す
                self.__twiapi.reply(content, tweet_id, screen_name)
