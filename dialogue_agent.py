import sys
from utils import Utils
from twitter_api import TwitterAPI


class DialogueAgent:
    def __init__(self, is_terminal, db):
        self.__is_terminal = is_terminal
        self.__utils = Utils()
        self.__twiapi = TwitterAPI(db)
        self.__db = db

    def weather_text(self, day=0):
        # jsonの取得
        weather = self.__utils.get_wether(day)
        # データの整理
        date = weather['date'][5:]
        rainfall = weather['rainfallchance']['period']
        for temp in weather['temperature']['range']:
            if temp['centigrade'] == 'max':
                temp_max = temp['content']  # 11
            if temp['centigrade'] == 'min':
                temp_min = temp['content']  # 5
        telop = weather['weather']

        # テキストの生成
        content = '{}は{}, 最低{}℃, 最高{}℃\n'.format(
            date, telop, temp_min, temp_max)
        content += '降水確率は, {} です！'.format(', '.join(
            '{}:{}%'.format(x['hour'], x['content']) for x in rainfall))
        return content

    def lang8_text(self):
        text = ''
        if not self.__utils.is_today_lang8():
            text = '今日のlang8がまだ投稿されてないです！'
        return text

    def generate_reply(self, text, method='markov'):
        if text == 'お題' or text == 'おだい':
            return self.__utils.get_odai()
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

    def speech(self, text, tweet_id=None, screen_name=None, avoid_dupl='。'):
        if self.__is_terminal:
            print(text)
        else:
            if tweet_id is not None and screen_name is not None:
                self.__twiapi.reply(text, tweet_id, screen_name)
            else:
                while self.__db.id_duplicate(text):
                    text += avoid_dupl
                self.__twiapi.tweet(text)
                self.__db.add_recent_tweet(text)

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
