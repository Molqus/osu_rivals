import json
import os

from flask import Flask, render_template, request

from osu.beatmap import osuAPI
from osu.db_utils import Database, Table

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def getUserInfo():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    osu_api = osuAPI()
    requested_user = request.form['user']
    target_user = request.form['target']
    is_same_mod = True if request.form['mod'] == 'on' else False
    # TODO: get user info from database
    requested_user_info = osu_api.get_user_from_name(user=requested_user)
    target_user_info = osu_api.get_user_from_name(user=target_user)

    table_name = 'score'
    db_name = '../data/test.db'
    # db_name = '../data/test.db'
    score_table = Table(table_name=table_name)
    db = Database(db_name=db_name, table=score_table)
    column = 'user_id'

    db.connect()
    requested_user_score_list = db.select(column=column, data=(requested_user_info['user_id'], ))
    target_user_score_list = db.select(column=column, data=(target_user_info['user_id'], ))
    both_scored_maps = {s[1] for s in requested_user_score_list} & {s[1] for s in target_user_score_list}
    if is_same_mod:
        requested_user_score_mods = {s[1]: s[8] for s in requested_user_score_list if s[1] in both_scored_maps}
        target_user_score_mods = {s[1]: s[8] for s in target_user_score_list if s[1] in both_scored_maps}
        both_scored_maps = {b for b in both_scored_maps if requested_user_score_mods[b] == target_user_score_mods[b]}
    # make dicts to access user's scores by O(1) from beatmap id
    requested_user_score_dict = {s[1]: s for s in requested_user_score_list if s[1] in both_scored_maps}
    target_user_score_dict = {s[1]: s for s in target_user_score_list if s[1] in both_scored_maps}

    with open('../data/beatmaps.json', 'r') as f:
        beatmap_list = json.load(f)

    beatmap_dict = {b['beatmap_id']: b for b in beatmap_list}
    requested_user_win_maps = []
    requested_user_lose_maps = []
    tie_maps = []
    for b in both_scored_maps:
        requested_user_score = requested_user_score_dict[b][2]
        target_user_score = target_user_score_dict[b][2]
        if requested_user_score > target_user_score:
            requested_user_win_maps.append(beatmap_dict[b])
        elif requested_user_score < target_user_score:
            requested_user_lose_maps.append(beatmap_dict[b])
        else:
            tie_maps.append(beatmap_dict[b])

    res = {'wins': len(requested_user_win_maps), 'loses': len(requested_user_lose_maps), 'ties': len(tie_maps)}
    db.close()

    return render_template('result.html', requested_user=requested_user_info, target_user=target_user_info, res=res,
                           wins=requested_user_win_maps, losses=requested_user_lose_maps, ties=tie_maps)
