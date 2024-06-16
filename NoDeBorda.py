# Exemplo de nó de borda atualizado para uma rede P2P

import socket
import threading

HOST = 'localhost'
PORT = 12345  # Porta para comunicação com os nós regulares

# Dicionário para armazenar informações sobre os nós regulares
nodes = {}  # Chave: endereço do nó, Valor: lista de arquivos que o nó possui

# Função para lidar com a conexão de um nó regular (cliente P2P)
def handle_node_connection(conn, addr):
    print(f"Conexão estabelecida com nó regular {addr}")

    try:
        while True:
            # Recebe o nome do arquivo do nó regular
            filename = conn.recv(1024).decode()
            if not filename:
                break

            print(f"Recebido pedido de arquivo '{filename}' de {addr}")

            # Verifica se o arquivo está disponível em algum nó regular
            file_found = False
            for node_addr, files in nodes.items():
                if filename in files:
                    file_found = True
                    print(f"Enviando arquivo '{filename}' para {addr} de {node_addr}")

                    # Abre o arquivo para leitura binária
                    with open(filename, 'rb') as f:
                        while True:
                            data = f.read(4096)
                            if not data:
                                break
                            conn.sendall(data)

                    print(f"Arquivo '{filename}' enviado para {addr}")
                    break

            if not file_found:
                print(f"Arquivo '{filename}' não encontrado em nenhum nó regular.")
                conn.sendall("Arquivo não encontrado")

            # Envia o arquivo para todos os outros nós regulares na rede
            send_file_to_all_nodes(filename)

    except Exception as e:
        print(f"Erro ao lidar com conexão de {addr}: {e}")

    finally:
        conn.close()
        print(f"Conexão fechada com {addr}")

# Função para atualizar a lista de arquivos de um nó regular
def update_node_files(addr, files):
    nodes[addr] = files
    print(f"Atualizada lista de arquivos para o nó {addr}: {files}")

# Função para enviar um arquivo para um nó regular específico
def send_file_to_node(conn, filename):
    try:
        # Envia o nome do arquivo primeiro
        conn.send(filename.encode())

        # Abre o arquivo para leitura binária
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                conn.sendall(data)

        print(f"Arquivo '{filename}' enviado para um nó regular.")

    except Exception as e:
        print(f"Erro ao enviar arquivo '{filename}' para um nó regular: {e}")

# Função para enviar um arquivo para todos os nós regulares na rede
def send_file_to_all_nodes(filename):
    for node_conn, node_addr in nodes.items():
        send_file_to_node(node_conn, filename)

# Função para iniciar o servidor de borda
def start_edge_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Nó de borda iniciado. Escutando na porta {PORT}...")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_node_connection, args=(conn, addr))
            thread.start()

            # Recebe a lista de arquivos do nó regular
            files_data = conn.recv(1024).decode()
            files = files_data.split(',')
            update_node_files(addr, files)

    except Exception as e:
        print(f"Erro ao iniciar o servidor de borda: {e}")

    finally:
        s.close()

# Inicia o servidor de borda em uma thread separada
if __name__ == "__main__":
    edge_server_thread = threading.Thread(target=start_edge_server)
    edge_server_thread.start()
