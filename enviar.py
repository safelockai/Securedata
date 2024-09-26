import socket
import os

def servidor():
    # Solicita as informações do usuário
    caminho_arquivo = input("Digite o caminho do arquivo para enviar: ")
    if not os.path.isfile(caminho_arquivo):
        print("Erro: Arquivo não encontrado.")
        return

    porta = int(input("Digite a porta: "))

    # Domínio padrão do cliente
    dominio_cliente = "serveo.net"

    # Cria o socket do servidor
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        servidor_socket.bind(('0.0.0.0', porta))  # Escuta em todas as interfaces
        servidor_socket.listen(1)
        print(f"Servidor ouvindo na porta {porta}...")
        
        # Aceita a conexão do cliente
        cliente_socket, endereco_cliente = servidor_socket.accept()
        print(f"Conectado a {endereco_cliente} (domínio: {dominio_cliente})")
        
        # Envia o nome do arquivo
        nome_arquivo = os.path.basename(caminho_arquivo)
        cliente_socket.sendall(nome_arquivo.encode())
        
        # Envia o arquivo
        with open(caminho_arquivo, 'rb') as arquivo:
            while (dados := arquivo.read(1024)):
                cliente_socket.sendall(dados)

        print("Arquivo enviado com sucesso.")
        
    except socket.error as e:
        print(f"Erro de socket: {e}")
    
    finally:
        # Fecha as conexões
        cliente_socket.close()
        servidor_socket.close()

# Chama a função para iniciar o servidor
servidor()
