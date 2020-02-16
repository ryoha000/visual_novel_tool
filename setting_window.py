import tkinter as tk
from PIL import Image, ImageTk


class SettingWindow(object):

    def __init__(self, parent):
        self.parent = parent
        self.win = None

    def open(self):
        if not self.win:
            self.win = tk.Toplevel(self.parent)
            self.win.title('Setting-VNT')
            self.setting_icon = Image.open('assets/setting-icon.png')
            self.setting_icon = self.setting_icon.resize((15, 15), Image.ANTIALIAS)
            self.setting_ico = ImageTk.PhotoImage(self.setting_icon)
            self.icon = tk.Label(self.win, image=self.setting_ico)
            self.icon.grid(row=1, column=1)
            self.text = tk.Label(self.win, text='Setting')
            self.text.grid(row=1, column=2)
            self.win.protocol('WM_DELETE_WINDOW', self.close)
        self.win.focus()

    def close(self):
        self.win.destroy()
        self.win = None
