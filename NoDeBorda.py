import sqlite3
import json
import socket
import threading
import time

nodes = {}
# Criação de um lock global
lock = threading.Lock()
# CONN = sqlite3.connect('file::memory:?cache=shared', uri=True)

# def get_files_db(conn):
#     conn = sqlite3.connect('file::memory:?cache=shared', uri=True)
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM tbfiles")
#     #consulta arquivos e ja pega o ip balanceado
#     #CUR.execute("SELECT * FROM tbfiles where filename like 'file%' and downloads = (SELECT min(downloads) FROM tbfiles where filename like 'file%') ")
#     rows = cur.fetchall()

#     # Exibir os dados
#     print("Dados na tabela 'tbfiles':")
#     for row in rows:
#         print(row)

#     # Fechar a conexão
#     CONN.close()

# def create_memory_db():
#     cur = CONN.cursor()
#     cur.execute('''CREATE TABLE tbfiles
#                (id INTEGER PRIMARY KEY, ip TEXT, filename TEXT, checksum TEXT, downloads INTEGER)''')
#     CONN.commit()

# def execute_queries_db(conn, sql):
#     cur = conn.cursor()
#     cur.execute(sql)
#     cur.commit()
#     get_files_db()

def get_files(client_socket, ip, handshake = False):
    print(ip)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 9998))
    
    data = client.recv(4096).decode()
    data_json = eval(data)
    if handshake == True:
        client_socket.send(('ack').encode())
    print(data_json)
    # sql = ''
    with lock:
        for d in data_json:
            nodes[ip] = nodes.get(ip, [])  # Inicializa a lista para o IP se ainda não existir
            nodes[ip].append(d)
    # print(sql)
    # with db_lock:
    #     execute_queries_db(conn, sql)

def handle_client(client_socket, ip):
    while True:
        try:
            # Recebe a mensagem do cliente
            request = client_socket.recv(1024).decode('utf-8')

            if request == 'handshake':
                threading.Thread(target=get_files, args=(client_socket, ip, True)).start()
                
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
        while True:
            with lock:
                print("Conteúdo atual de nodes:")
                for ip, files in nodes.items():
                    print(f"IP: {ip}, Arquivos: {files}")
                if nodes:  # Se nodes não estiver vazio, pare o loop
                    break
            
            # Aguarda um segundo antes de verificar novamente
            time.sleep(10)
if __name__ == "__main__":
    main()