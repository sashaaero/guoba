import json
import sys
import os
from typing import Union
from enum import Enum

from services.helpers.extractor import parse_stat_value


# noinspection PyPep8Naming
class percent:
    def __init__(self, p: Union[int, float]):
        self.percent = p

    def __repr__(self):
        return f'Percent({self.percent})'

    def __str__(self):
        return f'{self.percent}%'

    @property
    def float_value(self):
        return self.percent / 100

    def __radd__(self, other):
        val = 1 + self.float_value
        return other * val

    def __sub__(self, other):
        assert isinstance(other, percent)
        return percent(self.percent - other.percent)

    def __rmul__(self, other):
        if isinstance(other, percent):
            left_val = other.float_value
            right_val = self.float_value
            return left_val * right_val
        return other * self.float_value

    def __add__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, percent):
            return other.__rmul__(self)
        raise NotImplementedError


class Talents:
    auto: int
    skill: int
    burst: int

    def __init__(self, auto: int, skill: int, burst: int):
        self.auto = auto
        self.skill = skill
        self.burst = burst


class Weapon:
    level: int
    ascension: int
    refinement: int
    db_name: str = ''

    def __init__(self, level: int, ascension: int, refinement: int):
        self.level = level
        self.ascension = ascension
        self.refinement = refinement

    @classmethod
    def from_db(cls, data):
        key, level, ascension, refinement, location = data
        return cls(level, ascension, refinement)

    @property
    def atk(self):
        return 23  # TODO make real calculations


class ArtifactType(str, Enum):
    flower = 'flower'
    plume = 'plume'
    sands = 'sands'
    goblet = 'goblet'
    circlet = 'circlet'


class ArtifactStatType(str, Enum):
    hp = 'hp'
    hp_percent = 'hp_'
    atk = 'atk'
    atk_percent = 'atk_'
    def_percent = 'def_'
    elemental_mastery = 'eleMas'
    energy_recharge = 'enerRech_'
    crit_rate = 'critRate_'
    crit_damage = 'critDMG_'
    hydro_dmg = 'hydro_dmg_'
    electro_dmg = 'electro_dmg_'
    pyro_dmg = 'pyro_dmg_'
    dendro_dmg = 'dendro_dmg_'
    anemo_dmg = 'anemo_dmg_'
    cryo_dmg = 'cryo_dmg_'
    geo_dmg = 'geo_dmg_'
    physical_dmg = 'physical_dmg_'
    healing_bonus = 'heal_'


class Artifact:
    key: str  # TODO: Define all artifact sets
    slot: str
    type: ArtifactType
    level: int
    rarity: int
    main_stat_key: ArtifactStatType
    substats: dict[ArtifactStatType, Union[int, percent]]

    def __init__(self, key: str, slot: str, type: ArtifactType, level: int, rarity: int, main_stat_key: ArtifactStatType, substats: dict[ArtifactStatType, Union[int, percent]]):
        self.key = key
        self.slot = slot
        self.type = type
        self.level = level
        self.rarity = rarity
        self.main_stat_key = main_stat_key
        self.substats = substats

    @classmethod
    def from_db(cls, data):
        key, slot, level, rarity, main_stat_key, location, lock, substats = data
        substats = json.loads(substats)
        return cls(key, slot, level, rarity, main_stat_key, location, substats)


class Character:
    level: int
    constellation: int
    ascension: int
    talents: Talents
    weapon: Weapon
    curr_ascension: dict
    normal_data: dict
    skill_data: dict
    burst_data: dict
    db_name: str = ''
    data_file: str = ''

    def __init__(self, level: int, constellation: int, ascension: int, talents: Talents, weapon: Weapon):
        self.level = level
        self.constellation = constellation
        self.ascension = ascension
        self.talents = talents
        self.weapon = weapon

        stats_file = os.path.join(os.path.dirname(sys.modules[self.__class__.__module__].__file__), self.data_file)
        stats = json.loads(open(stats_file, 'r').read())

        stat_progression = stats['stat_progression']
        headers = stat_progression['headers']
        levels = stat_progression['levels']
        low, high = levels[self.ascension * 2], levels[self.ascension * 2 + 1]
        low_dict = {headers[j]: parse_stat_value(low[j]) for j in range(len(headers))}
        high_dict = {headers[j]: parse_stat_value(high[j]) for j in range(len(headers))}
        self.curr_ascension = dict(min=low_dict, max=high_dict)

        curr_level = [parse_stat_value(val) for val in stats['normal']['levels'][self.talents.auto-1]]

        self.normal_data = dict(headers=stats['normal']['headers'], level=curr_level)

    @classmethod
    def from_db(cls, char_data, weapon_data, artifacts_data):
        from services.weapons import weapons_mapping
        name, level, constellation, ascension, auto, skill, burst = char_data
        weapon_cls = weapons_mapping.weapon_classes[weapon_data[0]]
        return cls(level, constellation, ascension, Talents(auto, skill, burst), weapon_cls.from_db(weapon_data))

    @property
    def base_hp(self) -> int:
        return 0

    @property
    def max_hp(self) -> int:
        return self.base_hp

    @property
    def base_atk(self) -> int:
        return 0

    @property
    def atk(self) -> int:
        return self.base_atk

    @property
    def base_def(self) -> int:
        return 0

    @property
    def def_(self) -> int:
        return self.base_def

    @property
    def elemental_mastery(self) -> int:
        return 0

    @property
    def crit_rate(self) -> percent:
        return percent(5)

    @property
    def crit_dmg(self) -> percent:
        return percent(50)

    @property
    def healing_bonus(self) -> percent:
        return percent(0)

    @property
    def incoming_healing_bonus(self) -> percent:
        return percent(0)

    @property
    def energy_recharge(self) -> percent:
        return percent(100)

    @property
    def shield_strength(self) -> percent:
        return percent(0)

    @property
    def pyro_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def pyro_res(self) -> percent:
        return percent(0)

    @property
    def hydro_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def hydro_res(self) -> percent:
        return percent(0)

    @property
    def dendro_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def dendro_res(self) -> percent:
        return percent(0)

    @property
    def electro_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def electro_res(self) -> percent:
        return percent(0)

    @property
    def anemo_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def anemo_res(self) -> percent:
        return percent(0)

    @property
    def cryo_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def cryo_res(self) -> percent:
        return percent(0)

    @property
    def geo_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def geo_res(self) -> percent:
        return percent(0)

    @property
    def physical_dmg_bonus(self) -> percent:
        return percent(0)

    @property
    def physical_res(self) -> percent:
        return percent(0)

    @property
    def normal(self) -> dict:
        return {}

    @property
    def skill(self) -> dict:
        return {}

    @property
    def burst(self) -> dict:
        return {}
