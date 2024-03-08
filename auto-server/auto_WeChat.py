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
        *   __init__: ��ʼ��WeChatMonitor�ṹ��
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # self.processes���ڱ���ϵͳ�ϵ����н��̵���Ϣ��Ϊһ��dict
        # keyΪprocess_name, valueΪpid
        self.processes = {}
        # ���ø��࣬����һ����ΪWeChatMonitor���̣߳�����ִ�б����monitor����
        # ���߳̽��ڱ���̳��Ը����start()����������ʱ����������
        super().__init__("WeChatMonitor")
        pass # function: __init__
    
    def monitor(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor: ��д�����monitor����
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # ���ñ����monitor_wechat����
        self.monitor_wechat()
        pass # function monitor
    
    def get_all_processes(self) -> None:
        '''
        /***************************************************************************************************/
        *   get_all_processes: ��ȡwindows�ϵ����н�����Ϣ
        *
        *   ����: ��
        *
        *   ���: ��
        *
        *   ע�⣡����
        *   TODO: �ú����޷���ȡwindowsϵͳ���̣���Ľ�
        /***************************************************************************************************/
        '''
        # ����ѻ�ȡ������process��Ϣ
        self.processes.clear()
        # ��ȡ��ǰwindows�е�����process��Ϣ
        all_processes = win32process.EnumProcesses()
        # ��ȡÿ�����̵� ID ������
        for process_pid in all_processes:
            try:
                process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, process_pid)  # 1��ʾPROCESS_QUERY_INFORMATIONȨ��
                process_name = win32process.GetModuleFileNameEx(process_handle, 0) # process_name����ȫ·����Ϣ������: C:\Program Files\Tencent\WeChat\WeChat.exe
                # ��ÿ�����̵�process_name��pid��ӵ������processes�ֵ���
                self.processes[process_name] = process_pid
            except Exception as e:
                # ��ȡ������Ϣʧ��
                #print(f"Error retrieving process ID {process_pid}: {e}")
                pass # end try
            pass # for process_pid
        pass # function: get_all_processes
    
    def check_wechat(self) -> bool:
        '''
        /***************************************************************************************************/
        *   check_wechat: ���WeChat�����Ƿ����������У���¼���̺���������κ�һ�����������У���������������
        *
        *   ����: ��
        *
        *   ���: bool
        *       ���WeChat�������������У�����True�����򷵻�False
        /***************************************************************************************************/
        '''
        # ����wechat�Ŀ�ִ�г��������
        wechat_exe = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
        # ��ȡȫ���Ľ�����Ϣ
        self.get_all_processes()
        # �ж�WeChat�����Ƿ���������
        if wechat_exe not in self.processes: # ��ȫ��������Ϣ�У�û��WeChat���̣�����WeChat����û������
            print("warning: wechat is not running!")
            # TODO: ΢�Ž������˳�
            return False
        else: # ϵͳ���н�����Ϣ����WeChat���̣�����WeChat������������
            print("debug: WeChat running well.")
            return True
        pass # function is_wechat_running
    
    def monitor_wechat(self):
        '''
        /***************************************************************************************************/
        *   monitor_wechat: ���wechat�����Ƿ���������������������ִ������΢�Ų���¼�Ĳ���
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # ��ʼ����
        while True:
            # ���WeChat�����Ƿ���������
            is_running = self.check_wechat()
            if not is_running: # WeChat����û�����У�����self.operate()ִ����Ӧ�Ķ���
                self.operate()
            else: # WeChat�����У���ִ�в���
                # self.wechat_is_running_queue.put(True) # һ������(΢�Ž�������������)������Ҫput������Ҫ֪ͨoperatorȥִ�в���
                pass # end if wechat_exe
            
            time.sleep(global_params.global_parameters.check_interval) # ÿcheck_interval����һ��WeChat����
            pass # end while True
        pass # function monitor_wechat
    
    def operate(self) -> None:
        '''
        /***************************************************************************************************/
        *   operate: ����΢�ų���
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # TODO: wechat�˳�������wechat����
        print("TODO: wechat�˳�������wechat����")
        pass # function operate
    pass # class: Monitor


class Person(object):
    '''
    /***************************************************************************************************/
    *   Person: Person�࣬�����������Ѿ�ͷ���ͼƬ�洢λ��
    *       �ṹ���еĳ�Ա����:
    *           picture_path: ͷ��ͼƬ�洢λ��
    *           name: ����
    *
    *   ����: ��
    *
    *   ���: ��
    /***************************************************************************************************/
    '''
    def __init__(self, picture_path = "", name = "") -> None:
        '''
        /***************************************************************************************************/
        *   __init__: ��ʼ��Person�࣬�����Լ�ͷ��ͼƬ�洢λ������Ϊ��
        *
        *   ����: ��
        *
        *   ���: ��
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
        *   __init__: ��ʼ��Process�࣬pid��process���ھ�����Ƿ���������
        *
        *   ����: ��
        *
        *   ���: ��
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
        *   __init__: ��ʼ��WeChatOperator�ṹ��
        *       �ṹ���еĳ�Ա����:
        *           wechat_login_process: WeChat���̵ĵ�¼����ʱ�̵Ľ���
        *           wechat_chat_process: WeChat���̵��������ʱ�̵Ľ���
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        self.wechat_login_process = Process()
        self.wechat_chat_process = Process()
        pass # function __init__

    def send_messages(self, person: Person, messages: list[str]) -> None:
        '''
        /***************************************************************************************************/
        *   send_messages: WeChat���̷�����Ϣ
        *       �ṹ���еĳ�Ա����:
        *           wechat_login_process: WeChat���̵ĵ�¼����ʱ�̵Ľ���
        *           wechat_chat_process: WeChat���̵��������ʱ�̵Ľ���
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        pass # function send_messages
    pass # class WeChatOperator

def wechat_login():
    '''
    /***************************************************************************************************/
    *   wechat_login: ��¼΢��
    *       �ú����Ĳ���:
    *           1. ��ȡ΢�ŵ�¼���̵Ĵ�����Ϣ
    *           2. ��ȡ΢�ŵ�¼��ť��λ����Ϣ
    *           3. ���΢�ŵ�¼��ť��ʵ��΢�ŵ�¼����
    *
    *   ����: ��
    *
    *   ���: ��
    /***************************************************************************************************/
    '''
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
