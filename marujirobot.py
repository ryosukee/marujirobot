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


from docopt import docopt
from twitter_api import TwitterAPI
from dialogue_agent import DialogueAgent


with TwitterAPI() as twiapi:
    args = docopt(__doc__)
    agent = DialogueAgent(args['--terminal'], twiapi)

    if args['--weather']:
        # weatherの取得
        text = agent.get_weather()
        # ツイートする
        agent.speech('@marujiruo {}'.format(text))
    else:
        # 返事をする
        agent.reply()
