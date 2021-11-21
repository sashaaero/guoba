import json
import sys
import math
from datatypes import Character


class Xinyan(Character):
    db_name = 'Xinyan'
    data_file = 'xinyan.json'

    @property
    def base_hp(self) -> int:
        min_lvl = self.curr_ascension['min']['Lv']
        steps = self.curr_ascension['max']['Lv'] - min_lvl
        min_hp = self.curr_ascension['min']['Base HP']
        hp_step = (self.curr_ascension['max']['Base HP'] - min_hp) / steps
        lvl_offset = self.level - min_lvl
        base_hp = min_hp + (hp_step * lvl_offset)
        return math.ceil(base_hp)

    @property
    def base_atk(self) -> int:
        min_lvl = self.curr_ascension['min']['Lv']
        steps = self.curr_ascension['max']['Lv'] - min_lvl
        min_atk = self.curr_ascension['min']['Base ATK']
        atk_step = (self.curr_ascension['max']['Base ATK'] - min_atk) / steps
        lvl_offset = self.level - min_lvl
        base_atk = min_atk + (atk_step * lvl_offset) + self.weapon.atk
        return math.ceil(base_atk)

    @property
    def atk(self) -> int:
        atk_bonus = self.curr_ascension['min']['ATK']
        return math.ceil(self.base_atk + atk_bonus)

    @property
    def def_(self) -> int:
        min_lvl = self.curr_ascension['min']['Lv']
        steps = self.curr_ascension['max']['Lv'] - min_lvl
        min_def = self.curr_ascension['min']['Base DEF']
        def_step = (self.curr_ascension['max']['Base DEF'] - min_def) / steps
        lvl_offset = self.level - min_lvl
        def_ = min_def + (def_step * lvl_offset)
        return math.ceil(def_)

    @property
    def normal(self) -> dict:
        result = {}
        headers = self.normal_data['headers']
        level = self.normal_data['level']
        for i in range(4):  # Auto
            result[headers[i]] = int(self.atk * level[i])
        for i in range(4, 6):  # Charged
            result[headers[i]] = int((self.atk + (self.def_ * 0.5)) * level[i])
        result[headers[8]] = int(self.atk * level[8])
        result[headers[9]] = [int(self.atk * level[9][0]), int(self.atk * level[9][1])]
        return result


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

    print(xinyan.normal)

    print('Fighting Childe: Lvl. 60, Physical RES: 0')
    basic_res = (100 + xinyan.level) / ((100 + xinyan.level) + (100 + 60) * 1)
    normal = xinyan.normal
    for k, v in normal.items():
        if isinstance(v, list):
             normal[k] = [round(val * basic_res) for val in v]
        else:
            normal[k] = round(v * basic_res)

    print(normal)
