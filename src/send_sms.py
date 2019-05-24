import smtplib
from email.mime.text import MIMEText


def mailer(to_email, subject, body):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = 'crons@mytonic.com'
    msg['To'] = to_email

    s = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('AKIAJTOAEK6ZBZIH7N5A', 'AugMDmAHNV5sdaXEYgTBluaCVCEBwE+W+uGL3fmoPzld')
    s.sendmail('crons@mytonic.com', to_email, msg.as_string())
    s.quit()