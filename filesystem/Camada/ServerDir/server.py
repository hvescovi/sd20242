# importar a biblioteca flask
from flask import Flask, request, jsonify
# biblioteca CORS
from flask_cors import CORS
import os
import uuid
import json

# Tabela para mapear nomes de arquivos para UFIDs
file_mapping = {}

# Adicionando uma função para gerar um UFID
def generate_ufid():
    return str(uuid.uuid4())

# o arquivo file_mapping.json mapeia nomes de arquivos para UFIDs
# função para salvar no arquivo json
def save_file_mapping():
    with open(SERVER_DIR + 'file_mapping.json', 'w') as f:
        json.dump(file_mapping, f)

# função para carregar o arquivo json
def load_file_mapping():
    global file_mapping
    try:
        with open(SERVER_DIR + 'file_mapping.json', 'r') as f:
            file_mapping = json.load(f)
    except FileNotFoundError:
        # caso o arquivo não exista, o dicionário começa vazio
        file_mapping = {}

SERVER_DIR = "./files/"

class File:
    # construtor com valor padrão nos parâmetros
    def __init__(self, name="", id="", modified=""):
        self.name = name
        self.id = id
        self.modified = modified

    # expressar a classe em formato texto
    def __str__(self):
        return f'{self.name}, '+\
               f'{self.id}, {self.modified}'

    # expressar a classe em formato json
    def json(self):
        return {
            "name" : self.name,
            "id" : self.id,
            "modified" : self.modified 
        }

# acesso ao flask via variável app
app = Flask(__name__)

# inserindo a aplicação em um contexto
# https://flask.palletsprojects.com/en/2.2.x/appcontext
with app.app_context():

    # aplicando tratamento CORS ao flask
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

    load_file_mapping()

    # rota padrão
    @app.route("/")
    def ola():
        return "<b>Olá, gente!</b>"

    # rota de listar pessoas
    @app.route("/listar")
    def listar():
        try:
            # cria a lista de retorno que sera usadada para gerar o json
            lista_retorno = []
            # obtem lista dos arquivos do diretŕio atual
            dirEntrys = os.scandir(SERVER_DIR)
            lista = []
            # percorre a lista de entradas
            for entry in dirEntrys:
                # obtem status referente ao arquivo e grava na lista
                fileStatus = entry.stat()
                file = File(entry.name, fileStatus.st_ino, fileStatus.st_mtime)
                print(file)
                lista.append(file)


            # percorrer a lista de arquivos e tranforma em json
            for file in lista:
                lista_retorno.append(file.json())

            # preparar uma parte da resposta: resultado ok
            meujson = {"header":"OK"}

            meujson.update({"files":lista_retorno})

            # retornar a lista de pessoas json, com resultado ok
            resposta = meujson

            # trate corretamente esse erro
        except Exception as e: 
            resposta = jsonify({"header": "erro", "files": str(e)})

        return resposta

    @app.route("/criar/<file_name>")
    def criar(file_name):
        try:
            newFile = open(SERVER_DIR + file_name, "x")
            newFile.close()
            entry = os.stat(SERVER_DIR + file_name)
            file = File(file_name, entry.st_ino, entry.st_mtime)
            resposta = jsonify({"header": "OK", "file": file.json()})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})

        return resposta

    @app.route("/deletar/<file_name>")
    def deletar(file_name):
        try:
            os.remove(SERVER_DIR + file_name)
            resposta = jsonify({"header": "OK", "deatil": file_name + ' deleted'})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})

        return resposta

    # Rota antiga - usando método GET
    @app.route("/escrever_antigo/<file_name>/<conteudo>")
    def escrever_antigo(file_name, conteudo):
        try:
            openedFile = open(SERVER_DIR + file_name, "w")
            openedFile.write(conteudo)
            openedFile.close()
            print(conteudo)
            resposta = jsonify({"header": "OK", "detail": "success!"})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})
        return resposta
    
    # Para testar a rota: curl -i -X POST -F files=@nome_arquivo http://127.0.0.1:5000/escrever
    @app.route("/escrever", methods=['POST'])
    def escrever():
        try:
            f = request.files['files']

            original_filename = f.filename

            # Gerar UFID
            ufid = generate_ufid()

            # Salvar o arquivo com o nome do UFID
            # print(f.filename)
            #f.save(SERVER_DIR + f.filename)
            f.save(SERVER_DIR + ufid)

            # Mapear o nome original do arquivo para o UFID
            # atualiza o mapeamento em disco
            file_mapping[original_filename] = ufid
            
            save_file_mapping()

            resposta = jsonify({"header": "OK", "detail": "success!", "ufid": ufid})
        
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})
        
        return resposta

    @app.route("/ler/<file_name>")
    def ler(file_name):
        try:
            # Recuperar o UFID correspondente ao nome do arquivo
            ufid = file_mapping.get(file_name)

            if ufid is None:
                raise Exception("File not found")
            
            # Abrir e ler o arquivo usando o UFID
            openedFile = open(SERVER_DIR + ufid, "r")
            # poderia ser with open(SERVER_DIR + ufid, "r") as openedFile:
            conteudo = openedFile.read()

            openedFile.close()
            resposta = jsonify({"header": "OK", "detail": conteudo})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})
        return resposta
    
    @app.route("/listar_arquivos")
    def listar_arquivos():
        try:
            # Preparar a resposta com o mapeamento de arquivos
            resposta = jsonify({"header": "OK", "files": file_mapping})
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e)})
        return resposta

    app.run(debug=True, host='0.0.0.0')
    # para depurar a aplicação web no VSCode, é preciso remover debug=True
    # https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app


'''
resultado da invocação ao servidor:

curl localhost:5000/listar


'''
