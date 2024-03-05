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
        # �����߳�
        super().__init__("WeChatMonitor")
        pass # function: __init__
    
    def monitor(self) -> None:
        self.monitor_wechat()
        pass # function monitor
    
    def get_all_processes(self) -> None:
        # ���֮ǰ������process��Ϣ
        self.processes.clear()
        # ��ȡ��ǰwindows�е�����process��Ϣ
        all_processes = win32process.EnumProcesses()
        # ��ӡÿ�����̵� ID ������
        for process_pid in all_processes:
            try:
                process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, process_pid)  # 1��ʾPROCESS_QUERY_INFORMATIONȨ��
                process_name = win32process.GetModuleFileNameEx(process_handle, 0) # process_name����ȫ·����Ϣ������: C:\Program Files\Tencent\WeChat\WeChat.exe
                # ѭ�������е�process_name��pid��ӵ������processes�ֵ���
                self.processes[process_name] = process_pid
            except Exception as e:
                #print(f"Error retrieving process ID {process_pid}: {e}")
                pass # end try
            pass # for process_pid
        pass # function: get_all_processes
    
    def check_wechat(self) -> bool:
        # ����wechat�Ŀ�ִ�г��������
        wechat_exe = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
        self.get_all_processes()
        if wechat_exe not in self.processes:
            print("warning: wechat is not running!")
            # TODO: ΢�Ž������˳�
            return False
        else:
            print("debug: WeChat running well.")
            return True
        pass # function is_wechat_running
    
    def monitor_wechat(self):
        
        # ��ʼ����
        while True:
            is_running = self.check_wechat()
            if not is_running:
                self.operate()
            else:
                # self.wechat_is_running_queue.put(True) # һ������(΢�Ž�������������)������Ҫput������Ҫ֪ͨoperatorȥִ�в���
                pass # end if wechat_exe
            
            time.sleep(global_params.global_parameters.check_interval)
            pass # end while True
        pass # function monitor_wechat
    
    def operate(self) -> None:
        # TODO: ip��ַ�����仯ʱ��֪ͨwechat��������Ϣ
        print("TODO: wechat�˳�������wechat����")
        pass # function operate
    pass # class: Monitor

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
    mouse.MoveAndClick(click_pos, wechat_window.hWnd)
    pass # function: wechat_login
