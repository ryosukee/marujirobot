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


def weather(screen_name='marujiruo', tweet_id=None):
    # 今日のweatherの取得
    text = agent.weather_text()
    # ツイートする
    if tweet_id is None:
        agent.speech('@{} {}'.format(screen_name, text))
    else:
        agent.speech(text, tweet_id, screen_name)


def lang8reminder(screen_name='marujiruo', tweet_id=None):
    # 今日のlang8投稿してるかどうか
    text = agent.lang8_reminder_text()
    # textが空なら投稿済み
    if text != '':
        # 投稿してなかったらリマインダーツイート
        if tweet_id is None:
            agent.speech('@{} {}'.format(screen_name, text), avoid_dupl='！')
        else:
            agent.speech(text, tweet_id, screen_name)


def lang8check(screen_name='marujiruo', tweet_id=None):
    # 昨日は誰が投稿忘れたか
    text = agent.lang8_check_text()
    if text != '':
        if tweet_id is None:
            agent.speech('@{} {}'.format(screen_name, text), avoid_dupl='！')
        else:
            agent.speech(text, tweet_id, screen_name)


with DataManager() as db:
    args = docopt(__doc__)
    agent = DialogueAgent(args['--terminal'], db)

    if args['--weather']:
        weather()
    elif args['--lang8-reminder']:
        lang8reminder()
    elif args['--lang8-check']:
        lang8check()
    elif args['--tweet'] is not None:
        agent.speech(args['--tweet'])
    else:
        # リプライに対して返事をする
        for message, tweet_id, screen_name in agent.get_message():
            if message == '-weather':
                weather(screen_name, tweet_id)
            elif message == '-lang8-check':
                lang8check(screen_name, tweet_id)
            elif message == '-lang8-reminder':
                lang8reminder(screen_name, tweet_id)
            else:
                text = agent.generate_reply(message)
                agent.speech(text, tweet_id, screen_name)
