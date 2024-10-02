import socket
import os
import zipfile

def zip_pasta(caminho_pasta, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, _, arquivos in os.walk(caminho_pasta):
            for arquivo in arquivos:
                caminho_completo = os.path.join(raiz, arquivo)
                zipf.write(caminho_completo, os.path.relpath(caminho_completo, os.path.dirname(caminho_pasta)))

def servidor():
    caminho_arquivo = input("Digite o caminho do arquivo ou pasta para enviar: ")
    
    # Verifica se o caminho é um diretório
    if os.path.isdir(caminho_arquivo):
        nome_zip = os.path.basename(caminho_arquivo) + '.zip'
        zip_pasta(caminho_arquivo, nome_zip)
        caminho_arquivo = nome_zip  # Atualiza o caminho para o arquivo zipado

    if not os.path.isfile(caminho_arquivo):
        print("Erro: Arquivo não encontrado.")
        return

    porta = int(input("Digite a porta: "))
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        servidor_socket.bind(('0.0.0.0', porta))
        servidor_socket.listen(1)
        print(f"Servidor ouvindo na porta {porta}...")

        cliente_socket, endereco_cliente = servidor_socket.accept()
        print(f"Conectado a {endereco_cliente}")

        nome_arquivo = os.path.basename(caminho_arquivo)
        cliente_socket.sendall(nome_arquivo.encode())

        with open(caminho_arquivo, 'rb') as arquivo:
            while True:
                dados = arquivo.read(1024)
                if not dados:
                    break
                cliente_socket.sendall(dados)

        print("Arquivo enviado com sucesso.")

    except socket.error as e:
        print(f"Erro de socket: {e}")

    finally:
        cliente_socket.close()
        servidor_socket.close()

servidor()
