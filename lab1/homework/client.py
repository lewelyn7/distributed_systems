import socket, threading
from _thread import *
import signal
import sys
from struct import pack

s = None
su = None
host = '127.0.0.1'
group = '224.1.1.1'
port = 12345

def receiver_thread(s):
    while True:
        data = s.recv(1024)
        if not data:
            print("end of connection")
            break
        message = str(data.decode('utf-8'))
        print(message)
        print(">", end="", flush=True)

def Ureceiver_thread(s):
    while True:
        data = s.recv(1024)
        if not data:
            print("end of connection")
            break
        message = str(data.decode('utf-8'))
        print(message)
        print(">", end="", flush=True)        

def close_connections():
    print("exiting")
    s.close()
    su.sendto(pack('!i', -1), (host, port)) 
    su.close()

def ctrlc_handler(sig, frame):
    close_connections()
    sys.exit(0)

def Main(): 
    global s,su
    signal.signal(signal.SIGINT, ctrlc_handler)
    # local host IP '127.0.0.1' 

    gport = 5004
    gttl = 2
  
    udp_payload2 = "UDP DATA"
    udp_payload = """
                             __ 
                   _ ,___,-'",-=-. 
       __,-- _ _,-'_)_  (""`'-._\ `. 
    _,'  __ |,' ,-' __)  ,-     /. | 
  ,'_,--'   |     -'  _)/         `\ 
,','      ,'       ,-'_,`           : 
,'     ,-'       ,(,-(              : 
     ,'       ,-' ,    _            ; 
    /        ,-._/`---'            / 
   /        (____)(----. )       ,' 
  /         (      `.__,     /\ /, 
 :           ;-.___         /__\/| 
 |         ,'      `--.      -,\ | 
 :        /            \    .__/ 
  \      (__            \    |_ 
   \       ,`-, *       /   _|,\ 
    \    ,'   `-.     ,'_,-'    \ 
   (_\,-'    ,'\")--,'-'       __\ 
    \       /  // ,'|      ,--'  `-. 
     `-.    `-/ \'  |   _,'         `. 
        `-._ /      `--'/             \ 
-hrr-      ,'           |              \ 
          /             |               \ 
       ,-'              |               / 
      /                 |             -' 
"""
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    s.connect((host,port)) 
    print("connected")
    local_port = s.getsockname()[1]
    su.bind((host, local_port))

    message = "shaurya says geeksforgeeks"
    threading.Thread(target=receiver_thread, args=(s,), daemon=True).start()
    threading.Thread(target=Ureceiver_thread, args=(su,), daemon=True).start()
    print("type message or \"exit\" to close connection:")
    print(">",end="")
    while True: 
        ans = input('') 
        try:
            if ans == 'exit': 
                break  
            # message sent to server 
            if ans[0] == "u":
                su.sendto(udp_payload.encode('utf-8'), (host, port)) 
            else:
                s.send(ans.encode('utf-8')) 
                print(">", end="", flush=True)
        except (AttributeError, IndexError):
            pass

    close_connections() 
  
if __name__ == '__main__': 
    Main() 
