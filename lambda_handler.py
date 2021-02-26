#envio para data stream

import requests
import json
from datetime import datetime
import boto3

currentDate = datetime.now()
currentTime = str(datetime.now().time())
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
    hour = hour[:2]
    minute = "00"
    return hour + minute

def crtDict(fData):
    for item in fData:
        myDict = {
            'DC_NOME': item['DC_NOME'],
            'TEMP': item['TEM_INS'],
            'UMD': item['UMD_INS']
        }
        dict.append(myDict)

def lambda_handler(event, context, data):
    date = getDate(currentDate)
    hour = str(getHour(currentTime))
    response = gResponse(date, hour)

    if (response.status_code == 200):
        fData = filter(response)
        crtDict(fData)
        print(dict)

    return {
        'statusCode': 200,
        'body': json.dumps(dict)
    }

def sendKinesis(data):
    cKinesis = boto3.client("kinesis", "us-east-1")
    cKinesis.put_records(
        Records=[{
            'Data': json.dumps({"message_type": data}),
            'PartitionKey': 'key'
        }],
        StreamName="kinesis-stream")
    return {
        'statusCode': 200,
        'body': json.dumps('Successful')
    }