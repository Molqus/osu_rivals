from flask import Flask, render_template, request

from beatmap import osuAPI
from db_utils import Database, Table

app = Flask(__name__, static_folder='static')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def getUserInfo():
    osu_api = osuAPI()
    requested_user = request.form['user']
    target_user = request.form['target']
    # TODO: get user info from database
    requested_user_info = osu_api.get_user_from_name(user=requested_user)
    target_user_info = osu_api.get_user_from_name(user=target_user)

    table_name = 'score'
    db_name = 'test.db'
    # db_name = '../data/test.db'
    score_table = Table(table_name=table_name)
    db = Database(db_name=db_name, table=score_table)
    column = 'user_id'

    db.connect()
    requested_user_score_list = db.select(column=column, data=(requested_user_info['user_id'], ))
    target_user_score_list = db.select(column=column, data=(target_user_info['user_id'], ))
    both_scored_maps = {s[1] for s in requested_user_score_list} & {s[1] for s in target_user_score_list}
    # make dicts to access user's scores by O(1) from beatmap id
    requested_user_score_dict = {s[1]: s for s in requested_user_score_list if s[1] in both_scored_maps}
    target_user_score_dict = {s[1]: s for s in target_user_score_list if s[1] in both_scored_maps}

    requested_user_wins = requested_user_loses = ties = 0
    for b in both_scored_maps:
        requested_user_score = requested_user_score_dict[b][2]
        target_user_score = target_user_score_dict[b][2]
        if requested_user_score > target_user_score:
            requested_user_wins += 1
        elif requested_user_score < target_user_score:
            requested_user_loses += 1
        else:
            ties += 1

    res = {'wins': requested_user_wins, 'loses': requested_user_loses, 'ties': ties}
    db.close()

    return render_template('result.html', requested_user=requested_user_info, target_user=target_user_info, res=res)


if __name__ == "__main__":
    app.run(debug=True)
