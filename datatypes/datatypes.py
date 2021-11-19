import json
from typing import Union
from enum import Enum
from dataclasses import dataclass


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


@dataclass
class Talents:
    auto: int
    skill: int
    burst: int


@dataclass
class Weapon:
    @classmethod
    def from_db(cls, data):
        key, level, ascension, refinement, location = data
        return cls(level, ascension, refinement)

    level: int
    ascension: int
    refinement: int
    db_name: str = ''


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


@dataclass
class Artifact:
    @classmethod
    def from_db(cls, data):
        key, slot, level, rarity, main_stat_key, location, lock, substats = data
        substats = json.loads(substats)
        return cls(key, slot, level, rarity, main_stat_key, location, lock, substats)

    key: str  # TODO: Define all artifact sets
    slot: str
    type: ArtifactType
    level: int
    rarity: int
    main_stat_key: ArtifactStatType
    substats: dict[ArtifactStatType, Union[int, percent]]


@dataclass
class Character:
    level: int
    constellation: int
    ascension: int
    talents: Talents
    weapon: Weapon
    db_name: str = ''

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
        return 0

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
