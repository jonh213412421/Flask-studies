import email
import imaplib
import time
from email.mime.multipart import MIMEMultipart
import smtplib
import socket
from datetime import datetime
from email.mime.text import MIMEText

def verify_reqs():
    requisitor = ''
    ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[2][4][0]
    requisition = []
    with open("e-mail.txt", "r") as f:
        usuario = f.readline()
        senha = f.readline()
    imap_url = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(usuario, senha)
    mail.select("INBOX")
    _, req = mail.search(None, '(BODY "ipconfig::")')
    for num in req[0].split():
        resultado, data = mail.fetch(num, '(RFC822)')
        raw = data[0][1]
        msg = email.message_from_bytes(raw)
        requisitor = msg['From']
        mail.store(num, "+FLAGS", '\\Deleted')
        for part in msg.walk():
            if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                message = part.get_payload(decode=True)
                print("Message: \n", message.decode())
                temp = message.split()
                for tem in temp:
                    if tem.decode('utf-8') == 'ipconfig::':
                        requisition.append(tem.decode('utf-8'))
                        print("requisição de ipconfig: ", requisitor)
        mail.expunge()
    if len(requisition) != 0:
        for url in requisition:
            print(url)
        smtp_servidor = "smtp.gmail.com"
        smtp_porta = 587
        mensagem = MIMEMultipart()
        mensagem['From'] = usuario
        mensagem['To'] = requisitor
        mensagem['Subject'] = "server ip"
        corpo_email = f"Server ip: {ipv6}\n"
        mensagem.attach(MIMEText(corpo_email, 'plain'))
        try:
            servidor = smtplib.SMTP(smtp_servidor, smtp_porta)
            servidor.starttls()
            servidor.login(usuario, senha)
            servidor.sendmail(usuario, requisitor, mensagem.as_string())
            servidor.quit()
            print("Página enviada com sucesso!")
            with open('log.txt', 'a') as f:
                f.write(str(datetime.now().time().strftime("%H:%M:%S")))
                f.write("-> ")
                f.write(f"e-mail enviado para {requisitor} com sucesso!")
                f.write("\n")
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            with open('log.txt', 'a') as f:
                f.write(str(datetime.now().time().strftime("%H:%M:%S")))
                f.write("-> ")
                f.write(f"Erro. Falha em enviar endereço ip para {requisitor}")
                f.write("\n")

if __name__ == '__main__':
    while True:
        verify_reqs()
