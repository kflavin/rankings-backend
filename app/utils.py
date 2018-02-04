import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from datetime import date, timedelta

from flask import current_app

# Helper function to add in active attribute
# def isActive(d):
#     if date.today() > d and date.today() <= d + timedelta(3):
#         return True
#     else:
#         return False


def sendMail(fromAddr, toAddr, subject, text, html):

    # AWS Config
    EMAIL_HOST = current_app.config['EMAIL_HOST']
    EMAIL_HOST_USER = current_app.config['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = current_app.config['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = current_app.config['EMAIL_PORT']

    print("email host is " + EMAIL_HOST)

    #msg = MIMEMultipart('alternative')
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromAddr
    msg['To'] = toAddr

    #html = open('index.html').read()
    #mime_text = MIMEText(html, 'html')
    #msg.attach(mime_text)

    msg.attach(MIMEText(text, 'text'))
    msg.attach(MIMEText(html, 'html'))

    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(fromAddr, toAddr, msg.as_string())
    s.quit()