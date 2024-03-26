#works with ipv6 only
import subprocess
import time
import socket

def ipv6_get():
    ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[2][4][0]
    return ipv6

def changeipv6ip():
    subprocess.run(args=['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'disabled'])
    print("rede reiniciada")
    time.sleep(2)
    subprocess.run(args=['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'enabled'])
    time.sleep(10)
    print("rede estabelecida")
    ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[2][4][0]
    print(f"novo ip: {ipv6}")
