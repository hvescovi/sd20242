import os

SOURCE_FILE_NAME = "companies_sorted.csv"                               # Endereço do arquivo para particionamento e armazenamento em arquivos de texto
OUT_PATH = "./out/"
N_DIR = 1200                                                            # Quantidade de diretórios para o particionamento

n_files = 0                                                             # Quantidade máxima de arquivos em cada diretório - calculado pelo programa
count = 0                                                               # Variável de controle para indíce de particionamento
dir_content = []                                                        # Armazena o conteúdo de cada diretório em sublistas. Cada sublista armazena as entradas do diretório


with open(SOURCE_FILE_NAME, "r") as file:                               # Ler arquivo
    lines = file.readlines()[1:]                                        # Armazenar linhas - a partir da segunda - do arquivo em lista. TODO: Melhorar a abordagem para arquivos extensos
    n_files = int(len(lines)/N_DIR)                                     # Calcular a quantidade máxima de arquivos por diretório

    for i in range(10):                                      
        if i == N_DIR-1:                                                # Se for o último diretório, deve consumir até a última ocorrência
            dir_content.append(lines[count:])                           # Adicionar sublista com conteúdo do diretório
        else:
            dir_content.append(lines[count:count+n_files])
            count += n_files+1

contador_erro = 0    
for i in range(len(dir_content)):
    
    if not os.path.exists(OUT_PATH + str(i)):
        os.mkdir(OUT_PATH + str(i))
    
    for j in range(len(dir_content[i])):
        atributos = dir_content[i][j].split(',')
        try:
            f = open(f"{OUT_PATH}{i}/{atributos[1].replace('/','')}", "w")
            f.writelines(dir_content[i][j])
        except:
            #print("erro ao tentar criar: " + atributos[1])
            contador_erro = contador_erro + 1

print("Total de erros: " + str(contador_erro))