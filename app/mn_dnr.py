import re
import sys
import json
import requests
import properties
from functools import partial
import multiprocessing

def compile_lake_list():
    fish_id_lookup_url = properties.fish_id_lookup_url
    county_id_lookup_url = properties.county_id_lookup_url
    lake_id_lookup_url = properties.lake_id_lookup_url
    lake_info_url = properties.lake_info_url
    lake_id_list = []

    fish_species_json = get_fish_id(fish_id_lookup_url)
    print(f'Completed lookup for {len(fish_species_json)} fish species')

    county_json = get_county_list(county_id_lookup_url)
    print(f'Found {len(county_json)} counties')

    for county_name in county_json:
        county_id = county_json[county_name]
        print (f'Working on county: {county_name}')

        try:
            county_lake_id_lookup_url = (f'{lake_id_lookup_url}{county_id}')
            lake_id_list = get_lake_id_list(county_lake_id_lookup_url, lake_id_list)
        except:
            print (f'No results for county: {county_name}')
            pass

    print(f'Found {len(lake_id_list)} lakes for all counties')
    lake_list = threaded_get_lake_info(lake_id_list, lake_info_url, fish_species_json)

    return lake_list

def get_fish_id(url):
    '''
    Gather a json-ish list of fish
    This is used to translate abbreviations to common names
    '''
    fish_species_json = {}
    result = get_api_call(url)

    for line in result.split('\n'):
        if re.match('var fish_species.*', line):
            fish_species_results = line.split('var fish_species = ')[1].split(';')[0]
            fish_species_json = json.loads(fish_species_results)

    return fish_species_json

def get_county_list(url):
    '''
    Gather a list of available counties
    '''

    county_dictionary = {}

    result = get_api_call(url)
    json_result = json.loads(result)

    for county in json_result['results']:
        county_id = county['id']
        county_name = county['county']
        county_dictionary[county_name] = county_id

    return county_dictionary

def get_lake_id_list(url, lake_id_list):
    '''
    Gather a list of lakes
    Build out a json-ish format
    '''

    result = get_api_call(url)
    json_result = json.loads(result)

    for index, lake_item in enumerate(json_result['results']):
        lake_dictionary = {}
        lake_id = lake_item['id'].strip()
        lake_name = lake_item['name'].strip()
        county_name = lake_item['county'].strip()
        nearest_town = lake_item['nearest_town'].strip()
        lake_dictionary['lake_id'] = lake_id
        lake_dictionary['lake_name'] = lake_name
        lake_dictionary['county_name'] = county_name
        lake_dictionary['nearest_town'] = nearest_town
        lake_id_list.append(lake_dictionary)

    return lake_id_list

def threaded_get_lake_info(lake_id_list, lake_info_url, fish_species_json):
    '''
    Threaded calls for lake survey lookups
    By far the most time consuming part of
    running this app
    '''

    number_of_threads = properties.number_of_threads
    new_lake_id_list = []
    lake_id_list = sorted(lake_id_list, key=lambda k: k['lake_name'])

    pool = multiprocessing.Pool(number_of_threads)
    func = partial(get_lake_info, lake_info_url, fish_species_json, lake_id_list, new_lake_id_list)
    new_lake_id_list = pool.map(func, enumerate(lake_id_list), chunksize=1)
    pool.close()
    pool.join()

    return new_lake_id_list

def get_lake_info(url, fish_species_json, lake_id_list, new_lake_id_list, lake_dictionary_index_tuple):
    '''
    Given a list of lakes, gather survey info
    around species and counts by length
    '''

    index, lake_dictionary = lake_dictionary_index_tuple
    index = index + 1
    fish_species_list = []
    lake_id = lake_dictionary['lake_id']
    lake_name = lake_dictionary['lake_name']
    if lake_name != 'Unnamed':
        print(f'Working on lake id [ {index} ] of [ {len(lake_id_list)} ]: {lake_name}')
    else:
        print(f'No surveys found for lake id [ {index} ] of [ {len(lake_id_list)} ]: {lake_id}')

    lake_id_url = (f'{url}{lake_id}')
    result = get_api_call(lake_id_url)
    json_result = json.loads(result)
    try:
        most_recent_survey = json_result['result']['surveys'][-1]
        survey_date = most_recent_survey['surveyDate']
        lake_dictionary['survey_date'] = survey_date
        for fish_species in most_recent_survey['lengths']:
            fish_species_dictionary = {}
            fish_species_catch_list = []
            fish_catch_total_count = 0
            fish_species_name = fish_species_json[fish_species]['common_name']
            fish_species_dictionary['species_name'] = fish_species_name
            for fish_length_count in most_recent_survey['lengths'][fish_species]['fishCount']:
                fish_species_catch_dictionary = {}
                fish_species_catch_dictionary['fish_length'] = fish_length_count[0]
                fish_species_catch_dictionary['fish_count'] = fish_length_count[1]
                fish_catch_total_count = fish_catch_total_count + fish_length_count[1]
                fish_species_catch_list.append(fish_species_catch_dictionary)
            fish_species_dictionary['catches'] = fish_species_catch_list
            fish_species_dictionary['total_catch_count'] = fish_catch_total_count
            fish_species_list.append(fish_species_dictionary)
            lake_dictionary['species'] = fish_species_list
        new_lake_id_list.append(lake_dictionary)
    except:
        new_lake_id_list.append(lake_dictionary)
        pass

    return new_lake_id_list

def get_api_call(url):
    '''
    Makes a HTTP get call
    '''
    response = requests.get(url)
    return response.text