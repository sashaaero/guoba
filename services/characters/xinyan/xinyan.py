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
        min_lvl = asc_data['min']['Lv']
        steps = asc_data['max']['Lv'] - min_lvl
        min_hp = asc_data['min']['Base HP']
        hp_step = (asc_data['max']['Base HP'] - min_hp) / steps
        lvl_offset = self.level - min_lvl
        base_hp = min_hp + (hp_step * lvl_offset)
        return math.ceil(base_hp)

    @property
    def base_atk(self) -> int:
        asc_data = self.ascensions[self.ascension]
        min_lvl = asc_data['min']['Lv']
        steps = asc_data['max']['Lv'] - min_lvl
        min_atk = asc_data['min']['Base ATK']
        atk_step = (asc_data['max']['Base ATK'] - min_atk) / steps
        lvl_offset = self.level - min_lvl
        base_atk = min_atk + (atk_step * lvl_offset) + self.weapon.atk
        return math.ceil(base_atk)

    @property
    def atk(self) -> int:
        atk_bonus = self.ascensions[self.ascension]['min']['ATK']
        return math.ceil(self.base_atk + atk_bonus)

    @property
    def def_(self) -> int:
        asc_data = self.ascensions[self.ascension]
        min_lvl = asc_data['min']['Lv']
        steps = asc_data['max']['Lv'] - min_lvl
        min_def = asc_data['min']['Base DEF']
        def_step = (asc_data['max']['Base DEF'] - min_def) / steps
        lvl_offset = self.level - min_lvl
        def_ = min_def + (def_step * lvl_offset)
        return math.ceil(def_)


if __name__ == '__main__':
    from services.database import init_database, fill_database, fetch_data
    init_database()
    fill_database(json.loads(open(sys.argv[1], 'r').read()))
    stats_data = json.loads(open('xinyan.json', 'r').read())
    data = fetch_data(Xinyan.db_name)
    xinyan = Xinyan.from_db(*data)

    print(f'{xinyan.base_hp=}')
    print(f'{xinyan.base_atk=}')
    print(f'{xinyan.atk=} ({xinyan.base_atk} +{xinyan.atk - xinyan.base_atk})')
    print(f'xinyan.def={xinyan.def_}')
