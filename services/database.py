import json
import sqlite3

DB_FILENAME = 'user_data.db'


def init_database():
    with sqlite3.connect(DB_FILENAME) as con:
        cursor = con.cursor()
        char_table = 'create table if not exists character(' \
                     'key text primary key, level int, constellation int, ascension int, auto int, skill int, burst int)'

        cursor.execute(char_table)

        weapon_table = 'create table if not exists weapon(' \
                       'key text, level int, ascension int, refinement int, location text)'

        cursor.execute(weapon_table)

        artifact_table = 'create table if not exists artifact(' \
                         'set_key text, slot_key text, level int, rarity int, main_stat_key text, location text, ' \
                         'lock bool, substats text) '

        cursor.execute(artifact_table)
        con.commit()


def fill_database(data):
    with sqlite3.connect(DB_FILENAME) as con:
        cursor = con.cursor()
        table_names = ['character', 'weapon', 'artifact']
        for table_name in table_names:
            cursor.execute(f'delete from {table_name}')
        cursor.fetchall()

    for c in data['characters']:
        sql = 'insert into character (key, level, constellation, ascension, auto, skill, burst) ' \
              f'values (?, ?, ?, ?, ?, ?, ?)'

        cursor.execute(sql, [
            c['key'], c['level'], c['constellation'], c['ascension'], c['talent']['auto'], c['talent']['skill'], c['talent']['burst']
        ])

    for a in data['artifacts']:
        sql = 'insert into artifact (set_key, slot_key, level, rarity, main_stat_key, location, lock, substats)' \
              'values (?, ?, ?, ?, ?, ?, ?, ?)'

        cursor.execute(sql, [
            a['setKey'], a['slotKey'], a['level'], a['rarity'], a['mainStatKey'], a['location'], a['lock'], json.dumps(a['substats'])
        ])

    for w in data['weapons']:
        sql = 'insert into weapon (key, level, ascension, refinement, location)' \
              'values (?, ?, ?, ?, ?)'

        cursor.execute(sql, [
            w['key'], w['level'], w['ascension'], w['refinement'], w['location']
        ])

    con.commit()


def fetch_data(char_name):
    with sqlite3.connect(DB_FILENAME) as con:
        cursor = con.cursor()
        sql = 'select * from character where key = ?'
        char = cursor.execute(sql, [char_name]).fetchone()

        sql = 'select * from weapon where location = ?'
        weapon = cursor.execute(sql, [char_name]).fetchone()

        sql = 'select * from artifact where location = ?'
        artifacts = cursor.execute(sql, [char_name]).fetchall()

    return char, weapon, artifacts


if __name__ == '__main__':
    import json
    data = json.loads(open(r'C:\Users\sasha\Desktop\genshinData_GOOD_11.11.2021.json', 'r').read())
    init_database()
    fill_database(data)
    fetch_data('Xinyan')
