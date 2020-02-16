import tkinter
from PIL import Image, ImageTk
import setting_window

# 画面作成
tki = tkinter.Tk()
tki.geometry('193x65')
iconfile = 'assets/favicon.ico'
tki.title('VNT')
tki.iconbitmap(default=iconfile)
tki.resizable(0, 0)

# # ラベル
# lbl_1 = tkinter.Label(text='10進数')
# lbl_1.place(x=30, y=70)
# lbl_2 = tkinter.Label(text='16進数')
# lbl_2.place(x=30, y=100)

# # テキストボックス
# txt_1 = tkinter.Entry(width=20)
# txt_1.place(x=90, y=70)
# txt_2 = tkinter.Entry(width=20)
# txt_2.place(x=90, y=100)


# clickイベント
def btn_click():
    settingwindow = setting_window.SettingWindow(tki)
    # settingwindow.open()
    menu = tkinter.Menu(tki)
    menu.add_command(label='Setting', command=settingwindow.open)
    tki.config(menu=menu)


setting_icon = Image.open('assets/setting-icon.png')
setting_icon = setting_icon.resize((40, 40), Image.ANTIALIAS)
setting_ico = ImageTk.PhotoImage(setting_icon)
settingwindow = setting_window.SettingWindow(tki)
setting_btn = tkinter.Button(
    tki,
    text='setting',
    command=settingwindow.open,
    compound=tkinter.TOP,
    image=setting_ico
)
setting_btn.grid(row=1, column=1)

camera_icon = Image.open('assets/camera-icon.png')
camera_icon = camera_icon.resize((40, 40), Image.ANTIALIAS)
camera_ico = ImageTk.PhotoImage(camera_icon)
# ボタン
camera_btn = tkinter.Button(
    tki,
    text='capture',
    compound=tkinter.TOP,
    image=camera_ico
)
camera_btn.grid(row=1, column=2)

record_icon = Image.open('assets/video-icon.png')
record_icon = record_icon.resize((40, 40), Image.ANTIALIAS)
record_ico = ImageTk.PhotoImage(record_icon)
# ボタン
record_btn = tkinter.Button(
    tki,
    text='record',
    compound=tkinter.TOP,
    image=record_ico
)
record_btn.grid(row=1, column=3)

voice_icon = Image.open('assets/voice-icon.png')
voice_icon = voice_icon.resize((40, 40), Image.ANTIALIAS)
voice_ico = ImageTk.PhotoImage(voice_icon)
# ボタン
voice_btn = tkinter.Button(
    tki,
    text='read',
    compound=tkinter.TOP,
    image=voice_ico
)
voice_btn.grid(row=1, column=4)

# 画面をそのまま表示
tki.mainloop()
