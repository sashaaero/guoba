import requests
import sys
import json
from bs4 import BeautifulSoup
import re


def parse_stat_progression(stat_progression):
    headers = [elem.text for elem in stat_progression.contents[0] if elem.text != 'Ascension']
    size = len(headers)
    levels = []
    for row in stat_progression.contents[1:]:
        row_data = []
        for i in range(size):
            row_data.append(row.contents[i].text)
        levels.append(row_data)

    return headers, levels


def parse_normal(normal):
    matrix = []
    for row in normal.contents[1:]:
        matrix.append([elem.text for elem in row.contents])

    matrix = list(zip(*matrix))
    headers = matrix[0]
    levels = matrix[1:]
    return headers, levels


def main(char_name):
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
    element = element_elem[i+1:j]
    result['main_info']['element'] = element

    weapon_type = soup.find('a', href=re.compile('^/db/weapon/'))
    result['main_info']['weapon'] = weapon_type.contents[0]

    # ------ Talants and Stat ------

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


if __name__ == '__main__':
    main(sys.argv[1])
