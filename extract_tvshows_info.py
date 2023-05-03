import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
shows_file = open('tv-shows.txt', 'r')
shows_lines = shows_file.readlines()

shows = {}
elementos = []

for show_line in shows_lines:
    if (show_line[0] != '"'):
        try:
        
            info = show_line.split(", ")

            titulo, ano = info[0].split("(")
            network = info[1].strip()

            titulo = titulo.strip()
            ano = ano.strip(")")

            adaptation = "Original"
            if info[-1].strip().endswith("Adaptation)"):
                generos = [genero.strip() for genero in info[2:-3]]
                produtora = info[-3].strip()
                classificacao = info[-2].strip()
                if info[-1].strip().endswith("Book Adaptation)"):
                    adaptation = "Based on a book"
                if info[-1].strip().endswith("Comic Book Adaptation)"):
                    adaptation = "Based on a comic book"
                if info[-1].strip().endswith("Film Adaptation)"):
                    adaptation = "Based on a movie"
            else:
                generos = [genero.strip() for genero in info[2:-2]]
                produtora = info[-2].strip()
                classificacao = info[-1].strip()
                classificacao = classificacao.strip(")")
        except IndexError:
            # Skip malformed line
            continue
        nova_string = f'"{titulo}" ({ano}) - {network} - {produtora} - {", ".join(generos)} - {classificacao} - {adaptation}'
        
    else:
        info = show_line.split(" - ")
        titulo_ano = info[0]
        produtora = info[1]
        genero = info[2]
        classificacao = info[3]
        adaptation = info[4].strip()
        if adaptation == "Not a book adaptation":
            adaptation = "Original"
        titulo, ano = titulo_ano[1:-1].split(" (")
        network = "None"

        nova_string = f'"{titulo}" ({ano}) - {network} - {produtora} - {genero} - {classificacao} - {adaptation}'
    elementos.append(nova_string)

# Obtain information using API
for show_line in elementos:
    lista = show_line.split(" - ")
    titulo_ano = lista[0]
    titulo, ano = titulo_ano.split(" (")
    titulo = titulo.replace('"', '')
    ano = ano.strip(")").split("-")
    try:
        # criar um dicionário com as informações obtidas
        show = {
            "title": titulo,
            "year": "-".join(ano),
            "network": lista[1],
            "studio": lista[2],
            "genre": lista[3],
            "rating": lista[4],
            "adaptation": lista[5]
        }
        
        if titulo not in shows:
            # adicionar o dicionário ao dicionário principal
            shows[titulo] = {"data": {"tv-show": show}}

    except IndexError:
        # Skip malformed line
        continue

with open('tv-shows.json', 'w') as output_file:
    output_file.write(json.dumps(shows))
