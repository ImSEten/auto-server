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
        '''
        /***************************************************************************************************/
        *   __init__: 初始化WeChatMonitor结构体
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # self.processes用于保存系统上的所有进程的信息，为一个dict
        # key为process_name, value为pid
        self.processes = {}
        # 调用父类，创建一个名为WeChatMonitor的线程，用于执行本类的monitor方法
        # 该线程将在本类继承自父类的start()函数被调用时被真正创建
        super().__init__("WeChatMonitor")
        pass # function: __init__
    
    def monitor(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor: 重写父类的monitor方法
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # 调用本类的monitor_wechat方法
        self.monitor_wechat()
        pass # function monitor
    
    def get_all_processes(self) -> None:
        '''
        /***************************************************************************************************/
        *   get_all_processes: 获取windows上的所有进程信息
        *
        *   输入: 无
        *
        *   输出: 无
        *
        *   注意！！！
        *   TODO: 该函数无法获取windows系统进程，需改进
        /***************************************************************************************************/
        '''
        # 清空已获取的所有process信息
        self.processes.clear()
        # 获取当前windows中的所有process信息
        all_processes = win32process.EnumProcesses()
        # 获取每个进程的 ID 和名称
        for process_pid in all_processes:
            try:
                process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, process_pid)  # 1表示PROCESS_QUERY_INFORMATION权限
                process_name = win32process.GetModuleFileNameEx(process_handle, 0) # process_name包含全路径信息，例如: C:\Program Files\Tencent\WeChat\WeChat.exe
                # 将每个进程的process_name和pid添加到自身的processes字典中
                self.processes[process_name] = process_pid
            except Exception as e:
                # 获取进程信息失败
                #print(f"Error retrieving process ID {process_pid}: {e}")
                pass # end try
            pass # for process_pid
        pass # function: get_all_processes
    
    def check_wechat(self) -> bool:
        '''
        /***************************************************************************************************/
        *   check_wechat: 检查WeChat进程是否正在运行中，登录进程和聊天进程任何一个正在运行中，都算是正在运行
        *
        *   输入: 无
        *
        *   输出: bool
        *       如果WeChat进程正在运行中，返回True，否则返回False
        /***************************************************************************************************/
        '''
        # 设置wechat的可执行程序的名字
        wechat_exe = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
        # 获取全部的进程信息
        self.get_all_processes()
        # 判断WeChat进程是否正在运行
        if wechat_exe not in self.processes: # 当全部进程信息中，没有WeChat进程，表明WeChat进程没有运行
            print("warning: wechat is not running!")
            # TODO: 微信进程已退出
            return False
        else: # 系统所有进程信息中有WeChat进程，表明WeChat进程正在运行
            print("debug: WeChat running well.")
            return True
        pass # function is_wechat_running
    
    def monitor_wechat(self):
        '''
        /***************************************************************************************************/
        *   monitor_wechat: 监控wechat进程是否正常，如果不正常，则会执行启动微信并登录的操作
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # 开始运行
        while True:
            # 检查WeChat进程是否正在运行
            is_running = self.check_wechat()
            if not is_running: # WeChat进程没有运行，调用self.operate()执行相应的动作
                self.operate()
            else: # WeChat运行中，不执行操作
                # self.wechat_is_running_queue.put(True) # 一切正常(微信进程正在运行中)，不需要put，不需要通知operator去执行操作
                pass # end if wechat_exe
            
            time.sleep(global_params.global_parameters.check_interval) # 每check_interval秒检查一次WeChat进程
            pass # end while True
        pass # function monitor_wechat
    
    def operate(self) -> None:
        '''
        /***************************************************************************************************/
        *   operate: 重启微信程序
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        # TODO: wechat退出，重启wechat程序
        print("TODO: wechat退出，重启wechat程序")
        pass # function operate
    pass # class: Monitor


class Person(object):
    '''
    /***************************************************************************************************/
    *   Person: Person类，包含人名，已经头像的图片存储位置
    *       结构体中的成员变量:
    *           picture_path: 头像图片存储位置
    *           name: 人名
    *
    *   输入: 无
    *
    *   输出: 无
    /***************************************************************************************************/
    '''
    def __init__(self, picture_path = "", name = "") -> None:
        '''
        /***************************************************************************************************/
        *   __init__: 初始化Person类，人名以及头像图片存储位置设置为空
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        self.picture_path = picture_path
        self.name = name
        pass # function __init__
    pass

class Process(object):
    def __init__(self, process_id = -1, process_hWnd = -1, running = False) -> None:
        '''
        /***************************************************************************************************/
        *   __init__: 初始化Process类，pid、process窗口句柄，是否正在运行
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        self.process_id = process_id
        self.process_hWnd = process_hWnd
        self.running = running
        pass # function __init__
    pass # class Process

class WeChatOperator(object):
    def __init__(self) -> None:
        '''
        /***************************************************************************************************/
        *   __init__: 初始化WeChatOperator结构体
        *       结构体中的成员变量:
        *           wechat_login_process: WeChat进程的登录界面时刻的进程
        *           wechat_chat_process: WeChat进程的聊天界面时刻的进程
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        self.wechat_login_process = Process()
        self.wechat_chat_process = Process()
        pass # function __init__

    def send_messages(self, person: Person, messages: list[str]) -> None:
        '''
        /***************************************************************************************************/
        *   send_messages: WeChat进程发送消息
        *       结构体中的成员变量:
        *           wechat_login_process: WeChat进程的登录界面时刻的进程
        *           wechat_chat_process: WeChat进程的聊天界面时刻的进程
        *
        *   输入: 无
        *
        *   输出: 无
        /***************************************************************************************************/
        '''
        pass # function send_messages
    pass # class WeChatOperator

def wechat_login():
    '''
    /***************************************************************************************************/
    *   wechat_login: 登录微信
    *       该函数的步骤:
    *           1. 获取微信登录进程的窗口信息
    *           2. 获取微信登录按钮的位置信息
    *           3. 点击微信登录按钮，实现微信登录操作
    *
    *   输入: 无
    *
    *   输出: 无
    /***************************************************************************************************/
    '''
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
