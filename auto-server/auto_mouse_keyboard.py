# -*- coding: gb2312 -*-

import win32gui
import win32api
import win32con
import window

class Mouse(object):
    def MoveAndClick(self, pos: window.Pos, hWnd: int):
        '''
        ���: 
            pos: ���λ��������ϵͳ��Ļ�����x��y���꣬ΪPos�ṹ��
            hWnd: ���ھ��
        '''
        # �����λ��(��Ļ����)
        (click_x, click_y) = (pos.x, pos.y)
        # ��Ļ����ת����������
        click_pos_in_window =win32gui.ScreenToClient(hWnd,(click_x, click_y))
        print("click", click_pos_in_window[0], click_pos_in_window[1])
        # api���������һ��ֵ����Ҫ��(x, y)�����x int��y intת��Ϊһ��long��ֵ����������ֵƴ�ӡ�
        click_pos_in_window_long = win32api.MAKELONG(click_pos_in_window[0], click_pos_in_window[1])
        # �������
        win32gui.SendMessage(hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        # �������
        win32gui.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, click_pos_in_window_long)
        # ̧�����
        win32gui.SendMessage(hWnd, win32con.WM_LBUTTONUP, 0000, click_pos_in_window_long)
    pass # class Mouse

class Keyboard(object):
    def tap(self, message: str, hWnd: int) -> None:
        print("send message:", message)
        for s in message.encode():
            win32gui.SendMessage(hWnd, win32con.WM_CHAR, s, 0)
            pass # for x in string
        pass # function tap
    
    def tap_enter(self, hWnd: int) -> None:
        win32gui.PostMessage(hWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(hWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        pass # function new_line
    pass # class Keyboard


