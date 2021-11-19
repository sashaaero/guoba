import json, sys, os
from datatypes import Character, Talents, Weapon
from services.helpers.extractor import extract_char_data


class Xinyan(Character):
    db_name = 'Xinyan'


if __name__ == '__main__':
    from services.database import init_database, fill_database, fetch_data
    init_database()
    fill_database(json.loads(open(sys.argv[1], 'r').read()))
    stats_data = json.loads(open('xinyan.json', 'r').read())
    data = fetch_data(Xinyan.db_name)
    xinyan = Xinyan.from_db(*data)
