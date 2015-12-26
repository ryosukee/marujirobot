import sys
from utils import Utils


class DialogueAgent:
    def __init__(self, is_terminal, twiapi):
        self.__is_terminal = is_terminal
        self.__utils = Utils()
        self.__twiapi = twiapi

    def weather_text(self, day=0):
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

    def lang8_text(self):
        text = ''
        if not self.__utils.is_today_lang8():
            text = '今日のlang8がまだ投稿されてないです！'
        return text

    def generate_reply(self, text, method='markov'):
        if method == 'echo':
            return text
        if method == 'markov':
            # 名詞をseedにする
            seeds = list()
            for tok in self.__utils.morph_parse(text):
                if '名詞' in tok.part_of_speech:
                    seeds.append(tok.surface)
            if len(seeds) == 0:
                seeds.append(text)
            # seedをqueryにしてツイッター検索をかける
            sentences = list()
            query = ' OR '.join(seeds)
            count = len(seeds) * 20
            for tweet in self.__twiapi.search(query, count=count)["statuses"]:
                sentences.append(self.__utils.clean_tweet(tweet['text']))
            # マルコフ連鎖で文を生成
            gen_sentence = self.__utils.markov_generate(sentences)
            return gen_sentence

    def speech(self, text, tweet_id=None, screen_name=None):
        if self.__is_terminal:
            print(text)
        else:
            if tweet_id is not None and screen_name is not None:
                self.__twiapi.reply(text, tweet_id, screen_name)
            else:
                self.__twiapi.tweet(text)

    def get_message(self):
        if self.__is_terminal:
            for line in iter(sys.stdin.readline, '\n'):
                yield (line.strip(), None, None)
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
                yield (' '.join(text.split()[1:]), tweet_id, screen_name)
