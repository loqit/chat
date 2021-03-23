import socket
import os
import threading
import queue
import sys
import random

# Users Ports 2000 - 5000
# Server Ports 6000 - 10000

# Client Side
def receive_data(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

def send_data(sock, server, name):
    try:
        while True:
            data = input()
            if data == '\q':
                msg = '{} left chat!'.format(name)
                sock.sendto(msg.encode('utf-8'), server)
                break
            elif data=='':
                continue
            data = name + ': ' + data
            sock.sendto(data.encode('utf-8'), server)
        sock.close()
        os._exit(1)
    except:
        pass


def run_client(server_id):

    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000,10000)

    print('Client IP-> ' + str(host) + ' Port-> ' + str(port))
    server = (host, int(server_id))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    name = input('Please write your name here: ')
    if name == '':
        name = 'Guest'+str(random.randint(1000,9999))
        print('Your name is:' + name)

    s.sendto(name.encode('utf-8'), server)
    
    print('Please, wait for access...')
    
    access, addrws = s.recvfrom(1024)
    if access.decode('utf-8') != 'y':
        print('Access denied')
        os._exit(1)
    else: 
        msg = '{} joined!'.format(name)
        s.sendto(msg.encode('utf-8'), server)

    threading.Thread(target=receive_data, args=(s,)).start()
    threading.Thread(target=send_data, args=(s, server, name,)).start()


# Server Side
def recv_data(sock, recv_packets):
    while True:
        data,addr = sock.recvfrom(1024)
        recv_packets.put((data,addr))


def handle(sock, recv_packets, clients):
    while True:
        while not recv_packets.empty():
            data,addr = recv_packets.get()

            if addr not in clients :
                access = input('Allow {} to join chat? [y/n]'.format(data.decode('utf-8')))
                sock.sendto(access.encode('utf-8'), addr)
                if access == 'y':
                    clients.add(addr)
                continue

            clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('\q'):
                clients.remove(addr)
                continue
            for client in clients:
                if client != addr:
                    sock.sendto(data.encode('utf-8'), client)
    sock.close()


def run_server():
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(2000,5000)

    print('Server hosting on Port-> ' + str(port))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    clients = set()
    recv_packets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=recv_data,args=(s, recv_packets)).start()
    threading.Thread(target=handle,args=(s, recv_packets, clients)).start()
    run_client(port)
    

if __name__ == '__main__':
    
    if len(sys.argv)==1:
        os.system('clear')
        run_server()

    elif len(sys.argv)==2:
        os.system('clear')
        run_client(sys.argv[1])
    else:
        print('Create chat room:-> python Chat.py')
        print('Connect to exists chat:-> python Chat.py <Port>')