import requests
import time
from random import randint


class Cliente:

    def __init__(self):
        url = 'http://localhost:8080/jogo/escore'

        while True:
            operacao = randint(1, 1)
            if operacao == 0:
                resposta = requests.get(url).text
                print("Escore Atual: " + resposta)
            elif operacao == 1:
                resposta = int(requests.get(url).text)
                novoEscore = resposta + randint(1, 10)
                requests.post(url + '/' + str(novoEscore))
                print("Novo Escore: " + str(novoEscore))
            time.sleep(randint(1, 10))


if __name__ == '__main__':
    c = Cliente()
