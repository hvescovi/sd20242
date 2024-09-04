# importar a biblioteca flask
from flask import Flask, request, jsonify
# biblioteca CORS
from flask_cors import CORS
import os

from config import *
from file import *
import random

SERVER_DIR = "./files/"
File.create_table('file')

# acesso ao flask via variável app
app = Flask(__name__)

# inserindo a aplicação em um contexto
# https://flask.palletsprojects.com/en/2.2.x/appcontext
with app.app_context():

    # aplicando tratamento CORS ao flask
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

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
                file = File.get(File.id == entry.name)
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
            uid = str(random.getrandbits(32))

            newFile = open(SERVER_DIR + uid, "x")
            newFile.close()

            entry = os.stat(SERVER_DIR + uid)
            
            file = File.create(name=file_name, id=int(uid), modified=entry.st_mtime)
            file.save()

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
            requestContent = request.json
            fileName = requestContent.get('fileName')
            fileContent = requestContent.get('fileContent')
            
            print(fileName)
            file = File.get(File.name == fileName)
            openedFile = open(SERVER_DIR + str(file.id), "w")
            conteudo = openedFile.write(fileContent)
            openedFile.close()
            
            # f.save(SERVER_DIR + f.filename)
            resposta = jsonify({"header": "OK", "detail": "success!", "content": conteudo})
        
        except Exception as e:
            resposta = jsonify({"header": "erro", "detail": str(e), "content": "Deu erro irmãozao"})
        
        return resposta

    @app.route("/ler/<file_name>")
    def ler(file_name):
        try:
            fileName = File.get(File.name == file_name)
            openedFile = open(SERVER_DIR + str(fileName.id), "r")
            conteudo = openedFile.read()
            openedFile.close()
            resposta = jsonify({"header": "OK", "detail": conteudo})
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
