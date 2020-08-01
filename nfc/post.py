import requests
import json

import config

# 学生証番号を config.py に指定されたURLにPOSTする
def postData(data):
    if(data is None):
        print("params is empty")
        return False

    payload = {
        "data": data
    }
    url = config.url
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if(response.status_code == 200 and response.text == "success"):
        print("post success!")
        return True
    print(response.text)
    return False