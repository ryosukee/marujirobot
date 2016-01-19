import os
import re
import random
import json
import datetime
import nltk
from collections import defaultdict
import requests
from janome.tokenizer import Tokenizer


class Utils:
    def __init__(self):
        neologd = './mecab-user-dict-seed.20151224'
        if os.path.exists(neologd):
            self.__tokenizer = Tokenizer(neologd)
        else:
            self.__tokenizer = Tokenizer()

    def get_wether(self, day):
        tokyo = 13
        url = 'http://www.drk7.jp/weather/json/{}.js'.format(tokyo)
        res = requests.get(url)
        res.encoding = 'UTF-8'
        pref = len('drk7jpweather.callback(')
        suf = len(');')
        data = json.loads(res.text[pref:-suf])
        target_day = datetime.datetime.today() + datetime.timedelta(day)
        target_day = '{}/{:0>2}/{:0>2}'.format(target_day.year, target_day.month, target_day.day)
        for weather in data['pref']['area']['東京地方']['info']:
            if weather['date'] == target_day:
                return weather

    def lastday_lang8(self):
        members = list()
        one_day = datetime.timedelta(days=1)
        today = datetime.datetime.today()
        yesterday = today - one_day

        marujirou = ('marujirou', 'http://lang-8.com/1269216/journals')
        yoshio = ('yoshio', 'http://lang-8.com/1266645/journals')
        sugar = ('sugar', 'http://lang-8.com/864499/journals')
        headers = {'Accept-Language': 'ja'}
        for name, url in [marujirou, yoshio, sugar]:
            res = requests.get(url, headers=headers)
            lastday = ''
            flag = False
            for line in res.text.split('\n'):
                if line == "<span class='journal_date floated_on_left'>":
                    flag = True
                    continue
                if flag:
                    day = line.split()[0]
                    lastday = datetime.datetime.strptime(day, '%Y年%m月%d日')
                    flag = False
                    # 昨日に投稿してる
                    if yesterday.date() == lastday.date():
                        break
                    # 昨日よりも前ということは昨日投稿してない
                    if yesterday > lastday:
                        members.append(name)
                        break
        return members

    def is_today_lang8(self):
        url = 'http://lang-8.com/1269216/journals'
        headers = {'Accept-Language': 'ja'}
        res = requests.get(url, headers=headers)
        lastday = ''
        flag = False
        for line in res.text.split('\n'):
            if line == "<span class='journal_date floated_on_left'>":
                flag = True
                continue
            if flag:
                lastday = line.split()[0]
                break
        today = datetime.datetime.today()
        today = '{}年{}月{}日'.format(today.year, today.month, today.day)
        return lastday == today

    def get_odai(self):
        odai = list()

        re_hatena = re.compile('今週のお題は「(?P<odai>.*?)」です')
        url = 'http://blog.hatena.ne.jp/-/campaign/odai'
        res = requests.get(url)
        odai.append(re_hatena.search(res.text).group('odai'))

        re_jugem = re.compile('<a href=.*?>(?P<odai>.*?)</a>')
        url = 'http://tbm.jugem.jp/'
        res = requests.get(url)
        res.encoding = 'EUC-JP'
        flag = False
        for line in res.text.split('\n'):
            if 'alt="お題一覧"' in line:
                flag = True
            if flag:
                if '</ul>' in line:
                    break
                m = re_jugem.search(line)
                if m is not None:
                    odai.append(m.group('odai'))
        return '/'.join(odai)


    def morph_parse(self, text):
        for tok in self.__tokenizer.tokenize(text):
            yield tok

    def markov_generate(self, source_sentences, ngram=2):
        # ngramの辞書を作る
        ngram_dict = defaultdict(list)
        for sentence in source_sentences:
            pre_words = ['__BOS{}__'.format(i) for i in range(ngram)]
            for tok in self.morph_parse(sentence):
                ngram_dict[tuple(pre_words)].append(tok.surface)
                pre_words.pop(0)
                pre_words.append(tok.surface)
            ngram_dict[tuple(pre_words)].append('__EOS__')
        # できた辞書からランダムに生成
        gen_text = ''
        next_word = ''
        pre_words = ['__BOS{}__'.format(i) for i in range(ngram)]
        while next_word != '__EOS__':
            candidate = ngram_dict[tuple(pre_words)]
            rand_index = random.randint(0, len(candidate) - 1)
            next_word = candidate[rand_index]
            gen_text += next_word
            pre_words.pop(0)
            pre_words.append(next_word)
        # EOSの除去
        gen_text = gen_text[:-len(next_word)]
        return gen_text

    def clean_tweet(self, text):
        re_rt = re.compile('RT @.*?:')
        re_rep = re.compile('@.*? ')
        re_url = re.compile('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')
        # 日本語以外の文字を排除(韓国語とか中国語とかヘブライ語とか)
        # http://qiita.com/haminiku/items/5907cb81325083cb36c7
        jp_chartype_tokenizer = nltk.RegexpTokenizer(
            '([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')

        for r in [re_rt, re_url, re_rep]:
            text = r.sub('', text)
        text = "".join(jp_chartype_tokenizer.tokenize(text))
        return text
