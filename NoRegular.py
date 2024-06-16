# Exemplo simplificado de um nó regular (cliente P2P)

import socket
import os
import hashlib
import threading

HOST = 'localhost'
PORT = 12345  # Porta do servidor de borda

# Função para calcular o checksum MD5 de um arquivo
def calculate_checksum(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Função para lidar com o envio de um arquivo para o servidor de borda
def send_file_to_edge_server(filename):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        # Envia o nome do arquivo primeiro
        s.send(filename.encode())

        # Abre o arquivo para leitura binária
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                s.sendall(data)

        print(f"Arquivo '{filename}' enviado com sucesso para o servidor de borda.")

    except Exception as e:
        print(f"Erro ao enviar arquivo '{filename}' para o servidor de borda: {e}")

    finally:
        s.close()

# Exemplo de uso
if __name__ == "__main__":
    filenames = ['arquivo1.txt', 'video.mp4', 'imagem.jpg']  # Exemplo de lista de arquivos
    for filename in filenames:
        checksum = calculate_checksum(filename)
        print(f"Checksum do arquivo '{filename}': {checksum}")

        # Envia o arquivo para o servidor de borda em uma thread separada
        thread = threading.Thread(target=send_file_to_edge_server, args=(filename,))
        thread.start()
