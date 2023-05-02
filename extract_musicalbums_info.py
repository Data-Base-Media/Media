import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
albums_file = open('albums.txt', 'r')
albums_lines = albums_file.readlines()

albums = {}

# Obtain information using API
for album_line in tqdm(albums_lines, desc='Querying MetacriticAPI...', total=len(albums_lines)):
    try:
        title, artist, genre, year, label, sales = re.findall('(.*) - (.*) \((.*)\) - (\d{4}) - (.*) - (.*)', album_line)[0]

        query = (
          'query {',
          '  album(input: {',
          f'    title: "{title}",',
          f'    artist: "{artist}",',
          f'    genre: "{genre}",',
          f'    year: "{year}",',
          f'    label: "{label}",',
          f'    sales: "{sales}"',
          '  }) {',
              '  title',
              '  artist',
              '  criticScore',
              '  userScore',
              '  year',
              '  genres',
              '  label',
              '  numOfCriticReviews',
              '  numOfUserReviews',
          '  }',
          '}'
        )

        query = '\n'.join(query)

        response = requests.post(url=url, json={"query": query})
        if response.status_code == 200:
            albums.append(response.json())
    except IndexError:
        # Skip malformed line
        continue

with open('albums.json', 'w') as output_file:
    output_file.write(json.dumps(albums))
