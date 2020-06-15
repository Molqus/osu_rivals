import datetime
import json
import os

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
    res = osu_api.get_beatmaps(since=since)
    print(type(res))

    # 重複削除
    res_id = {r['beatmap_id'] for r in res} & prev_res
    res = [r for r in res if r['beatmap_id'] not in res_id]
    # print(res)

    json_name = 'test.json'
    if os.path.isfile(json_name):
        with open(json_name, 'ab+') as f:
            f.seek(-1, 2)
            f.truncate()
            f.write(' ,'.encode())
            f.write(json.dumps(res).encode())
            f.write(']'.encode())
    else:
        with open(json_name, 'w') as f:
            json.dump(res, f)


if __name__ == "__main__":
    getAllBeatmapData()
