import argparse
import json
import os
import time
from datetime import datetime, timedelta

from osu.beatmap import osuAPI
from osu.db_utils import Database, Table


def get_beatmap_recursive(osu_api: osuAPI, since: str, json_name: str) -> None:
    json_flag = os.path.isfile(json_name)
    if json_flag:
        with open(json_name) as f:
            prev_res = set((b['beatmap_id'] for b in json.load(f)[-100:]))
    else:
        prev_res = set()

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

        if json_flag:
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


def get_score_recursive(osu_api: osuAPI, beatmap_id_list: set, db: Database, columns: dict) -> None:
    count = 0
    max_count = len(beatmap_id_list)
    for b in beatmap_id_list:
        scores = osu_api.get_scores(beatmap=b)
        count += 1
        print(f'beatmap_id: {b}, number of scores: {len(scores)}, count: {count} / {max_count}')
        data = [tuple(s.values()) for s in scores]
        # print(data)
        db.insert_table(columns=columns, data=data)
        time.sleep(5)


def getAllBeatmapData() -> None:
    osu_api = osuAPI()
    since = '2000-01-01'
    json_name = '../data/beatmaps.json'

    get_beatmap_recursive(osu_api, since, json_name)


def updateBeatmapData() -> None:
    osu_api = osuAPI()
    json_name = '../data/beatmaps.json'

    try:
        with open(json_name) as f:
            beatmaps = json.load(f)

        since = str(datetime.strptime(beatmaps[-1]['approved_date'],
                                      '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1))
    except FileNotFoundError:
        print('previous data is not found. start to collect all maps...')
        since = '2000-01-01'

    print('start updating beatmap data.')
    get_beatmap_recursive(osu_api, since, json_name)


def getAllScores() -> None:
    osu_api = osuAPI()
    json_name = '../data/beatmaps.json'
    table_name = 'score'
    db_name = '../data/scores.db'
    columns = {'score_id': 'integer primary key', 'beatmap_id': 'integer', 'score': 'integer',
               'user_id': 'integer', 'pp': 'real', 'maxcombo': 'integer', 'rank': 'text',
               'mods': 'integer', 'perfect': 'integer', 'date': 'text'}
    score_table = Table(table_name=table_name)
    db = Database(db_name=db_name, table=score_table)
    db.connect()
    db.create_table(columns=columns)

    with open(json_name) as f:
        beatmaps = json.load(f)

    beatmap_id_list = {b['beatmap_id'] for b in beatmaps}

    if db.select(select_column='beatmap_id', distinct=True):
        exist_beatmaps = {d[0] for d in db.select(select_column='beatmap_id', distinct=True)}
        remain_beatmaps = beatmap_id_list - exist_beatmaps
        get_score_recursive(osu_api=osu_api, beatmap_id_list=remain_beatmaps, db=db, columns=columns)
    else:
        get_score_recursive(osu_api=osu_api, beatmap_id_list=beatmap_id_list, db=db, columns=columns)

    db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-gb', '--getb', help='get all ranked beatmap. you should execute first.', action='store_true')
    parser.add_argument('-ub', '--updateb', help='update beatmap data.', action='store_true')
    parser.add_argument('-gs', '--gets', help='get all ranked score. read the result of --getb.', action='store_true')
    args = parser.parse_args()
    if args.getb:
        getAllBeatmapData()
    elif args.updateb:
        updateBeatmapData()
    elif args.gets:
        getAllScores()
    else:
        parser.print_help()
