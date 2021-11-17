from typing import Union
from enum import Enum


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


class Talents:
    auto: int
    skill: int
    burst: int


class Weapon:
    level: int
    ascension: int
    refinement: int


class ArtifactType(Enum, str):
    flower = 'flower'
    plume = 'plume'
    sands = 'sands'
    goblet = 'goblet'
    circlet = 'circlet'


class ArtifactStatType(Enum, str):
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


class Character:
    level: int
    constellation: int
    ascension: int
    talents: Talents
    weapon: Weapon

    def __init__(self, *args):
        if self.__name__ == 'Character':
            raise NotImplementedError('Base class Character cannot be instanced')

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
