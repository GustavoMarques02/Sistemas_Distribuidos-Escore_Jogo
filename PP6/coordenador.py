from socket import *
import threading


class Coordenador(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.socketCliente = socket(AF_INET, SOCK_STREAM)
        self.socketCliente.bind((ip, 6002))
        self.socketCliente.listen(3)
        self.pilha = []
        self.lock = False
        print('Coordenador Pronto')

    def run(self):
        while True:
            (conn, addr) = self.socketCliente.accept()
            threading.Thread(
                target=self.__handling_connection, args=(conn)).start()

    def __handling_connection(self, conn):
        id = conn.recv(1024).decode()
        if self.lock:
            self.pilha.append(id)
            print('Processo ' + id + ' adicionado na pilha')
            while True:
                if id not in self.pilha:
                    print('Processo ' + id + ' saiu da pilha')
                    break
        self.lock = True
        conn.send('OK'.encode())
        conn.recv(1024)
        conn.close()
        self.lock = False
        if len(self.pilha) != 0:
            del self.pilha[0]
