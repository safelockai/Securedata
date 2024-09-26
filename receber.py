import socket
import os
import subprocess
import time

def cliente():
    dominio_servidor = "serveo.net"
    porta = int(input("Digite a porta: "))
    caminho_arquivo = input("Digite o diretório para salvar o arquivo recebido (ex: /data/data/com.termux/files/home/): ")

    # Verifica se o diretório existe
    if not os.path.exists(caminho_arquivo):
        print("O diretório especificado não existe.")
        return

    # Executa o comando SSH para criar a conexão externa
    try:
        subprocess.Popen(f"ssh -R {porta}:localhost:{porta} serveo.net", shell=True)
        print(f"Conexão externa estabelecida na porta {porta} através de {dominio_servidor}.")
        time.sleep(2)  # Atraso de 2 segundos para garantir que o SSH esteja ativo
    except Exception as e:
        print(f"Erro ao estabelecer conexão SSH: {e}")
        return

    # Resolve o IP do domínio serveo.net
    try:
        endereco_ip = socket.gethostbyname(dominio_servidor)
    except socket.error as e:
        print(f"Erro ao resolver o domínio {dominio_servidor}: {e}")
        return

    # Cria o socket do cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tenta conectar repetidamente até um limite de tentativas
    tentativas = 5
    for tentativa in range(tentativas):
        try:
            cliente_socket.connect((endereco_ip, porta))
            print("Conexão estabelecida. Recebendo o arquivo...")
            break  # Sai do loop se a conexão for bem-sucedida
        except socket.error as e:
            print(f"Tentativa {tentativa + 1} de conectar ao servidor falhou: {e}")
            time.sleep(2)  # Espera 2 segundos antes da próxima tentativa

    else:
        print("Falha ao conectar ao servidor após várias tentativas.")
        return

    # Recebe o nome do arquivo e monta o caminho completo
    nome_arquivo = cliente_socket.recv(1024).decode()
    caminho_arquivo_completo = os.path.join(caminho_arquivo, nome_arquivo)

    # Verifica se o arquivo já existe
    if os.path.exists(caminho_arquivo_completo):
        sobrescrever = input(f"O arquivo {nome_arquivo} já existe. Deseja sobrescrevê-lo? (s/n): ")
        if sobrescrever.lower() != 's':
            print("Recepção de arquivo cancelada.")
            return

    # Recebe e salva o arquivo
    with open(caminho_arquivo_completo, 'wb') as arquivo:
        while True:
            dados = cliente_socket.recv(1024)
            if not dados:
                break
            arquivo.write(dados)

    # Exibe a mensagem no terminal informando que o arquivo foi recebido com sucesso
    print(f"Arquivo '{nome_arquivo}' recebido com sucesso.")

    # Fecha a conexão
    cliente_socket.close()

# Chama a função para iniciar o cliente
cliente()
