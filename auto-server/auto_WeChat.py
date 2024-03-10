# -*- coding: gb2312 -*-

import window
import auto_mouse_keyboard
import monitors
import queue
import win32process
import win32api
import win32con
import time
import global_params
import threading

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
    '''
    Process���̣��������̵ĸ�����Ϣ
        1������pid
        2�����̴��ھ��
        3�������Ƿ�������
    '''
    def __init__(self, process_id = -1, process_window: window.Window = None , running = False) -> None:
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
        self.process_window = process_window
        self.running = running
        pass # function __init__
    pass # class Process

class WeChatSender(object):
    def __init__(self, message_queue: queue.Queue) -> None:
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
        # ��ʼ��һ�����ṹ��ͼ��̽ṹ��
        self.mouse = auto_mouse_keyboard.Mouse()
        self.keyboard = auto_mouse_keyboard.Keyboard()
        
        wechat_login_window = window.Window(window_class_name='WeChatLoginWndForPC', window_name='΢��')
        wechat_chat_window = window.Window(window_class_name='WeChatMainWndForPC', window_name='΢��')
        self.wechat_login_process = Process(process_window=wechat_login_window)
        self.wechat_chat_process = Process(process_window=wechat_chat_window)
        self.message_queue = message_queue
        self.operator_thread = threading.Thread(target=self.get_event, name="WeChatOperator", daemon=True)
        pass # function __init__
    
    def start(self) -> None:
        self.operator_thread.start()
        pass # function start
    
    def get_event(self) -> None:
        '''
        /***************************************************************************************************/
        * �������queue�л�ȡ��Ϣ�����ڷ��͸��û�
        *
        * ����: ��
        *
        * ���: ��
        /***************************************************************************************************/
        '''
        while True:
            message = self.message_queue.get()
            print("receive a message:", message)
            time.sleep(1)
            try:
                self.send_message(person=None, message=message)
            except:
                self.message_queue.put(message)
                print("Error: function get_event(): cannot send message:", message)
                continue
                pass # try except
            pass # while True
        pass # function get_event
    
    def get_person_click_pos(self, person: Person) -> window.Pos:
        # TODO: choose someone
        #(273, 137)
        first_person_pos = window.Pos(210, 100)
        click_pos = window.Pos(
            self.wechat_chat_process.process_window.window_left_top.x + first_person_pos.x, 
            self.wechat_chat_process.process_window.window_left_top.y + first_person_pos.y)
        return click_pos
        pass # function choose_person

    def send_message(self, person: Person, message: str) -> None:
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
        # �����һ����
        person_click_pos = self.get_person_click_pos(person=person)
        self.mouse.MoveAndClick(person_click_pos, self.wechat_chat_process.process_window.hWnd)
        # ��������
        self.keyboard.tap(message, self.wechat_chat_process.process_window.hWnd)
        # ������Ϣ
        self.keyboard.tap_enter(self.wechat_chat_process.process_window.hWnd)
        pass # function send_messages
    pass # class WeChatOperator

def login_wechat():
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
    wechat_login_window = window.Window(window_class_name='WeChatLoginWndForPC', window_name='΢��')
    print("wechat window position =", wechat_login_window.window_left_top.x, wechat_login_window.window_left_top.y, wechat_login_window.window_right_bottom.x, wechat_login_window.window_right_bottom.y)
    print("wechat window hwnd =", wechat_login_window.hWnd)
    # ��ʼ��һ�����ṹ��
    mouse = auto_mouse_keyboard.Mouse()
    # TODO: screen_scale����Ļ���ű���
    # ʵ�ⲻ��Ҫ������Ļ���ű����ĵ���
    screen_scale = window.get_screen_scale_factor()
    screen_scale = globals.global_params.default_screen_scale

    # ��½΢�Ű�ť��λ����Ϣ����λ����Ϣ������ڴ������Ͻǵ�λ����Ϣ��
    # ����΢�Ű�ť��λ��Ϊ��140, 300��ʾ�����Ͻǿ�ʼ+140�����Ͻ�+300���ǰ�ťλ�á�
    login_pos = window.Pos(int((wechat_login_window.window_right_bottom.x - wechat_login_window.window_left_top.x) / 2 * screen_scale), int((wechat_login_window.window_right_bottom.y - wechat_login_window.window_left_top.y) / 5 * 4 * screen_scale))
    print("login position =", login_pos.x, login_pos.y)
    click_pos = window.Pos(int(login_pos.x + wechat_login_window.window_left_top.x), int(login_pos.y + wechat_login_window.window_left_top.y))
    # �����
    mouse.MoveAndClick(click_pos, wechat_login_window.hWnd)
    pass # function: wechat_login
