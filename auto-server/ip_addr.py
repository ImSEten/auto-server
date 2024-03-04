import socket

# ��ȡipv4��ַ�����ڱ�д����ʱ��������о�����ipv4��ַ���޹���ipv4��ַ����˸õ�ַΪ������ipv4��ַ
def get_ipv4_address():
    hostname = socket.gethostname()    
    ipv4_address = socket.gethostbyname(hostname)
    return ipv4_address
    pass # function: get_ipv4_address

ipv4_address = get_ipv4_address()
print("Local IPv4 Address: " + ipv4_address)

# ��ȡ����ipv6��ַ��windows11�汾������ʱipv6��ַ��ipv6��ַ���������ȫ���������ų���fe80��ͷ�ı���ipv6��ַ
# �����ԣ���ʱipv6��ַ��ipv6��ַ�����Դ���������
def get_public_ipv6_address():
    ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
    public_ipv6_addresses = [addr[4][0] for addr in ip_addresses if not addr[4][0].startswith("fe80")]
    return public_ipv6_addresses
    pass # function: get_public_ipv6_address

# ��ȡipv6��ַ
def get_ipv6_address():
    ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
    ipv6_addresses = [addr[4][0] for addr in ip_addresses]
    return ipv6_addresses
    pass # function: get_ipv6_address

public_ipv6_addresses = get_public_ipv6_address()
for address in public_ipv6_addresses:
    print("Public IPv6 Address: " + address)