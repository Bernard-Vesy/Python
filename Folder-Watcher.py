import time
import logging
import smtplib
from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurer les paramètres de surveillance
directory_to_watch = 'C:/Users/berna/OneDrive/Python/Test'
email_recipient = 'bernard@vesy.ch'
smtp_server = 'pandora.kreativmedia.ch'
smtp_port = 587 #465
smtp_username = 'bernard@vesy.ch'
smtp_password = 'Koala71-71'

# Configurer le logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class MyHandler(FileSystemEventHandler):
    #def on_created(self, event):
    def on_modified(self, event):
        if event.is_directory:
            return
        logging.info(f'Fichier créé: {event.src_path}')
        send_email_alert(event.src_path)

def send_email_alert(file_path):
    subject = 'Alerte : Copie de fichier détectée'
    body = f'Le fichier {file_path} a été copié depuis le répertoire surveillé.'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = email_recipient

    server = smtplib.SMTP(smtp_server, smtp_port,)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, [email_recipient], msg.as_string())
    server.quit()

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
