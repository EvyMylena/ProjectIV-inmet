#envio para data stream

import requests
import json
from datetime import datetime

currentTime = datetime.now()
dict = []

def filter(response):
    filterData = response.json()
    filter = [x for x in filterData if x["UF"] == "PE"]
    return filter

def gResponse(date, hour):
    response = requests.get(f'https://apitempo.inmet.gov.br/estacao/dados/{date}/{hour}')
    return response

def getDate(date):
    return currentTime.date()

def getHour(hour):
    hour = currentTime.hour - 3
    minute = currentTime.minute
    return (hour, (":"), minute)

def crtDict(fData):
    for item in fData:
        myDict = {
            'DC_NOME': item['DC_NOME'],
            'TEMP': item['TEMP_INS'],
            'UMD': item['UMD_INS'],
            'TEM_MIN': item['TEMP_MIN'],
            'TEM_MAX': item['TEMP_MAX']
        }
        dict.append(myDict)

def lambda_handler(event, context):
    response = gResponse()
    date = getDate()
    hour = getHour()

    if (response.status_code == 200):
        fData = filter(response)
        crtDict(fData)
        print(dict)

    return {
        'statusCode': 200,
        'body': json.dumps(dict)
    }

