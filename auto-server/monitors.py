# -*- coding: gb2312 -*-

import wmi
import threading

# monitor ������
class Monitor(object):
    def __init__(self, monitor_name: str) -> None:
        '''
        /***************************************************************************************************/
        *   Monitor: ��ʼ��Monitor��
        *       ����Monitor����߳�
        *
        *   ����: 
        *       monitor_name: �����ļ���߳�����
        *
        *   ���:
        *       ��
        /***************************************************************************************************/
        '''
        # �����߳�
        self.monitor_thread = threading.Thread(target=self.monitor, name=monitor_name, daemon=True)
        pass # function __init__
    
    def start(self) -> None:
        '''
        /***************************************************************************************************/
        *   ����Monitor��ʼ��ʱ�������߳�
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        self.monitor_thread.start()
        pass # function start
    
    def monitor(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor: ����Monitor������һ��monitor�ӿڣ��ýӿڱ�monitor_threadʹ�ã�����������ʵ��
        /***************************************************************************************************/
        '''
        pass # function monitor
    
    def operate(self) -> None:
        '''
        /***************************************************************************************************/
        *   operate: ����Monitor������һ��operate�ӿڣ�
        *   �ýӿڱ�monitor�������ã�����������ʵ��monitor�ĵ��ü�����ʵ��
        /***************************************************************************************************/
        '''
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