# -*- coding: gb2312 -*-

import wmi
import threading


# TODO: 
# 1������Monitor�ṹ�����
# 2��WeChatMonitor�ŵ�auto_WeChat.py��
# 3��IpMonitor�ŵ�auto_ip_addr.py��

# monitor ������
class Monitor(object):
    def __init__(self, monitor_name: str) -> None:
        # �����߳�
        self.monitor_thread = threading.Thread(target=self.monitor, name=monitor_name, daemon=True)
        pass # function __init__
    
    def start(self) -> None:
        self.monitor_thread.start()
        pass # function start
    
    def monitor(self) -> None:
        pass # function monitor
    
    def operate(self) -> None:
        print("not implement!")
        pass # function operate
    
    pass # class Monitor







# ʹ��wmi���ȡ�����������еĽ�����Ϣ��
# ������δʹ�����ַ�ʽ��ԭ����Ч��̫�͡�
def check_process_running(process_name):
    c = wmi.WMI()
    for process in c.Win32_Process():
        # print(process.Name) # process.Name������׺������������Ľ��ΪWeChat.exe
        if process.Name == process_name:
            return True
    return False

