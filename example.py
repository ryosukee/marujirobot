from api import API
from other_api import OtherAPI


with API() as api:
    utils = OtherAPI()
    # ツイートする
    # api.tweet('tweet test2')

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

        # リプを返す
        content = ' '.join(text.split()[1:])
        if content == '天気':
            wethers = utils.get_wether()
            content = '\n'
            for i, day in enumerate(['今日', '明日', '明後日']):
                content += '{}\n  {}'.format(day, wethers[i]['telop'])
                maxt = wethers[i]['temperature']['max']
                mint = wethers[i]['temperature']['min']
                if maxt is not None:
                    content += ', 最高気温は{}℃, 最低気温は{}℃\n'.format(
                        maxt['celsius'], mint['celsius'])
                else:
                    content += '\n'
        api.reply(content, tweet_id, screen_name)
