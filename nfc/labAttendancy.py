import nfc
import threading

import post
import textbox

import winsound

# 学籍番号が格納されているサービスコード
service_code = 0x1a8b

# NFCがリーダに触れた際に実行される
# - カードの読み取り
# - メッセージボックスの更新
# - POST
def on_connect(tag):
    idm, pmm = tag.polling(system_code=0xfe00)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xfe00

    sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
    bc0 = nfc.tag.tt3.BlockCode(0, service=0)

    beep(1567,300)

    error_thread = threading.Thread(
        target = box.changeMsg,
        args = ("【Error】","Touch it Again!")
    )

    try:
        id_data = tag.read_without_encryption([sc], [bc0])
    except Exception:
        print("touch it again")
        beep(1000,130,880,130)
        error_thread.start()
    else:
        id = id_data[2:13].decode("utf-8")
        print("Student Num: " + id)
        message_thread = threading.Thread(
            target = box.defaultMsg,
            args = ("Posting...", id)
        )
        message_thread.start()
        suc = post.postData(id)
        if suc:
            success_thread = threading.Thread(
                target = box.changeMsg,
                args = ("Post Success", id)
            )
            beep(2093,300)
            success_thread.start()
        else:
            beep(1000,120,880,120)
            error_thread.start()
    return True

# NFCがリーダから離れた際に実行される
def on_release(tag):
    return True

def main():
    # メッセージボックスの作成
    global box
    box = textbox.TextBox()

    # サブスレッド動作フラグ
    running = True

    # NFCリーダの設定と読み取り動作
    def read_nfc():
        try:
            with nfc.ContactlessFrontend('usb') as clf:
                while 1:
                    try:
                        while clf.connect(rdwr={
                            'on-connect': on_connect,
                            'on-release': on_release,
                        }):
                            if (running == False):
                                # GUIが終了していた場合にread_nfc()をとめる
                                return
                    except nfc.tag.tt3.Type3TagCommandError:
                        # NFCが触れる時間が短かった際に発生するエラー
                        error_thread = threading.Thread(
                            target = box.changeMsg,
                            args = ("【Error】","Touch it Again!")
                        )
                        error_thread.start()
        except IOError:
            print("NFCが接続されていません")
            box.quit()
            return

    # 画面を表示したのちにNFCリーダをサブスレッドとして動かす
    thread = threading.Thread(target=read_nfc)
    thread.setDaemon(True)
    box.start(thread.start)

    # サブスレッド終了処理
    running = False
    thread.join()

def beep(*args):
    """
    Usage:
    args[i] = Hz, args[i+1] = ms (i = odd)
    args[i+2] = Hz, args[i+3] ms ...
    """
    if len(args) % 2 != 0 :
        # argument error
        return -1
    else:
        for i in range(0,int(len(args)),2):
            try:
                winsound.Beep(int(args[i]),int(args[i+1]))
            except RuntimeError:
                print(RuntimeError)
                break
    return

def beep(*args):
    for i in len(args):
        winsound.Beep(args[i-1],300/i) 

if __name__ == '__main__':
    main()
