from flask import Flask
from flask import request

app = Flask(__name__)


class Jogo:
    def __init__(self):
        self.escore = 0


@app.route('/jogo/escore', methods=['GET'])
def getEscore():
    return str(j.escore)


@app.route('/jogo/escore/<novoEscore>', methods=['POST'])
def setEscore(novoEscore):
    j.escore = int(novoEscore)
    return 'OK'


if __name__ == '__main__':
    j = Jogo()
    app.run(host='172.31.82.61', port='6001')
