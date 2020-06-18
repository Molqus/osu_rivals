import sqlite3


class Database():

    def __init__(self, db_name, table, *args, **kwargs):
        self.db_name = db_name
        self.table = table

    def connect(self):
        self.connect = sqlite3.connect(self.db_name)

    def close(self):
        self.connect.close()

    def create_table(self):
        try:
            self.connect.execute(self.table.create())
        except sqlite3.Error as e:
            print(e)


class Table():

    def __init__(self, table_name: str, columns: dict, *args, **kwargs) -> None:
        self.table_name = table_name
        self.columns = columns

    def name(self) -> str:
        return self.table_name

    def create(self):
        column_str = ''
        for k, v in self.columns.items():
            if not column_str:
                column_str += f'{k} {v}'
            else:
                column_str += f', {k} {v}'
        syntax = f'create table if not exists {self.table_name}({column_str})'
        return syntax

    def insert(self):
        pass