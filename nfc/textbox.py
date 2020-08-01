from tkinter import *
import time

class TextBox():
    def __init__(self):
        self.box = Tk()
        self.box.protocol("WM_DELETE_WINDOW", self.box.destroy)

        # 初期表示設定
        self.box.title(u"Lab Attendency")
        ww=self.box.winfo_screenwidth()
        wh=self.box.winfo_screenheight()
        lw = 400
        lh = 170
        self.box.geometry(str(lw) + "x" + str(lh) + "+" + str(int(ww/2-lw/2)) + "+" + str(int(wh-lh)))
        self.text = StringVar()
        self.label1 = Label(self.box, text = "Touch your Card", font = ("Arial",30))
        self.label1.pack()
        self.label2 = Label(self.box, text = "", font = ("Arial",20))
        self.label2.pack()

        self.box.update_idletasks()

    # メッセージボックスの作成、無限ループ
    def start(self, thread):
        self.box.after(100, thread)
        self.box.mainloop()

    # デフォルトメッセージの表示
    def defaultMsg(self):
        self.label1["text"] = "Touch your Card"
        self.label2["text"] = ""
        self.box.update_idletasks()

    # 引数に入っているメッセージを表示
    def changeMsg(self, *args):
        # メッセージ文(1行目)
        self.label1["text"] = str(args[0])
        # メッセージ文(2行目)・読み取った番号を格納する想定
        if len(args) == 2:
            self.label2["text"] = str(args[1])
        self.box.update_idletasks()

        # 1秒後にデフォルトメッセージに戻す
        time.sleep(1)
        self.defaultMsg()

    def quit(self):
        self.box.quit()

    def destroy(self):
        self.box.destroy()

