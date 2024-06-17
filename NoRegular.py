import hashlib
import socket
import threading
import os
import time

CURRENT_FOLDER = os.getcwd()
PATH = f'{CURRENT_FOLDER}/shared'
BORDER_NODE_IP = "192.168.0.154"

def calculate_checksum(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def receive_messages(sock):
    while True:
        try:
            # Recebe mensagens do servidor
            response = sock.recv(1024).decode('utf-8')
            print(f"[SERVER]: {response}")
        except ConnectionResetError:
            print("Servidor fechou a conexão.")
            break

def list_files_in_folder():
    files_info = []
    if not os.path.exists(PATH):
        try:
            os.makedirs(PATH)  # Tenta criar o diretório se não existir
            print(f"Pasta '{PATH}' criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar pasta '{PATH}': {e}")
            return []

    for root, _, filenames in os.walk(PATH):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            size = os.path.getsize(file_path)
            checksum = calculate_checksum(file_path)
            files_info.append({
                'filename': filename,
                'checksum': checksum,
                'size': size
            })

    return files_info

def handle_border_node(client_socket, ip):
    while True:
        try:
            client_socket.send(str(list_files_in_folder()).encode())
            # client_socket.send(('Hello').encode())
            client_socket.close()
            break
        except ConnectionResetError:
            break

def node_server():
    #Esse server e somente para se comunicar com os outros nos
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("0.0.0.0", 9998))
    listener.listen(1)
    print('Aberto a conexoes...')
    while True:
        client_socket, addr = listener.accept()
        print(f"Conexão aceita de: {addr[0]}")
        if addr[0] == BORDER_NODE_IP:
            client_handler = threading.Thread(target=handle_border_node, args=(client_socket, addr[0]))
            client_handler.start()


def main():
    threading.Thread(target=node_server, args=()).start()
    time.sleep(3)
    #Conectando ao no de borda
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((BORDER_NODE_IP, 9999))
    
    client.send(('handshake').encode())
    start_time = time.time()
    while True:
        if client.recv(1024).decode() == 'ack':
            break
        elif time.time() - start_time > 15:
            print('Timeout! Encerrando conexao')
            client.close()
            exit(1)

    print("Conectado ao servidor.")

    # Thread para receber mensagens do servidor
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.start()
    listFiles = list_files_in_folder()
    print(listFiles)
    while True:

        message = input()
        client.send((message).encode('utf-8'))
        # client.close()
        # print("Conexão fechada com o servidor.")

if __name__ == "__main__":
    main()