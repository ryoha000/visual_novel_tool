from screeninfo import get_monitors
import win32api


def GetMonitorData() -> dict:
    list_monitor = win32api.EnumDisplayMonitors()
    correct_monitors = {}
    real_monitors = {}
    monitor_scales = {}
    stretch_count = 0
    while stretch_count < 100:
        # 環境によって?失敗するため最大100回まわしてる
        if len(correct_monitors) > 0:
            # print(stretch_count)  # 試行回数
            break
        stretch_count += 1
        for m in get_monitors():
            correct_monitors[(m.x, m.y)] = (m.width, m.height)

    for m in list_monitor:
        # こっちはwidth, heightじゃなくて終点の座標がvalue
        real_monitors[(m[2][0], m[2][1])] = (abs(m[2][0] + m[2][2]), abs(m[2][1] + m[2][3]))

    for cm_k, cm_v in correct_monitors.items():
        # compare with width
        try:
            scale = cm_v[0] / real_monitors[cm_k][0]
            monitor_scales[(cm_k)] = (
                scale, real_monitors[cm_k][0], real_monitors[cm_k][1]
            )
        except KeyError and ZeroDivisionError as e:
            print("error2")
            print(e)
            monitor_scales[(cm_k)] = (
                1, cm_v[0], cm_v[1]
            )
            pass
        
    return monitor_scales
