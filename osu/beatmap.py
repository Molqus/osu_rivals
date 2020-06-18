import time
from pprint import pprint

import requests


class osuAPI():

    def __init__(self, *args, **kwargs):
        self.api_base_url = 'https://osu.ppy.sh/api/'
        with open('API_KEY') as f:
            self.api_key = f.read()

        self.params = {'k': self.api_key}

    def get_beatmaps(self, since, mode=2, a=1, limit=500, err_count=0):
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
            data = [{'approved_date': r['approved_date'], 'beatmapset_id':int(r['beatmapset_id']),
                     'beatmap_id': int(r['beatmap_id']), 'diff_name': r['version'],
                     'approved': int(r['approved']), 'artist': r['artist'], 'title': r['title'],
                     'creator': r['creator'], 'creator_id': r['creator_id'],
                     'CS': float(r['diff_size']), 'AR': float(r['diff_approach']),
                     'OD': float(r['diff_overall']), 'HP': float(r['diff_drain']),
                     'difficulty': float(r['difficultyrating'])} for r in res.json()]
            return data
        else:
            print(f'request failed. since: {since}, status: {res.status_code} \nwill retry after 10 sec...')
            time.sleep(10)
            err_count += 1
            if err_count < 10:
                self.get_beatmaps(since=since, err_count=err_count)
            else:
                print('request failed 10 times. stop requesting')
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

    def get_scores(self, beatmap, mode=2, limit=100, err_count=0):
        api_url = f'{self.api_base_url}get_scores'
        params = self.params
        params.update({
            'b': beatmap,
            'm': mode,
            'limit': limit,
        })
        res = requests.get(api_url, params=params)
        if res.status_code == 200:
            scores = [{'score_id': int(r['score_id']), 'beatmap_id': beatmap, 'score':int(r['score']),
                       'user_id': int(r['user_id']), 'username': r['username'], 'pp': float(r['pp'] if r['pp'] else 0),
                       'maxcombo': int(r['maxcombo']), 'rank': r['rank'], 'mods': int(r['enabled_mods']),
                       'perfect': int(r['perfect']), 'date': r['date']} for r in res.json()]
            return scores
        else:
            print(f'request failed. beatmap: {beatmap}, status: {res.status_code} \nwill retry after 10 sec...')
            time.sleep(10)
            err_count += 1
            if err_count < 10:
                self.get_scores(beatmap=beatmap, err_count=err_count)
            else:
                print('request failed 10 times. stop requesting')
                exit()
