import sqlite3
import threading

def criar_tabela(conn):
    """ Cria uma tabela e insere dados """
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios
                   (id INTEGER PRIMARY KEY, nome TEXT)''')
    cur.execute("INSERT INTO usuarios (nome) VALUES ('Alice')")
    cur.execute("INSERT INTO usuarios (nome) VALUES ('Bob')")
    conn.commit()

def consultar_dados(conn, thread_id):
    """ Consulta os dados da tabela """
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios")
    rows = cur.fetchall()
    print(f"Thread {thread_id}: {rows}")

def thread_func(thread_id):
    """ Função executada pelas threads """
    conn = sqlite3.connect(':memory:')
    criar_tabela(conn)
    consultar_dados(conn, thread_id)
    conn.close()

def processar_banco():
    threads = []
    for i in range(5):
        thread = threading.Thread(target=thread_func, args=(i,))
        threads.append(thread)
        thread.start()

    # for thread in threads:
    #     thread.join()

if __name__ == "__main__":
    processar_banco()
