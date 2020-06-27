import sqlite3
from typing import Optional


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

    def select(self, column: Optional[str], select_column: str) -> str:
        syntax = f'select {select_column} from {self.table_name}'
        if column:
            syntax += f' where {column}=?'
        return syntax

    def select_distinct(self, column: Optional[str], select_column: str):
        syntax = f'select distinct {select_column} from {self.table_name}'
        if column:
            syntax += f' where {column}=?'
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

    def select(self, data: tuple = None, column: str = None, select_column: str = '*', distinct: bool = False):
        try:
            if distinct:
                if column:
                    self.cursor.execute(self.table.select_distinct(column=column, select_column=select_column), data)
                    return self.cursor.fetchall()
                else:
                    self.cursor.execute(self.table.select_distinct(column=column, select_column=select_column))
                    return self.cursor.fetchall()
            else:
                if column:
                    self.cursor.execute(self.table.select(column=column, select_column=select_column), data)
                    return self.cursor.fetchall()
                else:
                    self.cursor.execute(self.table.select(column=column, select_column=select_column))
                    return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
