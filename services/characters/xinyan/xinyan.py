import json, sys
from datatypes import Character, Talents, Weapon
from services.helpers.extractor import extract_char_data


class Xinyan(Character):
    pass


if __name__ == '__main__':
    user_datafile = sys.argv[1]
    weapon, char = extract_char_data(user_datafile, 'Xinyan')
    stats_data = json.loads(open('xinyan.json', 'r').read())
    weapon = Weapon(level=weapon['level'], ascension=weapon['ascension'], refinement=weapon['refinement'], atk=23)
    xinyan = Xinyan(level=char['level'], constellation=char['constellation'], ascension=char['ascension'], talents=Talents(**char['talent']), weapon=weapon)
