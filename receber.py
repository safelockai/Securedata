import socket
import os
import subprocess
import time
import zipfile

def descompactar_arquivo(caminho_zip):
    with zipfile.ZipFile(caminho_zip, 'r') as zipf:
        zipf.extractall(os.path.dirname(caminho_zip))
        print(f"Arquivo descompactado em: {os.path.dirname(caminho_zip)}")

def cliente():
    porta = int(input("Digite a porta: "))
    caminho_arquivo = input("Digite o diretório para salvar o arquivo recebido: ")

    if not os.path.exists(caminho_arquivo):
        print("O diretório especificado não existe.")
        return

    subprocess.Popen(f"ssh -R {porta}:localhost:{porta} serveo.net", shell=True)
    time.sleep(2)

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente_socket.connect(("serveo.net", porta))
        print("Conexão estabelecida. Recebendo o arquivo...")

        nome_arquivo = cliente_socket.recv(1024).decode()
        caminho_arquivo_completo = os.path.join(caminho_arquivo, nome_arquivo)

        if os.path.exists(caminho_arquivo_completo):
            sobrescrever = input(f"O arquivo {nome_arquivo} já existe. Deseja sobrescrevê-lo? (s/n): ")
            if sobrescrever.lower() != 's':
                print("Recepção de arquivo cancelada.")
                return

        with open(caminho_arquivo_completo, 'wb') as arquivo:
            while True:
                dados = cliente_socket.recv(1024)
                if not dados:
                    break
                arquivo.write(dados)

        print(f"Arquivo '{nome_arquivo}' recebido com sucesso.")

        # Descompacta se o arquivo for um ZIP
        if nome_arquivo.endswith('.zip'):
            descompactar_arquivo(caminho_arquivo_completo)

    except socket.error as e:
        print(f"Erro de socket: {e}")

    finally:
        cliente_socket.close()

cliente()
