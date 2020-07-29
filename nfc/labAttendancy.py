import nfc
import requests
import json
from tkinter import *
import time

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
    except Exception:
        print("touch it again")
    else:
        id = id_data[2:13].decode("utf-8")
        print("Student Num: " + id)
        postData(id)
        msg_info(id)
    return True
    
# 画面中央にタッチされた学生証番号を1秒メッセージボックスで表示する
# ボックスの生存期間設定: https://living-sun.com/ja/python-3x/683869-python-3-closing-window-on-tkinter-python-3x-tkinter.html
def msg_info(id):
    box = Tk()

    # ボックス表示内容の設定
    box.title(u"Lab Attendency")
    Label1 = Label(box, text = "Read Successful!", font = ("Arial",30))
    Label1.pack()
    Label2 = Label(box, text = str(id), font = ("Arial", 20))
    Label2.pack()
    box.update_idletasks()

    # ボックス表示位置の設定
    ww=box.winfo_screenwidth()
    lw=box.winfo_width()
    wh=box.winfo_screenheight()
    lh=box.winfo_height()
    box.geometry(str(lw) + "x" + str(lh) + "+" + str(int(ww/2-lw/2)) + "+" + str(int(wh/2-lh/2)))

    # ボックスの生存期間を設定(秒数[ms])
    box.after(1000, box.destroy)
    box.mainloop()
    return


def msg_error():
    box = Tk()
    box.title(u"Lab Attendency")
    Label1 = Label(box, text = "Touch It Again!", font = ("Arial", 30), fg = "#ff0000", bg = "#000000")
    Label1.pack()
    box.update_idletasks()

    ww=box.winfo_screenwidth()
    lw=box.winfo_width()
    wh=box.winfo_screenheight()
    lh=box.winfo_height()
    box.geometry(str(lw) + "x" + str(lh) + "+" + str(int(ww/2-lw/2)) + "+" + str(int(wh/2-lh/2)))

    box.after(1500, box.destroy) #秒数[ms]
    box.mainloop()
    return

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
