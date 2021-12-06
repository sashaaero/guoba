import requests
import sys
import json
from bs4 import BeautifulSoup
import re


def parse_stat_progression(stat_progression, first: int = 0):
    exclude = ['Ascension', 'Ascension Materials', '']
    headers = [elem.text for elem in stat_progression.contents[first] if elem.text not in exclude]
    size = len(headers)
    levels = []
    for row in stat_progression.contents[first + 1:]:
        row_data = []
        if len(row) == 0:
            continue
        else:
            for i in range(size):
                row_data.append(row.contents[i].text)
            levels.append(row_data)

    return headers, levels


# я не пришло в голову, как можно по нормальному дополнить функцию parse_stat_progression для сабстатов
def parse_substat(stat_progression):
    levels = [[] for i in range(4)]
    headers = []
    for row in stat_progression.contents[1:]:
        if len(row) == 0:
            continue
        else:
            headers.append(row.contents[0].text)
            for i, col in zip(range(4), row.contents[1:]):
                levels[i].append(col.text)
    return headers[1:], levels


def parse_normal(normal):
    matrix = []
    for row in normal.contents[1:]:
        matrix.append([elem.text for elem in row.contents])

    matrix = list(zip(*matrix))
    headers = matrix[0]
    levels = matrix[1:]
    return headers, levels


def parse_link(url, name, compile):
    response = requests.get(url)
    response.raise_for_status()

    text = response.text
    soup = BeautifulSoup(text, 'lxml')
    link = soup.find_all('a', href=re.compile(compile))

    for i in range(0, len(link) - 1, 2):
        if link[i - 1].contents[0] == name:
            link = link[i - 1].attrs['href']
            break
    return link


def char(char_name):
    url = f"https://genshin.honeyhunterworld.com/db/char/{char_name}/?lang=EN"
    response = requests.get(url)
    response.raise_for_status()

    result = {
        "main_info": {"full_name": "", "element": "", "weapon": "", "personal_stat": "", "rarity": ""},
        "stat_progression": {"headers": [], "levels": []},
        "normal": {"title": "", "headers": [], "levels": {}},
        "skill": {"title": "", "headers": [], "levels": {}},
        "burst": {"title": "", "headers": [], "levels": {}}
    }

    text = response.text

    soup = BeautifulSoup(text, 'lxml')

    tables_order = {'normal': 1, 'skill': 2, 'burst': 3}
    if char_name in ('ayaka', 'mona'):
        tables_order['burst'] = 4

    # ------ Main info ------

    full_name = soup.find('div', {'class': ['custom_title']}).text
    result['main_info']['full_name'] = full_name

    element_img = soup.find('img', {'class': ['char_portrait_card_sea_element']})
    element_elem = element_img.attrs['data-src']
    i = element_elem.rfind('/')
    j = element_elem.find('_', i)
    element = element_elem[i + 1:j]
    result['main_info']['element'] = element

    weapon_type = soup.find('a', href=re.compile('^/db/weapon/'))
    result['main_info']['weapon'] = weapon_type.contents[0]

    rarity = soup.find('table', {'class': ['item_main_table']})
    result['main_info']['rarity'] = len(rarity.contents[3].next.nextSibling.contents)

    # ------ Talants and Stats ------

    live_data = soup.find('div', {'id': 'live_data'})
    span_stats = live_data.find_all('div', {'class': ['skilldmgwrapper']})
    name_stats = live_data.find_all('table', {'class': ['item_main_table']})

    headers, levels = parse_stat_progression(span_stats[0].next)
    result['stat_progression']['headers'] = headers
    result['stat_progression']['levels'] = levels

    for k, v in tables_order.items():
        headers, levels = parse_normal(span_stats[v].next)
        result[k]['title'] = name_stats[v].next.contents[1].contents[0].text
        result[k]['headers'] = headers
        result[k]['levels'] = levels

    # ------ Saving result ------

    with open(f'{char_name}.json', 'w') as file:
        file.write(json.dumps(result, indent=2))


