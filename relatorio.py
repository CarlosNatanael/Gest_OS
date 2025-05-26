import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def enviar_relatorio(email_destino, dados):
    remetente = "seu_email@gmail.com"
    senha = "sua_senha_app"  # Senha de app do Gmail

    # Criar tabela resumo
    df = pd.DataFrame(dados, columns=["ID", "Data", "Equipamento", "Problema", "Solução", "Tempo Reparo"])
    resumo = df.groupby("Equipamento")["Tempo Reparo"].mean().reset_index()
    html = resumo.to_html()

    # Configurar e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = email_destino
    msg['Subject'] = "Relatório Mensal de OS"
    msg.attach(MIMEText(html, 'html'))

    # Enviar
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)