#This is the heart og the program help us connect and communicate between two machines.
import socket
from threading import *

class Message(Thread):  #Messsage claa extending Thread class, helps client and server send and recieve data at same time
    def __init__(self):
        Thread.__init__(self)
    def binder(self,con,name1):
        self.con=con
        self.name1=name1
    def run(self):    #Task done by new thread
        name=current_thread().getName()
        while True:
            print(name)
            if name=='sender':
                print('1.Chat')
                print('2.send file')
                choice=int(input('Choice: '))
                if(choice==1):
                    values=input("Type ")
                    values=self.name1+': '+values
                    self.con.send(bytes(values,'utf-8'))
                elif(choice==2):
                    ff=input('Give file path:')
                    file=open(ff,'r')
                    for data in file:
                        self.con.send(bytes(data,'utf-8'))
                    print('File Sent Successfully')

            elif name=='receiver':
                    recvdata = self.con.recv(1024).decode()
                    if len(recvdata)!=0:
                        print()
                        print(recvdata)
                    else:
                        break


ip=input('IPV4 Address: ')

port=int(input('Port : '))
name=socket.gethostname()
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:  # It will try to connect the perticulat peer.If peer machine is not aactive throws exception
    print('Trying connection.....')
    print(port,type)
    server.connect((ip,port))
    sender=Message()
    sender.binder(server,name)
    sender.setName('sender')
    receiver=Message()
    receiver.binder(server,name)
    receiver.setName('receiver')
    sender.start()
    receiver.start()
except Exception as e :  # Thrown acception handled here, requesting machine will act as server.
    print('Target Machine not active......')
    server.bind(('127.0.0.1', port))
    print('Waiting for connection........')
    server.listen(5)
    clt, addr=server.accept()
    print('Connection Stablished ',clt)
    sender=Message()
    sender.binder(clt,name)
    sender.setName('sender')
    receiver=Message()
    receiver.binder(clt,name)
    receiver.setName('receiver')
    sender.start()
    receiver.start()