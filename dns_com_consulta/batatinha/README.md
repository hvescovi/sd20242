# BCC-Sistemas-Distribuidos

# :sweet_potato: Serviço de Nome - Batatinha
- Adicionado um array de servidores que faz com que cada pesquisa enviada pelo client procure em todos os servidores especificados no array.
- Testado e funcionando:
    * Servidor procura em mais de um servidor.
    * Se uma réplica parar, a outra responde com o arquivo encontrado.

- Adicionado a busca por conteúdo de arquivo
    * Se na requisição for passado a flag isFileName como 's' o servidor busca pelo nome do arquivo
    * Se na requisição for passado a flag isFileName como 'n' o servidor busca pelo conteúdo do arquivo