# -*- coding: gb2312 -*-

import window
import auto_mouse
import monitors
import queue
import win32process
import win32api
import win32con
import time
import global_params

class WeChatMonitor(monitors.Monitor):
    def __init__(self) -> None:
        self.processes = {}
        self.state_changed = queue.Queue()
        # 创建线程
        super().__init__("WeChatMonitor")
        pass # function: __init__
    
    def monitor(self) -> None:
        self.monitor_wechat()
        pass # function monitor
    
    def get_all_processes(self) -> None:
        # 清空之前的所有process信息
        self.processes.clear()
        # 获取当前windows中的所有process信息
        all_processes = win32process.EnumProcesses()
        # 打印每个进程的 ID 和名称
        for process_pid in all_processes:
            try:
                process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, process_pid)  # 1表示PROCESS_QUERY_INFORMATION权限
                process_name = win32process.GetModuleFileNameEx(process_handle, 0) # process_name包含全路径信息，例如: C:\Program Files\Tencent\WeChat\WeChat.exe
                # 循环将所有的process_name和pid添加到自身的processes字典中
                self.processes[process_name] = process_pid
            except Exception as e:
                #print(f"Error retrieving process ID {process_pid}: {e}")
                pass # end try
            pass # for process_pid
        pass # function: get_all_processes
    
    def check_wechat(self) -> bool:
        # 设置wechat的可执行程序的名字
        wechat_exe = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
        self.get_all_processes()
        if wechat_exe not in self.processes:
            print("warning: wechat is not running!")
            # TODO: 微信进程已退出
            return False
        else:
            print("debug: WeChat running well.")
            return True
        pass # function is_wechat_running
    
    def monitor_wechat(self):
        
        # 开始运行
        while True:
            is_running = self.check_wechat()
            if not is_running:
                self.operate()
            else:
                # self.wechat_is_running_queue.put(True) # 一切正常(微信进程正在运行中)，不需要put，不需要通知operator去执行操作
                pass # end if wechat_exe
            
            time.sleep(global_params.global_parameters.check_interval)
            pass # end while True
        pass # function monitor_wechat
    
    def operate(self) -> None:
        # TODO: ip地址发生变化时，通知wechat，发送信息
        print("TODO: wechat退出，重启wechat程序")
        pass # function operate
    pass # class: Monitor

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
    mouse.MoveAndClick(click_pos, wechat_window.hWnd)
    pass # function: wechat_login
