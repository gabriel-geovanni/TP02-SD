
import os
import re
import socket
import subprocess
from datetime import datetime, timedelta
from time import sleep


class Clients:
    def __init__(self, name, client, address):
        self.name = name
        self.client = client
        self.address = address


class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '192.168.2.132'
        self.port = 3333
        self.buffer = 1024

def init():
    server = Server()

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Iniciando servidor de sincronização de relógio\nAlgoritmo de Cristian\nHost: %s  Porta: %s" % (server.host, server.port))
    server.sock.bind((server.host, server.port))
    server.sock.listen()


    while True:
        clients = []
        i=0
        print ('\nAguardando conexão com clients... ')
        while i < 2:
            client, address = server.sock.accept() 
            data = client.recv(server.buffer) 
            clientName = data.decode('utf-8')
            print("Cliente se conectou.\nNome: {}\n".format(clientName))
            clients.append(Clients(clientName, client, address))
            i+=1

        try:
            while True:
                for client in clients:
                    pingClient = ping(client.address[0])
                    pings = re.search(r'time=(\d+\.\d+) ms', pingClient)
                    timePing = timedelta(days=0, hours=0,minutes=0,seconds=0,milliseconds=float(pings.group(1)))

                    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')
                    serverHourWithPingDelay = (datetime.now() + timePing).strftime('%Y-%m-%d %H:%M:%S.%f')
                    client.client.send(serverHourWithPingDelay.encode('utf-8'))
                    print('\nCliente: {}'.format(client.name))
                    print('Hora atual do servidor: ', now,'\nDelay PING: ',float(pings.group(1)), 'ms\nHora enviada para o cliente: ', serverHourWithPingDelay)

                sleep(1)

        except Exception:  
            print("Cliente desconectado")
            
             
def ping(address):
    p = subprocess.run(['ping', '-c', '4', address], stdout=subprocess.PIPE)

    stdout = p.stdout

    return stdout.decode('UTF-8') if p.returncode == 0 else ''
    
    

init()