from datetime import datetime, timedelta
import json
import os
import time

from beatmap import osuAPI
from db_utils import Database, Table

'''
すべてのビートマップの情報を収集する（API叩く）
ranked, loved, approvedだけbeatmapテーブルに格納する
その情報をもとにスコアを収集する
scoreテーブルに格納する
'''


def getAllBeatmapData():
    '''
    すべてのビートマップの情報を収集する
    sinceを用いることでleaderboardがある譜面だけ収集することができるので、
    1回APIを叩いて500譜面収集した後に最後の譜面のranked日時を次のsinceにする
    '''
    osu_api = osuAPI()
    since = '2000-01-01'
    prev_res = set()
    json_name = '../data/beatmaps.json'

    while 1:
        res = osu_api.get_beatmaps(since=since)
        end_flag = 0
        if len(res) < 500:
            end_flag = 1
        # print(type(res))

        # 重複削除
        res_duplicated = {r['beatmap_id'] for r in res} & prev_res
        res = [r for r in res if r['beatmap_id'] not in res_duplicated]
        # print(res)

        if os.path.isfile(json_name):
            with open(json_name, 'ab+') as f:
                f.seek(-1, 2)
                f.truncate()
                for r in res:
                    f.write(' ,'.encode())
                    f.write(json.dumps(r).encode())
                f.write(']'.encode())
        else:
            with open(json_name, 'w') as f:
                json.dump(res, f)

        since = str(datetime.strptime(res[-1]['approved_date'],
                                      '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1))

        if end_flag:
            print(f'reached latest ranked beatmap. since: {since}')
            break

        prev_res = {r['beatmap_id'] for r in res}
        print(since)
        print(res[0]['beatmap_id'], res[-1]['beatmap_id'], len(set(prev_res)))
        time.sleep(10)


if __name__ == "__main__":
    getAllBeatmapData()
