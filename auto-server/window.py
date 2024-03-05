﻿import win32api
import win32con
import win32gui
import win32ui
import global_params

# Pos为位置类，表示坐标位置信息
class Pos(object):
    def __init__(self, x: int, y: int) -> None:
        '''
        成员:
            x: 坐标位置的x坐标
            y: 坐标位置的y坐标
        '''
        self.x = x
        self.y = y
    pass # class Pos

# Window为窗口类
class Window(object):
    def __init__(self, window_class_name: str, window_name: str, print_hwnd: bool = False, print_text: bool = False) -> None:
        '''
        初始化窗口
            成员:
                window_name: 窗口名，一般是窗口的名称，在打开的程序的窗口最上面一般会有名字
                window_class_name: 窗口的类型名，可以在spy++中通过window_name将窗口搜索出来后查看
                hWnd: 窗口句柄，用于操作操作，比如在窗口中点击鼠标，在窗口中输入键盘
                window_left_top: 窗口左上角的坐标，为Pos类，window_left_top.x为x坐标，window_left_top.y为y坐标
                window_right_bottom: 窗口右下角的坐标，为Pos类，window_right_bottom.x为x坐标，window_right_bottom.y为y坐标
            入参
                window_name: 窗口名，一般是窗口的名称，在打开的程序的窗口最上面一般会有名字
                window_class_name: 窗口的类型名，可以在spy++中通过window_name将窗口搜索出来后查看
        '''
        
        window_pos, self.hWnd = self.GetWindow(class_name=window_class_name, window_name=window_name)
        self.window_name = window_name
        self.window_class_name = window_class_name
        self.window_left_top = Pos(window_pos[0], window_pos[1]) # 左上角
        self.window_right_bottom = Pos(window_pos[2], window_pos[3]) # 右下角
        pass # function __init__
    
    #获取窗口坐标
    def GetWindow(class_name: str, window_name: str, print_hwnd: bool = False, print_text: bool = False) -> tuple[tuple[int, int, int, int], int]:
        '''
        /***************************************************************************************************/
        *   返回窗口的文件句柄，窗口位置信息等。
        *   
        *   输入:
        *       window_name: 窗口名，一般是窗口的名称，在打开的程序的窗口最上面一般会有名字
        *       class_name: 窗口的类型名，可以在spy++中通过window_name将窗口搜索出来后查看
        /***************************************************************************************************/
        '''
        #hWnd是文件句柄，通过使用visual studio自带的spy++获得的。在工具栏中的 工具->spy++中
        # hWnd=win32gui.FindWindow('WeChatLoginWndForPC','微信')
        hWnd=win32gui.FindWindow('WeChatMainWndForPC','微信')
        window_pos = win32gui.GetWindowRect(hWnd)
        #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hwndDC = win32gui.GetWindowDC(hWnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        '''
        hwnd = win32gui.FindWindowEx(hWnd, 0, 'Qt5QWindowIcon', 'ScreenBoardClassWindow');
        if print_hwnd:
            print('hwnd =',hwnd)
        text = win32gui.GetWindowText(hwnd)                      #返回的是窗口的名字（不一定是窗口左上角显示的名字）
        if print_text:
            print('Window Text =',text)
        hwnd_pos = win32gui.GetWindowRect(hwnd)  #(left,top)是左上角的坐标，(right,bottom)是右下角的坐标
        #win32gui.SetForegroundWindow(hwnd)
        #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hwndDC = win32gui.GetWindowDC(hwnd)
        #创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        return (window_pos, hwnd_pos, hwnd, hwndDC, mfcDC)
        '''
        #return (window_pos, hwndDC, mfcDC)
        return (window_pos, hWnd)
        pass # function GetWindow
    pass # class Window


def get_screen_scale_factor() -> float:
    global_params.global_parameters.default_screen_scale
    try:
        win32api.GetDpiForSystem()
        hDC = win32api.GetDC(0)
        dpiX = win32api.GetDeviceCaps(hDC, win32api.LOGPIXELSX)  # 获取水平DPI
        win32api.ReleaseDC(0, hDC)
        return dpiX / 96.0
    except Exception as e:
        print(f"Error: {e}")
        return global_params.global_parameters.default_screen_scale
    pass # function: get_screen_scale_factor