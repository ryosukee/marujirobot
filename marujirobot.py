"""
Usage:
    marujirobot.py [--terminal] [--weather]

Options:
    -h, --help
        show this message
    -v, --version
        show version
    --terminal
        run on terminal
    --weather
        send weather
"""


import sys
from docopt import docopt
from api import API
from utils import Utils


with API() as api:
    utils = Utils()
    args = docopt(__doc__)

    # run on terminal
    if args['--terminal']:
        for line in iter(sys.stdin.readline, '\n'):
            print(line.strip())
    elif args['--weather']:
        # jsonの情報の取得
        wethers = utils.get_wether()
        # 整理 today
        day = 0
        date = wethers[day]['date']
        date_label = wethers[day]['dateLabel']
        date = '{}月{}日'.format(date.split('-')[1], date.split('-')[2])
        telop = wethers[day]['telop']
        maxt = wethers[day]['temperature']['max']
        mint = wethers[day]['temperature']['min']

        # テキストの生成
        content = '{}({})の天気は{}'.format(date_label, date, telop)
        if maxt is not None:
            content += ',\n最低気温は{}℃, 最高気温は{}℃です! \n'.format(
                mint['celsius'], maxt['celsius'])
        else:
            content += 'です！\n'
        # ツイートする
        api.tweet('@marujiruo {}'.format(content))
    else:
        # リプを取得
        for mention in api.get_mentions():
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
            api.reply(content, tweet_id, screen_name)
