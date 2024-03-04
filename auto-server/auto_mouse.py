import win32gui
import win32api
import win32con
import window

class Mouse(object):
    def MoveAndClick(self, pos: window.Pos, hWnd: int):
        # 点击的位置(屏幕坐标)
        (click_x, click_y) = (pos.x, pos.y)
        # 屏幕坐标转窗口内坐标
        click_pos_in_window =win32gui.ScreenToClient(hWnd,(click_x, click_y))
        print("click", click_pos_in_window[0], click_pos_in_window[1])
        # api函数入参是一个值，需要将(x, y)坐标从x int、y int转换为一个long型值，即二进制值拼接。
        click_pos_in_window_long = win32api.MAKELONG(click_pos_in_window[0], click_pos_in_window[1])
        # 激活鼠标
        win32gui.SendMessage(hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        # 按下鼠标
        win32gui.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, click_pos_in_window_long)
        # 抬起鼠标
        win32gui.SendMessage(hWnd, win32con.WM_LBUTTONUP, 0000, click_pos_in_window_long)
    pass




