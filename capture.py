import win32gui
import win32ui
import win32con
import numpy as np
import cv2
from get_monitor_data import GetMonitorData


#  ウィンドウのキャプチャを取得する。allは第一引数(window_name)を""に
def WindowCapture(window_name: str, bgr2rgb: bool = False) -> dict:
    # 現在アクティブなウィンドウ名を探す
    process_list = []

    def callback(handle, _):
        process_list.append(win32gui.GetWindowText(handle))

    win32gui.EnumWindows(callback, None)
    # ターゲットウィンドウ名を探す
    hnds = {}
    if window_name == "":
        for process_name in process_list:
            hnd = win32gui.FindWindow(None, process_name)
            hnds[process_name] = hnd

    else:
        for process_name in process_list:
            if window_name in process_name:
                hnd = win32gui.FindWindow(None, process_name)
                break
        else:
            # 見つからなかったら画面全体を取得
            hnd = win32gui.GetDesktopWindow()

        hnds[process_name] = hnd

    imgs_dict = {}
    monitor_dict = GetMonitorData()
    
    for key, hnd in hnds.items():
        # ウィンドウサイズ取得
        x0, y0, x1, y1 = win32gui.GetWindowRect(hnd)

        for m_k, m_v in monitor_dict.items():
            if m_v[0] > 1:
                # このモニターの範囲: m_k[0] =< x < m_k[0] + m_v[1], m_k[1] =< y < m_k[1] + m_v[2]
                if m_k[0] <= x0 <= m_k[0] + m_v[1]:
                    x0 = x0 + (x0 - m_k[0]) * (m_v[0] - 1)
                if m_k[0] + m_v[1] <= x0:
                    x0 = x0 + m_v[1] * (m_v[0] - 1)

                if m_k[0] <= x1 <= m_k[0] + m_v[1]:
                    x1 = x1 + (x1 - m_k[0]) * (m_v[0] - 1)
                if m_k[0] + m_v[1] <= x1:
                    x1 = x1 + m_v[1] * (m_v[0] - 1)

                if m_k[1] <= y0 <= m_k[1] + m_v[2]:
                    y0 = y0 + (y0 - m_k[1]) * (m_v[0] - 1)
                if m_k[1] + m_v[2] <= y0:
                    y0 = y0 + m_v[2] * (m_v[0] - 1)

                if m_k[1] <= y1 <= m_k[1] + m_v[2]:
                    y1 = y1 + (y1 - m_k[1]) * (m_v[0] - 1)
                if m_k[1] + m_v[2] <= y1:
                    y1 = y1 + m_v[2] * (m_v[0] - 1)

        width = x1 - x0
        height = y1 - y0
        if width == 0 or height == 0:
            continue

        # ウィンドウのデバイスコンテキスト取得
        windc = win32gui.GetWindowDC(hnd)
        srcdc = win32ui.CreateDCFromHandle(windc)
        memdc = srcdc.CreateCompatibleDC()
        # デバイスコンテキストからピクセル情報コピー, bmp化
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

        # bmpの書き出し
        if bgr2rgb is True:
            img = np.frombuffer(bmp.GetBitmapBits(True), np.uint8).reshape(height, width, 4)
            img = cv2.cvtColor(img, cv2.COLOR_bgr2rgb)
        else:
            img = np.frombuffer(bmp.GetBitmapBits(True), np.uint8).reshape(height, width, 4)

        #  真っ黒、真っ白かどうか判定。めっちゃ重いかも
        try:
            gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            ret, bw_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
            rev_img = cv2.bitwise_not(bw_image)
            b_count = cv2.countNonZero(rev_img)
            w_count = cv2.countNonZero(bw_image)
            if b_count / rev_img.size < 0.99 and w_count / rev_img.size < 0.99:
                imgs_dict[key] = img

        except SystemError:
            pass

        # 後片付け
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hnd, windc)
        win32gui.DeleteObject(bmp.GetHandle())

    return imgs_dict


# imgs = WindowCapture("")  # 部分一致
# for img in imgs.values():
#     scale = 150 / img.shape[1]
#     img = cv2.resize(img, dsize=None, fx=scale, fy=scale)
#     cv2.imshow("", img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
