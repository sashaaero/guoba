import requests
import sys
import json
from bs4 import BeautifulSoup
import re


def parse_value(value: str) -> object:
    if '+' in value:
        return [parse_value(v) for v in value.split('+')]

    val = value.replace('HP', '')

    if val.endswith('%'):
        return float(val[:-1]) / 100

    return int(val)


def parse_skills(value:str):
    return


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
    live_data = soup.find('div', {'id': 'live_data'})

    # --- stats ---

    span_stats = live_data.find('span', {'id': 'scroll_stat'})
    table_stats = span_stats.next_sibling.next
    header_element = table_stats.contents[0]
    print(header_element)
    data_elements = table_stats.contents[1:]
    headers = [elem.text for elem in header_element.contents if elem.text != 'Ascension']
    levels = []
    for level in data_elements:

        stats = [level.contents[0].text]

        for i in range(1, len(headers)):
            elem = level.contents[i]

            stats.append(parse_value(elem.text))

        levels.append(stats)

    result['stat_progression']['headers'] = headers
    result['stat_progression']['levels'] = levels

    # --- talents --
    span_stats = live_data.find_all('div', {'class': ['skilldmgwrapper']})
    for content in span_stats:
        for level in content:
            #print([elem.text for elem in level.contents])
            for elem in level.contents:
                print(elem.contents[2])
            #print([level.contents.text])
            #print(soup.find_all(r'<td>(.+?)</td>', level.contents[1]))


            #headers = [elem.text for elem in level.contents]

    pass

    with open(f'{char_name}.json', 'w') as file:
        file.write(json.dumps(result, indent=2))


if __name__ == '__main__':
    main('xinyan')
    #main(sys.argv[1])
