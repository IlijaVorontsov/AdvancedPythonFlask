# script to send emails
from email.message import EmailMessage
import ssl
import smtplib
import random


email = 'advancedpythoncourse@gmail.com'
password = ''
email_to = 'ali.170403@hotmail.com'


def generate_password():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    password = ''
    for _ in range(4):
        for _ in range(5):
            password += random.choice(letters + numbers)
        password += '-'
    password = password[:-1]
    return password

def send_register_mail(email_to, username, password):
    email_msg = EmailMessage()
    email_msg['From'] = email
    email_msg['To'] = email_to
    email_msg['Subject'] = 'Hello from Python!'

    body = f'''
    Willkommen bei unserem Kurs!
    Dein Benutzername ist: {username}
    Dein Passwort ist: {password}
    '''

    email_msg.set_content(body)

    send_mail(email_to, email_msg)


def send_reset_mail(email_to, username, password):
    email_msg = EmailMessage()
    email_msg['From'] = email
    email_msg['To'] = email_to
    email_msg['Subject'] = 'Hello from Python!'

    body = f'''
    Hallo {username}!
    Dein neues Passwort ist: {password}
    '''

    email_msg.set_content(body)

    send_mail(email_to, email_msg)

def send_mail(email_to, email_msg):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email, password)
        smtp.sendmail(email, email_to, email_msg.as_string())

