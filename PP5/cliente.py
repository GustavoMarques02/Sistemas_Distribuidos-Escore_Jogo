import sys
import threading
import requests
import sys
import time
from socket import *
from random import randint


class Coordenador(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socketCliente = socket
        self.pilha = []
        print('Coordenador Pronto')

    def run(self):
        while True:
            (conn, addr) = self.socketCliente.accept()
            threading.Thread(
                target=self.__handling_connection(conn, addr)).start()

    def __handling_connection(self, conn, addr):
        id = conn.recv(1024)
        while True:
            if len(self.pilha) != 0:
                self.pilha.append(id)
                print('Cliente ' + str(id) + ' adicionado na pilha')
                while True:
                    if id not in self.pilha:
                        break
            conn.send('OK'.encode())
            aux = conn.recv(1024)
            if len(self.pilha) != 0:
                del self.pilha[0]
            break
        conn.close()


class Cliente:

    def __init__(self):
        self.id = sys.argv[1]

        if len(sys.argv) == 3 and sys.argv[2] == 'Coordenador':
            socketCliente = socket(AF_INET, SOCK_STREAM)
            socketCliente.bind(('172.31.95.205', 6002))
            socketCliente.listen(10)
            coordenador = Coordenador(socketCliente)
            coordenador.start()

        url = 'http://172.31.82.61:6001/jogo/escore'

        while True:
            socketServidor = socket(AF_INET, SOCK_STREAM)
            try:
                socketServidor.connect(('172.31.95.205', 6002))
            except:
                print("Host nao encontrado!")
                exit(1)

            socketServidor.send(str(id).encode())
            confirmacao = socketServidor.recv(1024)
            if confirmacao.decode() == 'OK':
                operacao = randint(0, 1)
                if operacao == 0:
                    resposta = requests.get(url).text
                    print("Escore Atual: " + resposta)
                elif operacao == 1:
                    resposta = int(requests.get(url).text)
                    novoEscore = resposta + randint(1, 10)
                    requests.post(url + '/' + str(novoEscore))
                    print("Novo Escore: " + str(novoEscore))
                socketServidor.send('Finalizado'.encode())
            socketServidor.close()
            time.sleep(randint(1, 2))


if __name__ == '__main__':
    c = Cliente()
