
# import socket programming library 
import socket 
import signal
import sys
from struct import unpack
# import thread module 
import threading, queue
  
s = None
udp_sock = None
clients_q = []
Uclients_q = {}

def send_to_all(message, clients_queues):
    for q in clients_queues:
        q.put(message)
def Usend_to_all(message, client_ids):
    for name in client_ids:
        Uclients_q[name].put(message)


def client_receiver(c, q, who):
    global clients_q
    while True:
        data = c.recv(1024)
        if not data:
            print("end of connection")
            clients_q.remove(q)
            break        
        name = str(who)
        mess = str(data.decode('utf-8'))
        print(f'received data from {name} : {mess}')
        send_to_all(f'{name}: {mess}'.encode('utf-8'), filter(lambda q1: q1 != q, clients_q))
        if not data: 
            print('Bye') 
def Uclient_receiver(s):
    global Uclients_q
    while True:
        try:
            data, addr = s.recvfrom(1024)
            if not data or (len(data) == 4 and unpack('i', data)[0] == -1) :
                print("Uend of connection")
                break        
            name = str(addr[1])
            mess = str(data.decode('utf-8'))
            print(f'received udp data from {name} : ...')
            Usend_to_all(f'U{name}: {mess}'.encode('utf-8'), filter(lambda a: str(a) !=name , Uclients_q.keys()))
            if not data: 
                print('Bye') 
        except UnicodeDecodeError:
            print("couldn't decode")
            pass
def client_sender(c, q): 
    while True: 
        message = q.get()
        print(f'sending \"{str(message.decode("utf-8"))}\" to {c.getpeername()[1]}')
        c.send(message) 

def Uclient_sender(s, p, q): 
    while True: 
        message = q.get()
        print(f'sending UDP \"...\" to {p}')
        s.sendto(message, ("127.0.0.1", p))   
    # connection closed 
    c.close() 
  
def ctrlc_handler(sig, frame):
    print("exiting")
    s.close()
    udp_sock.close()
    sys.exit(0)

def Main(): 
    global s
    global udp_sock
    host = "" 
    port = 12345

    signal.signal(signal.SIGINT, ctrlc_handler)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
  
    s.listen() 
    print("listening") 
    
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("127.0.0.1", port))
    threading.Thread(target=Uclient_receiver, args=(udp_sock,), daemon=True).start()

    while True: 
  
        c, addr = s.accept() 
        
        print('Connected to :', addr[0], ':', addr[1]) 
  
        q = queue.Queue()
        clients_q.append(q)
        uq = queue.Queue()
        Uclients_q[addr[1]] = uq
        
        threading.Thread(target=client_receiver, args=(c,q, addr[1]), daemon=True).start()
        threading.Thread(target=client_sender, args=(c,q), daemon=True).start()
        threading.Thread(target=Uclient_sender, args=(udp_sock, addr[1], uq), daemon=True).start()
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 
