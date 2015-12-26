import os
import re
import random
import nltk
from collections import defaultdict
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
        re_url = re.compile('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')
        # 日本語以外の文字を排除(韓国語とか中国語とかヘブライ語とか)
        # http://qiita.com/haminiku/items/5907cb81325083cb36c7
        jp_chartype_tokenizer = nltk.RegexpTokenizer(
            '([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')

        for r in [re_rt, re_url]:
            text = r.sub('', text)
        text = "".join(jp_chartype_tokenizer.tokenize(text))
        return text
