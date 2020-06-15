from beatmap import osuAPI
from db_utils import Database, Table


def osu():
    osu_api = osuAPI()
    osu_api.get_user(user=5)


def getAllBeatmapInfo():
    osu_api = osuAPI()


def db():
    db_name = 'test.db'
    user_columns = {'user_id': 'integer primary key', 'playcount': 'integer',
                    'pp_rank': 'integer', 'pp_raw': 'integer', 'country': 'text'}
    table1 = Table(table_name='user', columns=user_columns)
    db = Database(db_name=db_name, table=table1)


def main():
    db()


if __name__ == "__main__":
    main()
