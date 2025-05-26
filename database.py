import sqlite3
from datetime import datetime

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
            tempo_reparo REAL  # Em horas
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_os(data, equipamento, problema, solucao, tempo_reparo):
    conn = sqlite3.connect("os.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ordens_servico (data, equipamento, problema, solucao, tempo_reparo)
        VALUES (?, ?, ?, ?, ?)
    ''', (data, equipamento, problema, solucao, tempo_reparo))
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