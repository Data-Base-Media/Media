import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
tvshows_file = open('tv-shows.txt', 'r')
tvshows_lines = tvshows_file.readlines()

tvshows = {}

# Obtain information using API
for tvshows_line in tqdm(tvshows_lines, desc='Querying MetacriticAPI...', total=len(tvshows_lines)):
    try:
        title, start, end, chanell, genre1, genre2, owner, adaptation = re.findall('(.*) \((\d{4})-(\d{4}), (.+), (.+), (.+), (.+), (.+)\)', tvshows_line)[0]

        query = (
          'query {',
          'tv(input: {',
          f'    title: "{title}",',
          f'    start: "{start}",',
          f'    end: "{end}",',
          f'    chanell: "{chanell}",',
          f'    genre1: "{genre1}",',
          f'    genre2: "{genre2}"',
          f'    owner: "{owner}"',
          f'    adaptation: "{adaptation}"',
          '}) {',
          '    title',
          '    start',
          '    end',
          '    chanell',
          '    genre1',
          '    genre2',
          '    owner',
          '    adaptation',
          '  }',
          '}'
        )

        query = '\n'.join(query)

        response = requests.post(url=url, json={"query": query})
        if response.status_code == 200:
            tvshows[title]=response.json()
    except IndexError:
        # Skip malformed line
        continue

with open('tv-shows.json', 'w') as output_file:
    output_file.write(json.dumps(tvshows))