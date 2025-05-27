import sqlite3
from datetime import datetime

# Cria o banco e a tabela se não existirem
def criar_banco():
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            equipamento TEXT NOT NULL,
            problema TEXT NOT NULL,
            solucao TEXT NOT NULL,
            tempo_reparo REAL,
            inicio_os TEXT,
            fim_os TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Chama criar_banco() sempre que o módulo é importado
criar_banco()

def adicionar_os(data, equipamento, problema, solucao, tempo_reparo, inicio, fim):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ordens_servico (data, equipamento, problema, solucao, tempo_reparo, inicio_os, fim_os)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data, equipamento, problema, solucao, tempo_reparo, inicio.strftime("%d/%m/%Y %H:%M"), fim.strftime("%d/%m/%Y %H:%M")))
    conn.commit()
    conn.close()

def buscar_os_mes(mes, ano):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM ordens_servico
        WHERE strftime('%m', data) = ? AND strftime('%Y', data) = ?
    ''', (f"{mes:02d}", str(ano)))
    return cursor.fetchall()

def buscar_todas_os():
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordens_servico ORDER BY data DESC")
    return cursor.fetchall()