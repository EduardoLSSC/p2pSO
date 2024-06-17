import socket
import threading

def receive_messages(sock):
    while True:
        try:
            # Recebe mensagens do servidor
            response = sock.recv(1024).decode('utf-8')
            if response.lower() == 'exit':
                print("Servidor fechou a conexão.")
                break
            print(f"[SERVER]: {response}")
        except ConnectionResetError:
            print("Servidor fechou a conexão.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.0.154", 9999))
    print("Conectado ao servidor.")

    # Thread para receber mensagens do servidor
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.start()

    while True:
        message = input("[CLIENT]: ")
        client.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            break

    client.close()
    print("Conexão fechada com o servidor.")

if __name__ == "__main__":
    main()
