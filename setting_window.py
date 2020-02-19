import tkinter as tk
from PIL import Image, ImageTk
from capture import WindowCapture
import cv2


class SettingWindow(object):

    def __init__(self, parent):
        self.parent = parent
        self.win = None

    def open(self):
        if not self.win:
            self.win = tk.Toplevel(self.parent)
            self.win.title('Setting-VNT')
            self.setting_icon = Image.open('assets/setting-icon.png')

            # frame1
            self.frame1 = tk.Frame(self.win)
            self.setting_icon = self.setting_icon.resize((15, 15), Image.ANTIALIAS)
            self.setting_ico = ImageTk.PhotoImage(self.setting_icon)
            self.icon = tk.Label(self.frame1, image=self.setting_ico)
            self.icon.grid(row=1, column=1)
            self.text = tk.Label(self.frame1, text='Setting')
            self.text.grid(row=1, column=2)
            self.frame1.grid(row=1)

            # frame2
            self.frame2 = tk.Frame(self.win)
            self.select_win_text = tk.Label(self.frame2, text='Select target window')
            self.select_win_text.grid(row=1, column=1)
            self.edit_box = tk.Entry(self.frame2)
            self.edit_box.grid(row=1, column=2)
            self.scope_button = tk.Button(self.frame2, text="絞り込み")
            self.scope_button.grid(row=1, column=3)
            self.frame2.grid(row=2)

            # frame3
            self.frame3 = tk.Frame(self.win)
            self.imgs_dict = WindowCapture("")
            self.img_index = 0
            self.img_texts: [tk.Label] = []
            self.img_imgs: [tk.Canvas] = []
            self.img_imgtks: [tk.Canvas] = []
            for key, value in self.imgs_dict.items():
                self.scale = 150 / value.shape[1]
                value = cv2.resize(value, dsize=None, fx=self.scale, fy=self.scale)
                self.image_rgb = cv2.cvtColor(value, cv2.COLOR_BGR2RGB)  # imreadはBGRなのでRGBに変換
                self.image_pil = Image.fromarray(self.image_rgb)  # RGBからPILフォーマットへ変換
                self.img_imgtks.append(ImageTk.PhotoImage(self.image_pil))  # ImageTkフォーマットへ変換
                self.image_pil.show()
                if len(key) > 9:
                    key = key[0:8] + '...'
                self.img_imgs.append(tk.Canvas(self.frame3, width=value.shape[0], height=value.shape[1]))  # Canvas作成
                self.img_texts.append(tk.Label(self.frame3, text=key))
                self.img_texts[self.img_index].grid(row=1, column=self.img_index + 1)
                self.img_imgs[self.img_index].grid(row=2, column=self.img_index + 1)
                self.img_imgs[self.img_index].create_image(0, 0, image=self.img_imgtks[self.img_index], anchor='nw')  # ImageTk 画像配置
                self.img_index += 1
            self.frame3.grid(row=3)

            self.win.protocol('WM_DELETE_WINDOW', self.close)
        self.win.focus()

    def close(self):
        self.win.destroy()
        self.win = None
