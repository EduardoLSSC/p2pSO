import socket
import threading
import time

nodes = {}
lock = threading.Lock()

def search_file_in_nodes(client_socket, search_file):
    print('fasf'+search_file)
    node_ip = ''
    for ip, file_list in nodes.items():
        for file_info in file_list:
            if file_info['filename'] == search_file:
                node_ip = str(ip)
                client_socket.send(node_ip.encode())
    if node_ip == '':
        client_socket.send(('Nenhum no conectado possui o arquivo digitado').encode())

def get_files_by_name(client_socket, search_file):
    print('Starting getfiles protocol')
    print('filename: '+search_file)
    search_file_in_nodes(client_socket, search_file)

def get_files(client_socket, ip, handshake = False):
    print('Starting handshake protocol')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 9998))
    if handshake == True:
        data = client.recv(4096).decode()
        data_json = eval(data)
        with lock:
            for d in data_json:
                nodes[ip] = nodes.get(ip, [])
                nodes[ip].append(d)
                print(nodes)
        client_socket.send(('ack').encode())
    else:
        data = client.recv(4096).decode()
        data_json = eval(data)
        with lock:
            for d in data_json:
                nodes[ip] = nodes.get(ip, [])
                nodes[ip].append(d)
                print(nodes)
    client.close()

def handle_client(client_socket, ip):
    while True:
        try:
            # Recebe a mensagem do cliente
            request = client_socket.recv(1024).decode('utf-8')
            print(request)
            if request == 'handshake':
                threading.Thread(target=get_files, args=(client_socket, ip, True)).start()
            else:
                protocol = eval(request)[0]
                filename = eval(request)[1]
            
                threading.Thread(target=get_files_by_name, args=(client_socket, filename)).start()
        except ConnectionResetError:
            break

    client_socket.close()
    print("Conexão fechada com o cliente.")

def main():
    # create_memory_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Servidor ouvindo na porta 9999...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de: {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr[0]))
        client_handler.start()
if __name__ == "__main__":
    main()