def weapon(weapon_name, weapon_type):
    result = {
        "main_info": {"full_name": "", "type": "", "secondary_stat": "", "rarity": ""},
        "stat_progression": {"headers": [], "levels": []}
    }
    url = f"https://genshin.honeyhunterworld.com/db/weapon/{weapon_type}/?lang=EN"

    link = parse_link(url, weapon_name, '^/db/weapon/w_')

    url = f"https://genshin.honeyhunterworld.com{link}"
    response = requests.get(url)
    response.raise_for_status()

    text = response.text
    soup = BeautifulSoup(text, 'lxml')

    # ------ Main info ------

    result['main_info']['full_name'] = weapon_name
    result['main_info']['type'] = weapon_type

    weapon_stats = soup.find('table', {'class': ['item_main_table']})
    result['main_info']['secondary_stat'] = weapon_stats.contents[3].contents[1].text

    result['main_info']['rarity'] = len(weapon_stats.contents[1].next.nextSibling.contents)

    # ------ Weapon stats ------

    weapon_stats = soup.find('table', {'class': ['add_stat_table']})

    headers, levels = parse_stat_progression(weapon_stats)

    result['stat_progression']['headers'] = headers
    result['stat_progression']['levels'] = levels

    # ------ Saving result ------

    with open(f'{weapon_name}.json', 'w') as file:
        file.write(json.dumps(result, indent=2))


def artifact(artifact_name):
    result = {
        "main_info": {"full_name": "", "rarity": ""},
        "Possible Main Stat Roll 1": {"headers": [], "levels": []},
        "Possible Substat Roll 1": {"headers": [], "levels": []},
        "Possible Main Stat Roll 2": {"headers": [], "levels": []},
        "Possible Substat Roll 2": {"headers": [], "levels": []}
    }

    url = f"https://genshin.honeyhunterworld.com/db/artifact/?lang=EN"

    link = parse_link(url, artifact_name, '^/db/art/family/a_')

    url = f"https://genshin.honeyhunterworld.com{link}"
    response = requests.get(url)
    response.raise_for_status()

    text = response.text
    soup = BeautifulSoup(text, 'lxml')

    # ------ Main info ------

    result['main_info']['full_name'] = artifact_name

    # ------ Artifact stats ------
    intermediate = []
    artifact_stats = soup.find_all('span', {'class': ['item_secondary_title']})
    for row in artifact_stats:
        if " Possible Main Stat Roll" in row.contents[0]:
            intermediate.append(parse_stat_progression(row.nextSibling.contents[0]))
        elif " Possible Substat Roll" in row.contents[0]:
            intermediate.append(parse_substat(row.nextSibling.contents[0]))

    # ------ Low stars artifact stats ------
    result['Possible Main Stat Roll 1']['headers'] = intermediate[0][0]
    result['Possible Main Stat Roll 1']['levels'] = intermediate[0][1:]

    # ------ Low stars artifact sub stats ------
    result['Possible Substat Roll 1']['headers'] = intermediate[1][0]
    result['Possible Substat Roll 1']['levels'] = intermediate[1][1:]

    # ------ high stars artifact stats ------
    result['Possible Main Stat Roll 2']['headers'] = intermediate[2][0]
    result['Possible Main Stat Roll 2']['levels'] = intermediate[2][1:]

    # ------ high stars artifact sub stats ------
    result['Possible Substat Roll 2']['headers'] = intermediate[3][0]
    result['Possible Substat Roll 2']['levels'] = intermediate[3][1:]
    # ------ Saving result ------

    with open(f'{artifact_name}.json', 'w') as file:
        file.write(json.dumps(result, indent=2))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('usage: python parser.py [char]/[weapon] name')
    parser = sys.argv[1]
    name = sys.argv[2]
    if parser == 'char':
        char(name)
    elif parser == 'weapon':
        weapon(name, sys.argv[3])
    elif parser == 'artifact':
        artifact(name)
    else:
        raise ValueError(f'{parser} parser is unknown')
