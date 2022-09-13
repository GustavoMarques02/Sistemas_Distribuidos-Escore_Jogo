import threading
import requests
import sys
import time
import const
from socket import *
from random import randint
from coordenador import Coordenador


class Cliente:

    def __init__(self):
        self.id = sys.argv[1]
        self.coordIp = const.registry['1']
        self.eleicao = False
        self.url = 'http://' + const.SERVER_HOST + \
            ':' + const.SERVER_PORT + '/jogo/escore'

        if sys.argv[1] == '1':
            coordenador = Coordenador(self.coordIp)
            coordenador.start()

        threading.Thread(target=self.esperarMensagem).start()

        while True:
            if not self.eleicao:
                socketServidor = socket(AF_INET, SOCK_STREAM)
                try:
                    socketServidor.connect((self.coordIp, 6002))
                    socketServidor.send(self.id.encode())
                    confirmacao = socketServidor.recv(1024)
                    if confirmacao.decode() == 'OK':
                        time.sleep(3)
                        operacao = randint(0, 1)
                        if operacao == 0:
                            resposta = requests.get(self.url).text
                            print("Escore Atual: " + resposta)
                        elif operacao == 1:
                            resposta = int(requests.get(self.url).text)
                            novoEscore = resposta + randint(1, 10)
                            requests.post(self.url + '/' + str(novoEscore))
                            print("Novo Escore: " + str(novoEscore))
                        socketServidor.send('Finalizado'.encode())

                    socketServidor.close()
                except:
                    print("Coordenador nao respondeu!")
                    self.fazerEleicao()

    def fazerEleicao(self):
        self.eleicao = True
        print('Iniciando eleicao por bullying')
        eleito = True

        for id in range(int(self.id) + 1, 4):
            socketEleicao = socket(AF_INET, SOCK_STREAM)
            ip = const.registry[str(id)]
            try:
                socketEleicao.connect((ip, 6003))
                socketEleicao.send('ELECTION'.encode())
                confirmacao = socketEleicao.recv(1024)
                if confirmacao == 'OK':
                    eleito = False
            except:
                print('Processo ' + str[id] + ' nao encontrado')
            finally:
                socketEleicao.close()

        if eleito:
            self.coordIp = const.registry[self.id]
            coordenador = Coordenador(self.coordIp)
            coordenador.start()
            self.eleicao = False

            print('Enviando meu ip como novo coordenador')
            for id in range(1, 4):
                socketNovoCoord = socket(AF_INET, SOCK_STREAM)
                ip = const.registry[str(id)]
                try:
                    socketNovoCoord.connect((ip, 6003))
                    socketNovoCoord.send(self.coordIp.encode())
                except:
                    print('Processo ' + str[id] + ' nao encontrado')
                finally:
                    socketNovoCoord.close()
        else:
            print('Esperando eleicao terminar')

    def esperarMensagem(self):
        socketMensagem = socket(AF_INET, SOCK_STREAM)
        socketMensagem.bind((const.registry[self.id], 6003))
        socketMensagem.listen(3)
        while True:
            (conn, addr) = socketMensagem.accept()
            mensagem = conn.recv(1024)
            if mensagem == 'ELECTION' and not self.eleicao:
                print('Mensagem de eleicao recebida')
                self.eleicao = True
                conn.send('OK'.encode())
                self.fazerEleicao()
            elif mensagem in const.registry.values():
                self.coordIp = mensagem
                self.eleicao = False
                print('Novo coordenador recebido')
            conn.close()


if __name__ == '__main__':
    c = Cliente()
