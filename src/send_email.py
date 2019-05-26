import os
import smtplib
from email.mime.text import MIMEText


def mailer(to_email, subject, body):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = "{} <{}>".format(os.environ.get("FROM_NAME"), os.environ.get('FROM_EMAIL'))
    msg['To'] = to_email

    s = smtplib.SMTP(os.environ.get('SMTP_HOST'), int(os.environ.get('SMTP_PORT')))
    s.ehlo()
    s.starttls()
    s.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
    s.sendmail('crons@mytonic.com', to_email, msg.as_string())
    s.quit()