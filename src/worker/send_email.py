# import os
# import smtplib
# from email.mime.text import MIMEText


# def mailer(to_email, subject, body):
#     msg = MIMEText(body)

#     msg['Subject'] = subject
#     msg['From'] = "{} <{}>".format(os.environ.get("FROM_NAME"), os.environ.get('FROM_EMAIL'))
#     msg['To'] = to_email

#     s = smtplib.SMTP(os.environ.get('SMTP_HOST'), int(os.environ.get('SMTP_PORT')))
#     s.ehlo()
#     s.starttls()
#     s.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
#     s.sendmail('crons@mytonic.com', to_email, msg.as_string())
#     s.quit()

import os
import sys
import smtplib
from email.mime.text import MIMEText
import jinja2

def render_template(template, customer):
    ''' renders a Jinja template into HTML '''
    # check if template exists
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(customer)

def mailer(customer, order_number):
    """
    customer = {
        "name": "Customer Name",
        "address": "Customer Address",
        "email": "customer@email.com",
    }
    """
    # email sender
    subject = "Telenor Health Invoice"
    from_name = os.environ.get("FROM_NAME")
    from_email = os.environ.get("FROM_EMAIL")

    # render j2 template
    customer["order_number"] = order_number
    path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(path, 'template', 'email.j2')
    html = render_template(template_path, customer)

    # setup email
    email = MIMEText(html, 'html')
    email['Subject'] = subject
    email['From'] = "{} <{}>".format(from_name, from_email)
    email['To'] = customer.get("email", "test@test.com")

    # TODO: attach file

    s = smtplib.SMTP(os.environ.get('SMTP_HOST'), int(os.environ.get('SMTP_PORT')))
    s.ehlo()
    s.starttls()
    s.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
    s.sendmail(from_email, customer.get("email", "test@test.com"), email.as_string())
    print("email sent.")
    s.quit()

