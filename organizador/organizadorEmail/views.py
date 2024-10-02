from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model
import imapclient
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
import datetime
from organizadorEmail.models import Emails,Markers, UserEmailMarker, UserMarker
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError
from django.views.decorators.http import require_POST
from django.urls import reverse

genai.configure(api_key="AIzaSyDFGsp5xa0r9pIp8rpzLWFaUYQyhyaQzF8")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def fetch_email_content(email_address, password, folder="INBOX", imap_server='imap.gmail.com',max_emails=10, fetch_today=False):
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

def classify_email(emails_content, marker, usuario):
    email_uids =[]
    for email_data in emails_content:
        if not Emails.objects.filter(emailUid=email_data['uid']).exists():
            email_obj = Emails.objects.create(
                emailUid=email_data['uid'],
                subject=email_data['subject'],
                body=email_data['plain_text_content'],
                sender=email_data['from'],
                receiver=usuario.email,
                received_at=email_data['date']
            )
            response = model.generate_content(
                f'Esse email se encaixa nessa categoria, responda apenas com sim ou não\n Categoria:{marker}\nDados email:\n{email_data['subject']}\n{email_data['plain_text_content']}'
            )
            email_uids = email_data['uid'] if 'sim' in response.text else email_uids
    for uid in email_uids:
        uid = uid.strip()  # Remover espaços em branco
        try:
            email_obj = Emails.objects.get(emailUid=uid)
            print(f"Classificando email com UID {uid} para o marcador {marker.name}")
            # Salvar a associação do email com o marcador para o usuário
            UserEmailMarker.objects.create(
                user=usuario,
                email=email_obj,
                marker=marker
            )
        except Emails.DoesNotExist:
            print(f"Email com UID {uid} não encontrado.")


CustomUser = get_user_model()

def listEmails(request,marker=None):
    emails_content = []
    email = request.user.email
    
    # Buscar o usuário no banco de dados
    usuario = get_object_or_404(CustomUser, email=email)
    
    # Obter a senha de app do usuário
    app_password = usuario.password_app
    
    # Verificar se é o primeiro login do usuário
    is_first_login = usuario.last_login is None
    
    if is_first_login:
        classificacao = Markers.objects.get_or_create(name='Sem classificação')
        UserMarker.objects.create(user=usuario,marker= classificacao)
    
        
    markers_user = UserMarker.objects.filter(userId=usuario.userId)
    print([m for m in markers_user])
    
    
    return render(request, 'email/email.html', {
        'usuario': usuario,
        'classificadores': [m.markerId for m in markers_user],
    })
   
@require_POST
def add_category(request):
    category_name = request.POST.get('category')
    if category_name:
        email = request.user.email
        usuario = get_object_or_404(CustomUser, email=email)

        # Verificar se o marcador já existe
        try:
            marker = Markers.objects.get(name=category_name)
            created = False
        except Markers.DoesNotExist:
            marker = Markers.objects.create(name=category_name)
            created = True

        # Criar a associação entre o usuário e o marcador
        UserMarker.objects.create(userId=usuario, markerId=marker)
    else:
        messages.error(request, 'Por favor, forneça um nome de categoria válido')
    return redirect(reverse('list_emails'))

def load_emails(request):
    # Obter o email do usuário logado
    email = request.user.email
    usuario = get_object_or_404(CustomUser, email=email)

    # Obter o marcador (opcional)
    marker_name = request.GET.get('marker', None)
    print(marker_name)
    
    if marker_name:
        # Se um marcador for passado, filtrar emails por marcador
        classify_email(fetch_email_content(email, usuario.password_app), marker_name, usuario)
        marker = get_object_or_404(Markers, name=marker_name)
        user_email_markers = UserEmailMarker.objects.filter(userId=usuario, markerId=marker)
        emails = []
        for user_email_marker in user_email_markers:
            emails.append(Emails.objects.get(emailId=user_email_marker.emailId))
        
    else:
        # Caso nenhum marcador seja passado, carregar os últimos 10 emails
        emails = Emails.objects.filter(receiver=email).order_by('-received_at')[:10]

    # Preparar os dados dos emails para retornar como JSON
    email_data = [
        {
            'subject': email.subject,
            'date': email.received_at.strftime('%Y-%m-%d %H:%M:%S'),
            'from': email.sender,
            'plain_text_content': email.body,
        }
        for email in emails
    ]

    return JsonResponse({'emails': email_data})