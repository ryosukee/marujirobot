"""
Usage:
    marujirobot.py [--terminal] [--weather] [--lang8-reminder] [--lang8-check] [--tweet <text>]

Options:
    -h, --help
        show this message
    -v, --version
        show version
    --terminal
        run on terminal
    --weather
        send weather
    --lang8-reminder
        lang8 reminder
    --lang8-check
        check lang8 posts
    --tweet <text>
        tweet
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
    elif args['--lang8-reminder']:
        # 今日のlang8投稿してるかどうか
        text = agent.lang8_reminder_text()
        # textが空なら投稿済み
        if text != '':
            # 投稿してなかったらリマインダーツイート
            agent.speech('@marujiruo {}'.format(text), avoid_dupl='！')
    elif args['--lang8-check']:
        # 昨日は誰が投稿忘れたか
        text = agent.lang8_check_text()
        if text != '':
            agent.speech('@marujiruo {}'.format(text), avoid_dupl='！')
    elif args['--tweet'] is not None:
        agent.speech(args['--tweet'])
    else:
        # リプライに対して返事をする
        for message, tweet_id, screen_name in agent.get_message():
            text = agent.generate_reply(message)
            agent.speech(text, tweet_id, screen_name)
