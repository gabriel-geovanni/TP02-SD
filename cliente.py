import os
import platform
import socket
from datetime import datetime


class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '192.168.2.132'
        self.port = 3333
        self.buffer = 1024

def connect(): 
    server = Server()
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Conectando \nHost: %s   Porta: %s" % (server.host, server.port)) 
    server.sock.connect((server.host, server.port)) 
    try: 
     
        name = input('\nPara começar, \ninforme o nome do sistema: ')
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Enviando requisição para o servidor")
        server.sock.sendall('{}'.format(name).encode('utf-8'))
        
        while True:
            print('\nHora atual do sistema: ', datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f'))

            print("Aguardando sincronização do servidor...")
            data = server.sock.recv(server.buffer) 
            serverHour = data.decode('utf-8')
            
            dateNow, hourNow = serverHour.split(' ')
            year, month, day = dateNow.split('-')
            time, milliseconds = hourNow.split('.')
            hour, minute, second = time.split(':')
            print('Hora atual do servidor: \n{}-{}-{} {}:{}:{}.{}'.format(day, month, year, hour, minute, second, milliseconds))
            
            print('\nHora do sistema atualizada')
            os.system("date -s '{}-{}-{} {}:{}:{}.{}'".format(year, month,day,hour,minute,second,milliseconds))
            
            

    except Exception as e: 
        print ("Erro na execução: %s" %str(e)) 
    

   
connect()