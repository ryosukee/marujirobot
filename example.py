from api import API

with API() as api:
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
        api.reply(content, tweet_id, screen_name)
