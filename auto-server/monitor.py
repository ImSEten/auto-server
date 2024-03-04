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
        # 创建线程
        wechat_monitor_thread = threading.Thread(target=self.monitor_wechat, name="WeChatMonitor", daemon=True)
        wechat_monitor_thread.start()
        pass # function: __init__
    
    def get_all_processes(self) -> None:
        # 清空之前的所有process信息
        self.processes.clear()
        # 获取当前windows中的所有process信息
        all_processes = win32process.EnumProcesses()
        # 打印每个进程的 ID 和名称
        for process_pid in all_processes:
            try:
                process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, process_pid)  # 1表示PROCESS_QUERY_INFORMATION权限
                process_name = win32process.GetModuleFileNameEx(process_handle, 0) # process_name包含全路径信息，例如: C:\Program Files\Tencent\WeChat\WeChat.exe
                # 循环将所有的process_name和pid添加到自身的processes字典中
                self.processes[process_name] = process_pid
            except Exception as e:
                print(f"Error retrieving process ID {process_pid}: {e}")
                pass # end try
            pass # for process_pid
        pass # function: get_all_processes
    
    def monitor_wechat(self):
        # 设置wechat的可执行程序的名字
        wechat_exe = "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"
        # 开始运行
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
        # TODO: 获取以前的ip地址
        self.ipv6 = ["2409:8a62:e45:4a40:b59c:f76c:b68a:9f6e", "2409:8a62:e45:4a40:909a:ba8b:658:ce1fa"]
        self.ipv6_changed = queue.Queue()
        # 创建线程
        ip_monitor_thread = threading.Thread(target=self.monitor_ip, name="IpMonitor", daemon=True)
        ip_monitor_thread.start()
        pass # function: __init__
    
    # 获取ipv4地址，由于编写代码时计算机仅有局域网ipv4地址，无公网ipv4地址，因此该地址为局域网ipv4地址
    def get_ipv4_address(self):
        hostname = socket.gethostname()    
        ipv4_address = socket.gethostbyname(hostname)
        return ipv4_address
        pass # function: get_ipv4_address
    
    # 获取公网ipv6地址，windows11版本会有临时ipv6地址和ipv6地址，这个函数全都包含，排除以fe80开头的本地ipv6地址
    # 经测试，临时ipv6地址和ipv6地址都可以从外网访问
    def get_public_ipv6_address(self):
        ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        public_ipv6_addresses = [addr[4][0] for addr in ip_addresses if not addr[4][0].startswith("fe80")]
        return public_ipv6_addresses
        pass # function: get_public_ipv6_address
    
    # 获取ipv6地址
    def get_ipv6_address(self):
        ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
        ipv6_addresses = [addr[4][0] for addr in ip_addresses]
        return ipv6_addresses
        pass # function: get_ipv6_address
    
    def monitor_ip(self):
        # 开始运行
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





# 使用wmi库获取所有正在运行的进程信息。
# 本程序未使用这种方式，原因是效率太低。
def check_process_running(process_name):
    c = wmi.WMI()
    for process in c.Win32_Process():
        # print(process.Name) # process.Name包含后缀名，例如输出的结果为WeChat.exe
        if process.Name == process_name:
            return True
    return False

