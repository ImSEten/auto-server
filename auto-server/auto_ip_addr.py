# -*- coding: gb2312 -*-

import monitors
import time
import queue
import socket
import global_params

class IpMonitor(monitors.Monitor):
    def __init__(self, message_event: queue.Queue) -> None:
        '''
        /***************************************************************************************************/
        *   __init__: ��ʼ��IpMonitor�ṹ��
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # TODO: ��ȡ��ǰ��ip��ַ
        # self.ipv6���ڴ洢ϵͳipv6��ַ��Ϣ
        self.ipv6 = []
        self.message_event = message_event
        # ���ø��࣬����һ����ΪIpMonitor���̣߳�����ִ�б����monitor����
        # ���߳̽��ڱ���̳��Ը����start()����������ʱ����������
        super().__init__("IpMonitor")
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
        # ���ñ����monitor_ip����
        self.monitor_ip()
        pass # function monitor
    
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
    
    def check_ipv6_changed(self) -> bool:
        '''
        /***************************************************************************************************/
        *   check_ipv6_changed: ���ipv6��ַ�Ƿ����ı䣬windows11������ʱipv6������ipv6��ַ�����������Ա���������
        *   �κ�һ�������ı䶼��Ϊipv6��ַ�����仯
        *
        *   ����: ��
        *
        *   ���: bool
        *       ���ipv6��ַ��Ϣ�����ı䣬����True�����򷵻�False
        /***************************************************************************************************/
        '''
        ipv6 = self.get_public_ipv6_address()
        if set(ipv6) != set(self.ipv6): # ipv6��ַ�����ı�
            print("warning: ipv6 addr has changed!")
            print("old ip:", self.ipv6)
            print("new ip:", ipv6)
            self.ipv6 = ipv6 # �޸�monitor�е�ipv6��ַ������֮���䷢�͸�operator
            return True
        else:
            print("debug: ipv6 addr keep the same.")
            return False
            pass # end if wechat_exe
        pass # function get_state
    
    def monitor_ip(self) -> None:
        '''
        /***************************************************************************************************/
        *   monitor_ip: ���ipv6��ַ�Ƿ����ı䣬��������仯�����֪ͨWeChat���̷�����Ϣ
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # ��ʼ����
        while True:
            # ���Ipv6��ַ��Ϣ�Ƿ����ı�
            state_chaged = self.check_ipv6_changed()
            if state_chaged: # ipv6��ַ�����ı䣬����self.operate()ִ����Ӧ�Ķ���
                self.operate()
                # self.state_changed.put(True) # ��������仯(ip��ַ�����ı�)��֪ͨoperatorִ�в���
            else:
                # self.state_changed.put(False) # һ������(ip��ַû�з����ı�)������Ҫput������Ҫ֪ͨoperatorȥִ�в���
                pass # end if wechat_exe
            time.sleep(global_params.global_parameters.check_interval) # ÿcheck_interval����һ��ip��ַ�Ƿ����ı�
            pass # end while True
        pass # function: monitor_ip
    
    def operate(self) -> None:
        '''
        /***************************************************************************************************/
        *   operate: ֪ͨWeChat���̷�����Ϣ
        *
        *   ����: ��
        *
        *   ���: ��
        /***************************************************************************************************/
        '''
        # TODO: ip��ַ�����仯ʱ��֪ͨwechat��������Ϣ
        print("TODO: ip��ַ�����仯ʱ��֪ͨwechat��������Ϣ")
        for ipv6 in self.ipv6:
            self.message_event.put(ipv6)
            pass # for ipvt in self.ipv6
        pass # function operate
    pass # class: IpMonitor



# class IpOperator(operators.Operator):
#     def operate(self, monitor: monitors.IpMonitor) -> None:
#         print("ip addr changed!", monitor.ipv6)
#         pass # function: operate
#     pass # class IpOperator