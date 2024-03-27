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

dict_for_operator = \
    {
        'Общество с ограниченной ответственностью «Скартел»': 'Скартел',
        'Общество с ограниченной ответственностью \"Скартел\"': 'Скартел',

        'Общество с ограниченной ответственностью \"Т2 Мобайл\"': 'Т2 Мобайл',
        'Общество с ограниченной ответственностью «Т2 Мобайл»': 'Т2 Мобайл',

        'Публичное акционерное общество «Мобильные ТелеСистемы»': 'МТС',
        'Публичное акционерное общество \"Мобильные ТелеСистемы\"': 'МТС',

        'Публичное акционерное общество \"МегаФон\"': 'МегаФон',
        'Публичное акционерное общество «МегаФон»': 'МегаФон',

        'Публичное акционерное общество \"Ростелеком\"': 'Ростелеком',
        'Публичное акционерное общество «Ростелеком»': 'Ростелеком',
        'Публичное акционерное общество междугородной и международной электрической связи \"Ростелеком\"': 'Ростелеком',

        'Публичное акционерное общество «Вымпел-Коммуникации»': 'ВымпелКом',
        'Публичное акционерное общество \"Вымпел-Коммуникации\"': 'ВымпелКом'
    }


dict_ETC = \
    {
        '18.1.1.3.': 'GSM',
        '18.1.1.8.': 'GSM',
        '18.1.1.5.': 'UMTS',
        '18.1.1.6.': 'UMTS',
        '18.7.1.':   'LTE',
        '18.7.4.':   'LTE',
        '18.7.5.':   '5G NR',
        '19.2.':     'РРС'
    }


def to_sql(file):
    db_name = str(translit(str(file).strip('./lib/temp_folder\\')[:-5].replace('.', '_').replace(' ', '_'), 'ru', reversed=True))
    print(f'Чтение данных файла: {db_name}')

    with open(f'./lib\\created_database.txt', 'w') as created_database:
        print(f'{db_name}', file=created_database)
    try:
        #df = pd.read_excel(file).loc[:,
                   #['Наименование РЭС', 'Адрес', '№ вида ЕТС', 'Владелец', 'Широта', 'Долгота', 'Частоты',
                    #'Дополнительные параметры', 'Классы излучения', 'Серия последнего действующего РЗ/СоР',
                    #'Номер последнего действующего РЗ/СоР']]

        #df['№ вида ЕТС'] = [dict_ETC[x.strip()] for x in df['№ вида ЕТС']]
        #df['Владелец'] = [dict_for_operator[x.strip()] for x in df['Владелец']]

        #df['Серия_Номер_последнего_действующего_РЗ_СоР'] = df['Серия последнего действующего РЗ/СоР'].astype(str) + ' ' + df['Номер последнего действующего РЗ/СоР'].astype(str)

        #df = df.drop(['Серия последнего действующего РЗ/СоР'], axis=1)
        #df = df.drop(['Номер последнего действующего РЗ/СоР'], axis=1)

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