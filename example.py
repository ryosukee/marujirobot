from api import API
from utils import Utils


with API() as api:
    utils = Utils()
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

        # echo
        content = ' '.join(text.split()[1:])

        # weather
        if content == '天気':
            # jsonの情報の取得
            wethers = utils.get_wether()
            # 整理
            tomorrow = 1
            data = wethers[tomorrow]['date']
            data = '{}月{}日'.format(data.split('-')[1], data.split('-')[2])
            telop = wethers[tomorrow]['telop']
            maxt = wethers[tomorrow]['temperature']['max']
            mint = wethers[tomorrow]['temperature']['min']

            # テキストの生成
            content = '明日{}の天気は{}です！\n'.format(data, telop)
            if maxt is not None:
                content += '最高気温は{}℃, 最低気温は{}℃です．\n'.format(
                    maxt['celsius'], mint['celsius'])
        # リプを返す
        api.reply(content, tweet_id, screen_name)
