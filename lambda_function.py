import json
import base64
import requests

#envio para thingsboard

dir = {}

def sendBase(dir):
    access_token = " "
    baseUrl = f'https://demo.thingsboard.io/api/v1/{access_token}/telemetry'
    requests.post(baseUrl, data=json.dumps(dir))

def getData(event):
    dataRecords = event.get('Records')
    for i in dataRecords:
        data = i['kinesis']['data']
        message = json.loads(base64.b64decode(data))
        local = message['DC_NOME']
        hi = message['HEAT_INDEX']
        if (hi != None):
            index = getIndexValue(hi)
            dir[local] = str(hi), index
        else:
           print("Índice de calor não encontrado para " + local)

    print(dir)
    sendBase(dir)

def getIndexValue(hi):
    if hi <= 27:
        return "Normal"
    elif hi > 27 or hi <= 32:
        return "Cautela"
    elif hi > 32 or hi <= 41:
        return "Cautela extrema"
    elif hi > 41 or hi <= 54:
        return  "Perigo"
    elif hi > 54:
        return "Perigo extremo"


def lambda_handler(event, context):
    getData(event)
    return {
        'statusCode': 200,
        'body': json.dumps(dir)
    }