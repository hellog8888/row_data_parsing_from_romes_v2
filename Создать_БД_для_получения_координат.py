import os
import glob
import shutil
import sqlite3
import warnings
import pandas as pd
from psycopg2 import Error
from transliterate import translit
from lib.measure_time import measure_time


warnings.simplefilter("ignore")


def to_sql(file):
    db_name = str(translit(str(file).strip('./lib/temp_folder\\')[:-5].replace('.', '_').replace(' ', '_'), 'ru', reversed=True))
    print(f'Чтение данных файла: {db_name}')

    with open(f'./lib\\created_database.txt', 'w') as created_database:
        print(f'{db_name}', file=created_database)

    try:
        print(f'Чтение данных файла: {db_name} завершено')
        print(f'Создание таблицы ...')

        SQLlite_db = sqlite3.connect(f'./lib/{db_name}.db', )
        dfs = pd.read_excel(file, sheet_name=None)
        for table, data in dfs.items():
            data.to_sql(table, SQLlite_db)

        print(f'Создание таблицы завершено')

    except (Exception, Error) as error:
        print("Error while creating the table", error)


@measure_time
def manage_database_from_eirs_(path):
    try:
        to_sql(glob.glob(f'{path}*.xlsx')[0])
    except IndexError:
        print("Пустая папка или содержит более 2-х файлов")
    try:
        shutil.move(glob.glob(f'{path}*.xlsx')[0], f'./lib/archive')
    except Exception:
        os.remove(glob.glob(f'{path}*.xlsx')[0])


manage_database_from_eirs_('./lib/temp_folder/')