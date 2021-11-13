import math

ascensions_atk = {
    0: {'range': [1, 20], 'min': 21, 'max': 54, 'personal': {'atk': 1}},
    1: {'range': [20, 40],  'min': 69, 'max': 103, 'personal': {'atk': 1}},
    2: {'range': [40, 50], 'min': 115, 'max': 132, 'personal': {'atk': 1.06}},
    3: {'range': [50, 60], 'min': 147, 'max': 164, 'personal': {'atk': 1.12}},
    4: {'range': [60, 70], 'min': 175, 'max': 192, 'personal': {'atk': 1.12}},
    5: {'range': [70, 80], 'min': 203, 'max': 220, 'personal': {'atk': 1.18}},
    6: {'range': [80, 90], 'min': 231, 'max': 249, 'personal': {'atk': 1.24}},
}

weapon_atk = 41


def get_atk(ascension, lvl):
    asc = ascensions_atk[ascension]
    span = asc['range'][1] - asc['range'][0]
    step = (asc['max'] - asc['min']) / span
    atk = asc['min'] + (step * (lvl - asc['range'][0])) + weapon_atk
    if 'atk' in asc['personal']:
        atk *= asc['personal']['atk']
    return math.ceil(atk)


if __name__ == '__main__':
    print(get_atk(1, 25))
