import sqlite3

# Conectar ao banco de dados em memória
conn = sqlite3.connect(':memory:')

# Criar um cursor
cur = conn.cursor()

# Criar uma tabela
cur.execute('''CREATE TABLE tbfiles
               (id INTEGER PRIMARY KEY, ip TEXT, filename TEXT, hash TEXT, downloads INTEGER)''')

# Inserir dados
cur.execute("INSERT INTO tbfiles (ip, filename, hash, downloads) VALUES ('127.0.0.1', 'file.txt', 'sdsdsdsd', 1)")
cur.execute("INSERT INTO tbfiles (ip, filename, hash, downloads) VALUES ('127.0.0.1', 'fil.txt', 'sdsdsdsd', 0)")
cur.execute("INSERT INTO tbfiles (ip, filename, hash, downloads) VALUES ('127.0.0.1', 'file.txt', 'sdsdsdsd', 0)")
# Commit para salvar as mudanças
conn.commit()

# Consultar os dados
cur.execute("SELECT * FROM tbfiles")
#consulta arquivos e ja pega o ip balanceado
cur.execute("SELECT * FROM tbfiles where filename like 'file%' and downloads = (SELECT min(downloads) FROM tbfiles where filename like 'file%') ")
rows = cur.fetchall()

# Exibir os dados
print("Dados na tabela 'tbfiles':")
for row in rows:
    print(row)

# Fechar a conexão
conn.close()
