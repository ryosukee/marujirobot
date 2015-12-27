"""
Usage:
    marujirobot.py [--terminal] [--weather] [--lang8]

Options:
    -h, --help
        show this message
    -v, --version
        show version
    --terminal
        run on terminal
    --weather
        send weather
    --lang8
        check lang8 post
"""


from docopt import docopt
from datamanager import DataManager
from dialogue_agent import DialogueAgent


with DataManager() as db:
    args = docopt(__doc__)
    agent = DialogueAgent(args['--terminal'], db)

    if args['--weather']:
        # 今日のweatherの取得
        text = agent.weather_text()
        # ツイートする
        agent.speech('@marujiruo {}'.format(text))
    elif args['--lang8']:
        # 今日のlang8投稿してるかどうか
        text = agent.lang8_text()
        # textが空なら投稿済み
        if text != '':
            # 投稿してなかったらリマインダーツイート
            agent.speech('@marujiruo {}'.format(text))
    else:
        # リプライに対して返事をする
        for message, tweet_id, screen_name in agent.get_message():
            text = agent.generate_reply(message)
            agent.speech(text, tweet_id, screen_name)
