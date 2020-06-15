import requests
import time
from pprint import pprint


class osuAPI():

    def __init__(self, *args, **kwargs):
        self.api_base_url = 'https://osu.ppy.sh/api/'
        with open('API_KEY') as f:
            self.api_key = f.read()

        self.params = {'k': self.api_key}

    def get_beatmaps(self, since, mode=2, a=1, limit=500, err_count=0):
        # print(f'get_beatmaps')
        api_url = f'{self.api_base_url}get_beatmaps'
        params = self.params
        params.update({
            'since': since,
            'm': mode,
            'a': a,
            'limit': limit,
        })
        res = requests.get(api_url, params=params)
        if res.status_code == 200:
            return res.json()
        else:
            print(f'request failed. since: {since}, status: {res.status_code} \nwill retry after 10 sec...')
            time.sleep(10)
            err_count += 1
            if err_count < 10:
                get_beatmaps(since=since, err_count=err_count)
            else:
                print(f'request failed 10 times. stop requesting')
                exit()


    def get_user(self, user, mode=2):
        print(f'get_user: {user}')
        api_url = f'{self.api_base_url}get_user'
        params = self.params
        params.update({
            'u': user,
            'm': mode,
        })
        res = requests.get(api_url, params=params)
        pprint(res.json())
        return

    def get_scores(self, beatmap, mode=2, limit=100):
        print(f'get_scores')
        api_url = f'{self.api_base_url}get_scores'
        params = self.params
        params.update({
            'b': beatmap,
            'm': mode,
            'limit': limit,
        })
        res = requests.get(api_url, params=params)
        scores = [{'date': r['date'], 'mods': r['enabled_mods'], 'maxcombo': r['maxcombo'], 'perfect': r['perfect'], 'pp': r['pp'],
                   'rank': r['rank'], 'score': r['score'], 'score_id': r['score_id'], 'user_id': r['user_id'], 'username': r['username']} for r in res.json()]
        pprint(scores)
        return
