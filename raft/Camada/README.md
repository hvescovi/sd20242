# Teste - Raft

## Link do Repositório utilizado para testar o Raft (escrito em GO):
```
https://github.com/lni/dragonboat-example
```

## Teste
Testamos o primeiro exemplo disponibilizado, que é o que possui a estrtura mais simples, focado em configurar os nós e o grupo como um todo.

Comandos
```
cd $HOME/src/dragonboat-example
make helloworld
./example-helloworld -replicaid 1
./example-helloworld -replicaid 2
./example-helloworld -replicaid 3
```
E envio de mensagens.

Resultado
![Captura de tela de 2024-11-13 20-09-18](https://github.com/user-attachments/assets/9d3b79a9-7911-49d8-8a16-3d3002d3e750)

Comandos <br/>
Remoção do nó 3 (Ctrl + C). --> Problemas

Resultado
![Captura de tela de 2024-11-13 20-09-52](https://github.com/user-attachments/assets/84bbaf3c-4d76-4ce2-9490-ab6b4a6c0250)

Comandos <br/>
Retorno do nó 3. --> Recebe as mensagens antigas e os problemas param

Resultado
![Captura de tela de 2024-11-13 20-11-20](https://github.com/user-attachments/assets/160d08c9-035b-4340-b234-ca6af368d4cd)



