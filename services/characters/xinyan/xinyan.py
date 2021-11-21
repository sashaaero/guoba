import json
import sys
import math
from datatypes import Character


class Xinyan(Character):
    db_name = 'Xinyan'
    data_file = 'xinyan.json'

    @property
    def base_hp(self) -> int:
        asc_data = self.ascensions[self.ascension]
        steps = asc_data['max']['Lv'] - asc_data['min']['Lv']
        min_hp = asc_data['min']['Base HP']
        hp_step = (asc_data['max']['Base HP'] - min_hp) / steps
        lvl_offset = self.level - asc_data['min']['Lv']
        base_hp = min_hp + (hp_step * lvl_offset)
        return math.ceil(base_hp)


if __name__ == '__main__':
    from services.database import init_database, fill_database, fetch_data
    init_database()
    fill_database(json.loads(open(sys.argv[1], 'r').read()))
    stats_data = json.loads(open('xinyan.json', 'r').read())
    data = fetch_data(Xinyan.db_name)
    xinyan = Xinyan.from_db(*data)

    print(xinyan.base_hp)
