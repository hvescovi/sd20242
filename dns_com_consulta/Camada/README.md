separador.py -> Separa os valores encontrados no banco (arquivo .csv) em arquivos de texto divididos entre pastas de 0 a 9. Você deve colocar o arquivo .csv na pasta da aplicação, criar uma pasta out e por último rodar o programa separador.py. Você obterá algo assim:
<p align="center">
  <img src="https://github.com/user-attachments/assets/ad0e627e-937e-4f6b-99b2-3875c142a139">
</p>

server.py -> Roda o servidor da aplicação. Contém a lógica para procurar o nome de um arquivo em três pastas, que são definidas inserindo, na versão atual, três parâmetros ao rodar o programa, ou procurar um atributo dentro dos arquivos das três pastas. Ex.: Para que o programa procure dentro das pastas 0, 1 e 2, o comando deve ser: `python3 server.py 0 1 2`, assim como na imagem abaixo:
<p align="center">
  <img src="https://github.com/user-attachments/assets/df6e9b57-4095-4a15-8517-258078bd9d12">
</p>

client.py -> Roda um cliente para a aplicação. Espera que o usuário digite um nome de arquivo para ser procurado ou atributos para serem procurado dentro dos arquivos. Na próxima imagem, vemos o resultado da procura pelo arquivo zumba:

<p align="center">
  <img src="https://github.com/user-attachments/assets/1cd03997-d2ff-4c3e-a866-c70aa34230e3">
</p>

Na imagem seguinte, vemos a execução do cliente e o resultado da solicitação de procura pelo atributo china, encontrado em vários arquivos, que foram retornados:

<p align="center">
  <img src="https://github.com/user-attachments/assets/ac86d82c-c8eb-49d1-823a-a53e46760365">
</p>

Agora, pegamos todo o conteúdo que está dentro do arquivo zte, que é este:

<p align="center">
  <img src="https://github.com/user-attachments/assets/abc4ebc7-f51f-43b9-aa51-8b4c65d972bc">
</p>

E fazemos a busca com isso tudo, para, assim, obter como resposta apenas um arquivo, que foi o próprio zte:
<p align="center">
  <img src="https://github.com/user-attachments/assets/1b593545-307c-4284-94a8-4db62d030c89">
</p>
