import requests
import json

response = requests.get(f'https://apitempo.inmet.gov.br/estacao/dados/2021-02-22/2200')
js = response.json()

filter = [x for x in js if x["UF"] == "PE"]

print(filter)