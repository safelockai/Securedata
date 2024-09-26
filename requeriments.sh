#!/bin/bash

# Atualiza o repositório e pacotes
pkg update && pkg upgrade -y

# Instala o Python e pip se não estiverem instalados
pkg install -y python python-pip

# Informa ao usuário que a instalação foi concluída
echo "Instalação concluída."
echo "Siga @Safelockai no Instagram."
