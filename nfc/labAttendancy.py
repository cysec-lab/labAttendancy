import nfc
import requests
import json

import config

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

# 学籍番号が格納されているサービスコード
service_code = 0x1a8b

def on_connect(tag):
    print(tag)

    idm, pmm = tag.polling(system_code=0xfe00)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xfe00

    sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
    bc0 = nfc.tag.tt3.BlockCode(0, service=0)
    try:
        id_data = tag.read_without_encryption([sc], [bc0])
        id = id_data[2:13].decode("utf-8")
        print("Student Num: " + id)
    except:
        print("touch it again")

    return True

def on_release(tag):
    pass


def main():
    try:
        with nfc.ContactlessFrontend('usb') as clf:
            while clf.connect(rdwr={
                'on-connect': on_connect,
                'on-release': on_release,
            }):
                pass
    except IOError:
        print("NFCリーダーの接続Error")
        sys.exit(0)

if __name__ == '__main__':
    main()
