# -*- coding: gb2312 -*-

from win32con import SECURITY_CREATOR_GROUP_RID
import window
import auto_mouse
import globals
import ip_addr

class Process(object):
    pass # class: Process

def wechat_login():
    # 获取微信进程的信息。
    wechat_window = window.Window(window_class_name='WeChatLoginWndForPC', window_name='微信')
    print("wechat window position =", wechat_window.window_left_top.x, wechat_window.window_left_top.y, wechat_window.window_right_bottom.x, wechat_window.window_right_bottom.y)
    print("wechat window hwnd =", wechat_window.hWnd)
    # 初始化一个鼠标结构体
    mouse = auto_mouse.Mouse()
    # TODO: screen_scale，屏幕缩放比例
    # 实测不需要进行屏幕缩放比例的调整
    screen_scale = window.get_screen_scale_factor()
    screen_scale = globals.global_params.default_screen_scale

    # 登陆微信按钮的位置信息，该位置信息是相对于窗口左上角的位置信息。
    # 例如微信按钮的位置为：140, 300表示从左上角开始+140，左上角+300则是按钮位置。
    login_pos = window.Pos(int((wechat_window.window_right_bottom.x - wechat_window.window_left_top.x) / 2 * screen_scale), int((wechat_window.window_right_bottom.y - wechat_window.window_left_top.y) / 5 * 4 * screen_scale))
    print("login position =", login_pos.x, login_pos.y)
    click_pos = window.Pos(int(login_pos.x + wechat_window.window_left_top.x), int(login_pos.y + wechat_window.window_left_top.y))
    # 鼠标点击
    #mouse.MoveAndClick(click_pos, wechat_window.hWnd)
    pass # function: wechat_login
