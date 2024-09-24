import requests
import json
import zipfile
import re
import os
import geopandas as gpd
import unicodedata


def get_variable_id(subject_id):
    result = []
    data = requests.get(
        'https://bdl.stat.gov.pl/api/v1/variables/search?subject-id=' + subject_id + '&level=2&page=0&page-size=100'
                                                                                     '&format=jsonapi')

    if data.status_code == 200:
        data = json.loads(data.content.decode('utf-8'))
        for item in data['data']:
            tmp = {'variable-id': item['id'],
                   'name': item['attributes']['n1']}
            if 'n2' in item['attributes']:
                tmp['description'] = item['attributes']['n2']
            result.append(tmp)
    return result


def get_variable_data(variable_id, years_list, region_level='2'):
    result = []
    api_years = ''
    for year in years_list:
        api_years += 'year=' + str(year) + '&'

    data = requests.get(
        'https://bdl.stat.gov.pl/api/v1/data/by-variable/' + variable_id + '?' + api_years + 'unit-level=' +
        region_level + '&page=0&page-size=100&format=jsonapi')

    if data.status_code == 200:
        data = json.loads(data.content.decode('utf-8'))
        new_data = data['data']
        for item in new_data:
            tmp = {'name': item['attributes']['name']}
            for value in item['attributes']['values']:
                tmp[f'{value['year']}'] = value['val']
            result.append(tmp)
    return result


def print_list(_list):
    for item in _list:
        print(item)
    print('\n')


def read_zipfile(zip_filename, entry_name):
    with zipfile.ZipFile(zip_filename, mode='r') as zip_file:
        dbf_name = list(filter(lambda x: re.match(entry_name + r'.*\.dbf$', os.path.basename(x)),
                               zip_file.namelist()))[0]
        return gpd.read_file(f'zip://{zip_filename}!/{dbf_name}', encoding='utf-8')


def normalize_text(_text):
    normalized_text = unicodedata.normalize('NFC', _text)
    result = ''.join(c for c in normalized_text if not unicodedata.combining(c))
    return result
