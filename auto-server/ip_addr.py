import socket

# 获取ipv4地址，由于编写代码时计算机仅有局域网ipv4地址，无公网ipv4地址，因此该地址为局域网ipv4地址
def get_ipv4_address():
    hostname = socket.gethostname()    
    ipv4_address = socket.gethostbyname(hostname)
    return ipv4_address
    pass # function: get_ipv4_address

ipv4_address = get_ipv4_address()
print("Local IPv4 Address: " + ipv4_address)

# 获取公网ipv6地址，windows11版本会有临时ipv6地址和ipv6地址，这个函数全都包含，排除以fe80开头的本地ipv6地址
# 经测试，临时ipv6地址和ipv6地址都可以从外网访问
def get_public_ipv6_address():
    ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
    public_ipv6_addresses = [addr[4][0] for addr in ip_addresses if not addr[4][0].startswith("fe80")]
    return public_ipv6_addresses
    pass # function: get_public_ipv6_address

# 获取ipv6地址
def get_ipv6_address():
    ip_addresses = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
    ipv6_addresses = [addr[4][0] for addr in ip_addresses]
    return ipv6_addresses
    pass # function: get_ipv6_address

public_ipv6_addresses = get_public_ipv6_address()
for address in public_ipv6_addresses:
    print("Public IPv6 Address: " + address)