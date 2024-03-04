import wmi
import win32api
import win32process
import win32con
import threading
import time
import queue
import ip_addr
import socket

class WeChatMonitor(object):
    def __init__(self) -> None:
        self.processes = {}
        self.wechat_is_running_queue = queue.Queue()
        # �����߳�
        wechat_monitor_thread = threading.Thread(target=self.monitor_wechat, name="WeChatMonitor", daemon=True)
        wechat_monitor_thread.start()
        pass # function: __init__
    
    def get_all_processes(self) -> None:
        # ���֮ǰ������process��Ϣ
        self.processes.clear()
        # ��ȡ��ǰwindows�е�����process��Ϣ
        all_processes = win32process.EnumProcesses()
        # ��ӡÿ�����̵� ID ������
        for process_pid in all_processes:
            try:
                process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, process_pid)  # 1��ʾPROCESS_QUERY_INFORMATIONȨ��
                process_name = win32process.GetModuleFileNameEx(process_handle, 0) # process_name����ȫ·����Ϣ������: C:\Program Files\Tencent\WeChat\WeChat.exe
                # ѭ�������е�process_name��pid��ӵ������processes�ֵ���
                self.processes[process_name] = process_pid
            except Exception as e:
                print(f"Error retrieving process ID {process_pid}: {e}")
                pass # end try
            pass # for process_pid
        pass # function: get_all_processes
    
    def monitor_wechat(self):
        # ����wechat�Ŀ�ִ�г��������
        wechat_exe = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
        # ��ʼ����
        while True:
            self.get_all_processes()
            if wechat_exe not in self.processes:
                print("warning: wechat is not running!")
                self.wechat_is_running_queue.put(False)
            else:
                print("debug: wechat is running!")
                self.wechat_is_running_queue.put(True)
                pass # end if wechat_exe
            
            time.sleep(300)
            pass # end while True
        pass # 
    pass # class: Monitor

class IpMonitor(object):
    def __init__(self) -> None:
        # TODO: ��ȡ��ǰ��ip��ַ
        self.ipv6 = ["2409:8a62:e45:4a40:b59c:f76c:b68a:9f6e", "2409:8a62:e45:4a40:909a:ba8b:658:ce1fa"]
        self.ipv6_changed = queue.Queue()
        # �����߳�
        ip_monitor_thread = threading.Thread(target=self.monitor_ip, name="IpMonitor", daemon=True)
        ip_monitor_thread.start()
        pass # function: __init__
    
    # ��ȡipv4��ַ�����ڱ�д����ʱ��������о�����ipv4��ַ���޹���ipv4��ַ����˸õ�ַΪ������ipv4��ַ
    def get_ipv4_address(self):
        hostname = socket.gethostname()    
        ipv4_address = socket.gethostbyname(hostname)
        return ipv4_address
        pass # function: get_ipv4_address
    
    # ��ȡ����ipv6��ַ��windows11�汾������ʱipv6��ַ��ipv6��ַ���������ȫ���������ų���fe80��ͷ�ı���ipv6��ַ
    # �����ԣ���ʱipv6��ַ��ipv6��ַ�����Դ���������
    def get_public_ipv6_address(self):
        ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        public_ipv6_addresses = [addr[4][0] for addr in ip_addresses if not addr[4][0].startswith("fe80")]
        return public_ipv6_addresses
        pass # function: get_public_ipv6_address
    
    # ��ȡipv6��ַ
    def get_ipv6_address(self):
        ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        ipv6_addresses = [addr[4][0] for addr in ip_addresses]
        return ipv6_addresses
        pass # function: get_ipv6_address
    
    def monitor_ip(self):
        # ��ʼ����
        while True:
            ipv6 = self.get_public_ipv6_address()
            if set(ipv6) != set(self.ipv6):
                print("warning: ipv6 addr has changed!")
                self.ipv6_changed.put(True)
            else:
                print("debug: wechat is running!")
                self.ipv6_changed.put(False)
                pass # end if wechat_exe
            
            time.sleep(300)
            pass # end while True
        pass # function: monitor_ip
    pass # class: IpMonitor





# ʹ��wmi���ȡ�����������еĽ�����Ϣ��
# ������δʹ�����ַ�ʽ��ԭ����Ч��̫�͡�
def check_process_running(process_name):
    c = wmi.WMI()
    for process in c.Win32_Process():
        # print(process.Name) # process.Name������׺������������Ľ��ΪWeChat.exe
        if process.Name == process_name:
            return True
    return False

