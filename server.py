import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            # Recebe a mensagem do cliente
            request = client_socket.recv(1024).decode('utf-8')
            if request.lower() == 'exit':
                break
            print(f"[CLIENT]: {request}")

            # Resposta do servidor
           # response = input("[SERVER]: ")
            resp = 'Voce disse ' + request
           # client_socket.send(response.encode('utf-8'))
            client_socket.send(resp.encode('utf-8'))
        except ConnectionResetError:
            break

    client_socket.close()
    print("Conexão fechada com o cliente.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Servidor ouvindo na porta 9999...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
