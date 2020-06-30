import json
import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from osu.beatmap import osuAPI

os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
if os.path.isfile('DB_TXT'):
    with open('DB_TXT') as f:
        username = f.readline().strip()
        password = f.readline().strip()
    db_uri = f'postgresql://{username}:{password}@localhost/scores'
else:
    db_uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Score(db.Model):
    __table__ = db.Model.metadata.tables['score']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def getUserInfo():
    osu_api = osuAPI()
    requested_user = request.form['user']
    target_user = request.form['target']
    is_same_mod = False if not request.form.getlist('mod') else True
    # TODO: get user info from database
    requested_user_info = osu_api.get_user_from_name(user=requested_user)
    target_user_info = osu_api.get_user_from_name(user=target_user)

    requested_user_score_list = db.session.query(Score).filter(Score.user_id == requested_user_info['user_id']).all()
    target_user_score_list = db.session.query(Score).filter(Score.user_id == target_user_info['user_id']).all()

    both_scored_maps = {s.beatmap_id for s in requested_user_score_list} & {
        s.beatmap_id for s in target_user_score_list}
    if is_same_mod:
        requested_user_score_mods = {
            s.beatmap_id: s.mods for s in requested_user_score_list if s.beatmap_id in both_scored_maps}
        target_user_score_mods = {
            s.beatmap_id: s.mods for s in target_user_score_list if s.beatmap_id in both_scored_maps}
        both_scored_maps = {b for b in both_scored_maps if requested_user_score_mods[b] == target_user_score_mods[b]}
    # make dicts to access user's scores by O(1) from beatmap id
    requested_user_score_dict = {s.beatmap_id: s for s in requested_user_score_list if s.beatmap_id in both_scored_maps}
    target_user_score_dict = {s.beatmap_id: s for s in target_user_score_list if s.beatmap_id in both_scored_maps}

    with open('../data/beatmaps.json', 'r') as f:
        beatmap_list = json.load(f)

    beatmap_dict = {b['beatmap_id']: b for b in beatmap_list}
    requested_user_win_maps = []
    requested_user_lose_maps = []
    tie_maps = []
    for b in both_scored_maps:
        requested_user_score = requested_user_score_dict[b].score
        target_user_score = target_user_score_dict[b].score
        if requested_user_score > target_user_score:
            requested_user_win_maps.append(beatmap_dict[b])
        elif requested_user_score < target_user_score:
            requested_user_lose_maps.append(beatmap_dict[b])
        else:
            tie_maps.append(beatmap_dict[b])

    res = {'wins': len(requested_user_win_maps), 'loses': len(requested_user_lose_maps), 'ties': len(tie_maps)}

    return render_template('result.html', requested_user=requested_user_info, target_user=target_user_info, res=res,
                           wins=requested_user_win_maps, losses=requested_user_lose_maps, ties=tie_maps)
