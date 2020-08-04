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

    beep_connect()

    error_thread = threading.Thread(
        target = box.changeMsg,
        args = ("【Error】","Touch it Again!")
    )

    try:
        id_data = tag.read_without_encryption([sc], [bc0])
    except Exception:
        print("touch it again")
        beep_error()
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
            beep_success()
            success_thread.start()
        else:
            beep_error()
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

def beep_connect():
    winsound.Beep(1567,300)
def beep_success():
    winsound.Beep(2093,300)
def beep_error():
    winsound.Beep(1000,120)
    winsound.Beep(880,120)

if __name__ == '__main__':
    main()
