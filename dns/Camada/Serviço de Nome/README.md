separador.py -> Separa os valores encontrados no banco (arquivo .csv) em arquivos de texto divididos entre pastas de 0 a 9. Você deve colocar o arquivo .csv na pasta da aplicação, criar uma pasta out e por último rodar o programa separador.py. Você obterá algo assim:
<p align="center">
  <img src="https://github.com/user-attachments/assets/ad0e627e-937e-4f6b-99b2-3875c142a139">
</p>

server.py -> Roda o servidor da aplicação. Contém a lógica para procurar o nome de um arquivo em duas pastas, que são definidas inserindo dois parâmetros ao rodar o programa. Ex.: Para que o programa procure dentro das pastas 0 e 1, o comando deve ser: `python3 server.py 0 1`, assim como na imagem abaixo:
<p align="center">
  <img src="https://github.com/user-attachments/assets/81172814-0538-4d2d-8e38-9769b8fb2884">
</p>

client.py -> Roda um cliente para a aplicação. Espera que o usuário digite um nome de arquivo para ser procurado. Na próxima imagem, vemos o arquivo aafes na pasta 0:

<p align="center">
  <img src="https://github.com/user-attachments/assets/fddbf160-2608-4bb3-8c07-66638cf97aa9">
</p>

Na imagem seguinte, vemos a execução do cliente e o resultado da solicitação de procura pelo arquivo aafes:

<p align="center">
  <img src="https://github.com/user-attachments/assets/7918bf0f-f70e-40e3-baaa-ba5613d58f7c">
</p>
