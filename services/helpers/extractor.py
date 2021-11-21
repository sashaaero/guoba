import json


def extract_char_data(file, char_name):
    user_data = json.loads(open(file, 'r').read())
    char, weapon = '', ''
    for char in user_data['characters']:
        if char['key'] == char_name:
            break
    for weapon in user_data['weapons']:
        if weapon['location'] == char_name:
            break

    return char, weapon


def parse_stat_value(value):
    from datatypes.datatypes import percent

    if value.endswith('+'):
        return int(value[:-1])
    if value.endswith('%'):
        return percent(value[:-1])
    return int(value)
