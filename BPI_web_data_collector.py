import requests
import json
import pandas as pd
import re

# BPI Web API
# http://site.api.espn.com/apis/fitt/v3/sports/basketball/mens-college-basketball/powerindex?lang=en&region=us&season={year}&sort=bpi.bpi%3Adesc&groups=50&limit=50&page={page}
# max page = 5
# max limit = 50
# max groups = 50

bpi_data = {'YEAR':[], 'TEAM':[], 'BPI':[]}

for year in range(2008, 2024):
    print(f'Collecting data for {year}.')
    i = 1
    while True:
        print(f'\tCollecting data for page {i}.')
        url = f'http://site.api.espn.com/apis/fitt/v3/sports/basketball/mens-college-basketball/powerindex?lang=en&region=us&season={year}&sort=bpi.bpi%3Adesc&groups=50&limit=50&page={i}'
        i += 1
        response = requests.get(url)
        if response.status_code != 200:
            print(f'\t\tError: {response.status_code}')
            break
        data = json.loads(response.text)
        for team in data['teams']:
            bpi_data['YEAR'].append(year)
            bpi_data['TEAM'].append(team['team']['shortDisplayName'])
            bpi_data['BPI'].append(team['categories'][0]['totals'][0])

bpi_data_frame = pd.DataFrame(bpi_data, columns=['YEAR', 'TEAM', 'BPI'])
bpi_data_frame.to_csv('march-madness-data/new_bpi_data.csv', index=False)