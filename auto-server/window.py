# -*- coding: gb2312 -*-

import win32api
import win32con
import win32gui
import win32ui
import global_params

# PosΪλ���࣬��ʾ����λ����Ϣ
class Pos(object):
    def __init__(self, x: int, y: int) -> None:
        '''
        ��Ա:
            x: ����λ�õ�x����
            y: ����λ�õ�y����
        '''
        self.x = x
        self.y = y
    pass # class Pos

# WindowΪ������
class Window(object):
    def __init__(self, window_class_name: str, window_name: str, print_hwnd: bool = False, print_text: bool = False) -> None:
        '''
        ��ʼ������
            ��Ա:
                window_name: ��������һ���Ǵ��ڵ����ƣ��ڴ򿪵ĳ���Ĵ���������һ���������
                window_class_name: ���ڵ���������������spy++��ͨ��window_name����������������鿴
                hWnd: ���ھ�������ڲ��������������ڴ����е����꣬�ڴ������������
                window_left_top: �������Ͻǵ����꣬ΪPos�࣬window_left_top.xΪx���꣬window_left_top.yΪy����
                window_right_bottom: �������½ǵ����꣬ΪPos�࣬window_right_bottom.xΪx���꣬window_right_bottom.yΪy����
            ���
                window_name: ��������һ���Ǵ��ڵ����ƣ��ڴ򿪵ĳ���Ĵ���������һ���������
                window_class_name: ���ڵ���������������spy++��ͨ��window_name����������������鿴
        '''
        # ͨ������Ĵ�������(window_class_name)�ʹ�����(window_name)��������
        print("class_name =", window_class_name)
        window_pos, self.hWnd = self.GetWindow(class_name=window_class_name, window_name=window_name)
        # ���������������ṹ����
        self.window_name = window_name
        # �����������������ṹ����
        self.window_class_name = window_class_name
        # window_left_top��ʾ���ڵ����Ͻǣ���xΪ������������꣬yΪ��������������
        self.window_left_top = Pos(window_pos[0], window_pos[1]) # ���Ͻ�
        # window_right_bottom��ʾ���ڵ����½ǣ���xΪ�������Ҳ����꣬yΪ��������������
        self.window_right_bottom = Pos(window_pos[2], window_pos[3]) # ���½�
        pass # function __init__
    
    def GetWindow(self, class_name: str, window_name: str, print_hwnd: bool = False, print_text: bool = False) -> tuple[tuple[int, int, int, int], int]:
        '''
        /***************************************************************************************************/
        *   GetWindow: ���ش��ڵ��ļ����������λ����Ϣ�ȡ�
        *   
        *   ����:
        *       window_name: ��������һ���Ǵ��ڵ����ƣ��ڴ򿪵ĳ���Ĵ���������һ���������
        *       class_name: ���ڵ���������������spy++��ͨ��window_name����������������鿴
        *
        *   ���:
        *       window_pos: tuple[int, int, int, int]
        *           window_pos���ش��ڵ���Ļ���꣬�ֱ�Ϊ���ڵ�left, top, right, high
        *       hWnd: int
        *           hWnd���ش��ڵľ�������ڶ�������ڽ��в����������򴰿ڷ��������̲���
        /***************************************************************************************************/
        '''
        #hWnd���ļ������ͨ��ʹ��visual studio�Դ���spy++��õġ��ڹ������е� ����->spy++��
        # hWnd=win32gui.FindWindow('WeChatLoginWndForPC','΢��')
        hWnd=win32gui.FindWindow('WeChatMainWndForPC','΢��')
        # ͨ�����ھ������ȡ���ڵ�������Ϣ��������Ϊ��Ļ���꣬�����ڴ�����Ļ�е�ʲô����
        window_pos = win32gui.GetWindowRect(hWnd)
        #���ؾ�����ڵ��豸�����������������ڣ������ǿͻ��������������˵����߿�
        hwndDC = win32gui.GetWindowDC(hWnd)
        '''
        hwnd = win32gui.FindWindowEx(hWnd, 0, 'Qt5QWindowIcon', 'ScreenBoardClassWindow');
        if print_hwnd:
            print('hwnd =',hwnd)
        text = win32gui.GetWindowText(hwnd)                      #���ص��Ǵ��ڵ����֣���һ���Ǵ������Ͻ���ʾ�����֣�
        if print_text:
            print('Window Text =',text)
        hwnd_pos = win32gui.GetWindowRect(hwnd)  #(left,top)�����Ͻǵ����꣬(right,bottom)�����½ǵ�����
        #win32gui.SetForegroundWindow(hwnd)
        #���ؾ�����ڵ��豸�����������������ڣ������ǿͻ��������������˵����߿�
        hwndDC = win32gui.GetWindowDC(hwnd)
        #�����豸������
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        return (window_pos, hwnd_pos, hwnd, hwndDC, mfcDC)
        '''
        #return (window_pos, hwndDC, mfcDC)
        return (window_pos, hWnd)
        pass # function GetWindow
    pass # class Window


def get_screen_scale_factor() -> float:
    '''
    /***************************************************************************************************/
    *   get_screen_scale_factor: ��ȡ����ϵͳ��Ļ���ű���
    *
    *   ����: ��
    *
    *   ���:
    *       screen_scale: float
    *           ����ϵͳ�����ű�����Ϊfloatֵ������windows��������Ϊ125%���򷵻�ֵΪ1.25
    /***************************************************************************************************/
    '''
    global_params.global_parameters.default_screen_scale
    try:
        win32api.GetDpiForSystem()
        hDC = win32api.GetDC(0)
        dpiX = win32api.GetDeviceCaps(hDC, win32api.LOGPIXELSX)  # ��ȡˮƽDPI
        win32api.ReleaseDC(0, hDC)
        return dpiX / 96.0
    except Exception as e:
        print(f"Error: {e}")
        return global_params.global_parameters.default_screen_scale
    pass # function: get_screen_scale_factor