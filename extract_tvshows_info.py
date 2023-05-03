import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
tvshow_file = open('tv-shows.txt', 'r')
tvshow_lines = tvshow_file.readlines()

tvshow = {}

# Obtain information using API
for tvshow_line in tvshow_lines:
    
    try:
        # split the string into its components
        title, info = tvshow_line.split(" (")
        info = info[:-2]  # remove the closing parenthesis
        
        # extract the relevant information from the components
        elements = info.split(", ")
        
        # create a dictionary with the extracted information
        show = {
            "year": elements[0],
            "network": elements[1],
            "genre": elements[2],
            "owner": elements[3],
            "mode": elements[4]
        }

        # add the dictionary to a main dictionary
        tvshow[title] = {"data": {"show": show}}

    except IndexError:
        # skip malformed line
        continue

with open('tv-shows.json', 'w') as output_file:
    output_file.write(json.dumps(tvshow))