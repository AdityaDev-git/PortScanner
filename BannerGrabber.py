import socket

# s = socket.socket()
# ip = input("enter ip: ")
# port = str(input("enter port: "))
# s.connect((ip, int(port)))
# print(s.recv(1024))

def banner (ip,port):
    s = socket.socket()
    s.connect((ip, int(port)))
    s.settimeout(5)
    print(s.recv(1024))

def main():
    ip = input("enter ip: ")
    port = str(input("enter port: "))
    banner(ip, port)

main()