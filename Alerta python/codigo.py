import requests
import smtplib
import email.message
import schedule
import time


def obter_cotacao():
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/BTC-BRL")
    requisicao_dicionario = requisicao.json()
    cotacao = float(requisicao_dicionario['BTCBRL']['bid'])
    return cotacao


def enviar_email(cotacao, destinatarios):
    corpo_email = f"<p>Olá, a atual cotação do bitcoin é de: {cotacao}</p>"

    msg = email.message.Message()
    msg['Subject'] = "Cotação do BTC"
    msg['From'] = 'botdobitcoin@gmail.com'
    msg['To'] = ', '.join(destinatarios)
    password = 'jtbfhdhfaymkfmep'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], destinatarios, msg.as_string().encode('utf-8'))
    s.quit()
    print('Email enviado para:', ', '.join(destinatarios))


def job():
    cotacao = obter_cotacao()

    # Lista de e-mails para os quais você deseja enviar a cotação
    destinatarios = ['user2@gmail.com']

    enviar_email(cotacao, destinatarios)


# Agendar o trabalho para ser executado a cada dia às 8:00
schedule.every().day.at("15:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)