import sqlite3


class Table():

    def __init__(self, table_name: str, *args, **kwargs) -> None:
        self.table_name = table_name

    def name(self) -> str:
        return self.table_name

    def create(self, columns: dict) -> str:
        column_str = ''
        for k, v in columns.items():
            if not column_str:
                column_str += f'{k} {v}'
            else:
                column_str += f', {k} {v}'
        syntax = f'create table if not exists {self.table_name}({column_str})'
        return syntax

    def insert(self, columns: dict) -> str:
        placeholder = '?' + ', ?' * (len(columns) - 1)
        syntax = f'insert into {self.table_name} values ({placeholder})'
        return syntax

    def select(self, column: dict) -> str:
        syntax = f'select * from {self.table_name} where {column}=?'
        return syntax


class Database():

    def __init__(self, db_name: str, table: Table, *args, **kwargs) -> None:
        self.db_name = db_name
        self.table = table

    def connect(self) -> None:
        self.connect = sqlite3.connect(self.db_name)
        self.cursor = self.connect.cursor()

    def close(self) -> None:
        self.connect.close()

    def create_table(self, columns: dict) -> None:
        try:
            self.cursor.execute(self.table.create(columns=columns))
        except sqlite3.Error as e:
            print(e)

    def insert_table(self, columns: dict, data: list) -> None:
        try:
            self.cursor.executemany(self.table.insert(columns=columns), data)
            self.connect.commit()
        except sqlite3.Error as e:
            print(e)

    def select(self, column: dict, data: tuple):
        try:
            self.cursor.execute(self.table.select(column=column), data)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
