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
    full_name = soup.find('div', {'class': ['custom_title']}).text
    result['main_info']['full_name'] = full_name

    element_img = soup.find('img', {'class': ['char_portrait_card_sea_element']})
    element_elem = element_img.attrs['data-src']
    i = element_elem.rfind('/')
    j = element_elem.find('_', i)
    element = element_elem[i+1:j]
    result['main_info']['element'] = element

    live_data = soup.find('div', {'id': 'live_data'})
    span_stats = live_data.find_all('div', {'class': ['skilldmgwrapper']})

    headers, levels = parse_stat_progression(span_stats[0].next)
    result['stat_progression']['headers'] = headers
    result['stat_progression']['levels'] = levels

    headers, levels = parse_normal(span_stats[1].next)
    result['normal']['headers'] = headers
    result['normal']['levels'] = levels

    headers, levels = parse_normal(span_stats[2].next)
    result['skill']['headers'] = headers
    result['skill']['levels'] = levels

    headers, levels = parse_normal(span_stats[3].next)
    result['burst']['headers'] = headers
    result['burst']['levels'] = levels

    with open(f'{char_name}.json', 'w') as file:
        file.write(json.dumps(result, indent=2))


if __name__ == '__main__':
    main(sys.argv[1])
