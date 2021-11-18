import json, sys
from datatypes import Character, Talents, Weapon


class Xinyan(Character):
    pass


if __name__ == '__main__':
    user_datafile = sys.argv[1]
    with open(user_datafile, 'r') as file:
        user_data = json.loads(file.read())
    for char in user_data['characters']:
        if char['key'] == 'Xinyan':
            break
    for weapon in user_data['weapons']:
        if weapon['location'] == 'Xinyan':
            break
    stats_data = json.loads(open('xinyan.json', 'r').read())
    weapon = Weapon(level=weapon['level'], ascension=weapon['ascension'], refinement=weapon['refinement'], atk=23)
    xinyan = Xinyan(level=char['level'], constellation=char['constellation'], ascension=char['ascension'], talents=Talents(**char['talent']), weapon=weapon)
