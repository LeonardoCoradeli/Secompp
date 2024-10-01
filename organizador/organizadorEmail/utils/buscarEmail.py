import imapclient
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import datetime

def fetch_email_content(imap_server, email_address, password, folder="INBOX", max_emails=50, fetch_today=False):
    """
    Fetches the text content of emails and prepares them for rendering in a Django template.
    
    Args:
        imap_server (str): The IMAP server address.
        email_address (str): The email address to log in.
        password (str): The password for the email account.
        folder (str): The folder to search emails in (default is "INBOX").
        max_emails (int): The maximum number of emails to search through (default is 50).
        fetch_today (bool): If True, fetch only today's emails. Otherwise, fetch the last max_emails emails.

    Returns:
        list: A list of dictionaries, each containing metadata and plain text content of an email.
    """

    # Conectar ao servidor IMAP
    with imapclient.IMAPClient(imap_server) as client:
        client.login(email_address, password)
        client.select_folder(folder)

        # Se fetch_today for True, buscar apenas emails de hoje
        if fetch_today:
            current_date = datetime.date.today()
            uids = client.search(['SINCE', current_date])
        else:
            # Buscar todos os e-mails e pegar os mais recentes
            uids = client.search('ALL')

        if not uids:
            return []  # Sem emails

        # Limitar o número de emails, pegando os mais recentes
        uids = uids[-max_emails:]  # Pegue os últimos 'max_emails'

        # Armazenar dados de todos os emails encontrados
        emails_data = []

        # Iterar sobre cada UID encontrado
        for uid in reversed(uids):  # Processar em ordem reversa para obter os mais recentes primeiro
            raw_email = client.fetch([uid], ['BODY[]', 'UID'])

            msg = email.message_from_bytes(raw_email[uid][b'BODY[]'])

            # Decodificar o assunto
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            # Remetente e data
            from_ = msg.get("From")
            date = parsedate_to_datetime(msg.get("Date"))

            # Extrair conteúdo HTML e converter para texto puro usando BeautifulSoup
            html_content = ""
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True).decode(part.get_content_charset())

            soup = BeautifulSoup(html_content, 'html.parser')
            plain_text_content = soup.get_text()

            emails_data.append({
                'uid': uid,
                'subject': subject,
                'from': from_,
                'date': date,
                'plain_text_content': plain_text_content.strip(),
            })

    return emails_data