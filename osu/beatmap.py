import time

import requests


class osuAPI():

    def __init__(self, *args, **kwargs):
        self.api_base_url = 'https://osu.ppy.sh/api/'
        with open('API_KEY') as f:
            self.api_key = f.read()

        self.params = {'k': self.api_key}

    def get_beatmaps(self, since: str, mode: int = 2, a: int = 1, limit: int = 500, err_count: int = 0) -> list:
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

        return []

    def get_user_from_name(self, user: int, mode: int = 2, user_type: str = 'string', err_count: int = 0) -> dict:
        api_url = f'{self.api_base_url}get_user'
        params = self.params
        params.update({
            'u': user,
            'm': mode,
            'type': user_type,
        })
        res = requests.get(api_url, params=params)
        if res.status_code == 200:
            if not res.json()[0]['pp_raw'] or float(res.json()[0]['pp_raw']) == 0.0:
                # ppがnullまたは0ならスコアの記録がないと判断できる
                data = {}
            else:
                r = res.json()[0]
                data = {'user_id': int(r['user_id']), 'user_name': user, 'playcount': int(r['playcount']),
                        'ranked_score': int(r['ranked_score']), 'total_score': int(r['total_score']),
                        'pp_rank': int(r['pp_rank']), 'level': float(r['level']),
                        'pp': float(r['pp_raw']), 'accuracy': float(r['accuracy']), 'country': r['country'],
                        'pp_country_rank': int(r['pp_country_rank'])}
            return data
        else:
            print(f'request failed. user: {user}, status: {res.status_code} \nwill retry after 10 sec...')
            time.sleep(10)
            err_count += 1
            if err_count < 10:
                self.get_user_from_name(user=user, err_count=err_count)
            else:
                print('request failed 10 times. stop requesting')
                exit()

        return {}

    def get_scores(self, beatmap: int, mode: int = 2, limit: int = 100, err_count: int = 0) -> list:
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

        return []
