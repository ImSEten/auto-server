# -*- coding: gb2312 -*-

from win32con import SECURITY_CREATOR_GROUP_RID
import window
import auto_mouse
import globals
import ip_addr

class Process(object):
    pass # class: Process

def wechat_login():
    # ��ȡ΢�Ž��̵���Ϣ��
    wechat_window = window.Window(window_class_name='WeChatLoginWndForPC', window_name='΢��')
    print("wechat window position =", wechat_window.window_left_top.x, wechat_window.window_left_top.y, wechat_window.window_right_bottom.x, wechat_window.window_right_bottom.y)
    print("wechat window hwnd =", wechat_window.hWnd)
    # ��ʼ��һ�����ṹ��
    mouse = auto_mouse.Mouse()
    # TODO: screen_scale����Ļ���ű���
    # ʵ�ⲻ��Ҫ������Ļ���ű����ĵ���
    screen_scale = window.get_screen_scale_factor()
    screen_scale = globals.global_params.default_screen_scale

    # ��½΢�Ű�ť��λ����Ϣ����λ����Ϣ������ڴ������Ͻǵ�λ����Ϣ��
    # ����΢�Ű�ť��λ��Ϊ��140, 300��ʾ�����Ͻǿ�ʼ+140�����Ͻ�+300���ǰ�ťλ�á�
    login_pos = window.Pos(int((wechat_window.window_right_bottom.x - wechat_window.window_left_top.x) / 2 * screen_scale), int((wechat_window.window_right_bottom.y - wechat_window.window_left_top.y) / 5 * 4 * screen_scale))
    print("login position =", login_pos.x, login_pos.y)
    click_pos = window.Pos(int(login_pos.x + wechat_window.window_left_top.x), int(login_pos.y + wechat_window.window_left_top.y))
    # �����
    #mouse.MoveAndClick(click_pos, wechat_window.hWnd)
    pass # function: wechat_login
