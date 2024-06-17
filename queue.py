import threading

# Variável compartilhada entre as threads
shared_var = 0
lock = threading.Lock()

# Função que modifica a variável compartilhada
def incrementar():
    global shared_var
    with lock:
        shared_var += 1

# Criar threads
threads = []
for _ in range(5):
    t = threading.Thread(target=incrementar)
    threads.append(t)
    t.start()

# Aguardar todas as threads terminarem
for t in threads:
    t.join()

print(f"Valor final da variável compartilhada: {shared_var}")
