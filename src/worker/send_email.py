import os
import sys
import smtplib
import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2

from .invoice import InvoiceGenerator

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

def mailer(customer, order_number, items, delivery_fee, bcc):
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

    # set today
    today = datetime.datetime.today()
    str_today = str(today.strftime("%d/%m/%Y"))

    # create pdf
    pdf = InvoiceGenerator(customer, items, delivery_fee, order_number, str_today)
    pdf.create_invoice()

    # render j2 template
    customer["date"] = str_today
    customer["order_number"] = order_number
    path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(path, 'template', 'email.j2')
    html = render_template(template_path, customer)

    # setup email
    to = customer.get("email")

    email = MIMEMultipart()
    email['Subject'] = subject
    email['From'] = "{} <{}>".format(from_name, from_email)
    email['To'] = to
    
    # attach email body
    email.attach(MIMEText(html, 'html'))

    # attach pdf
    pdf_file = "{}.pdf".format(order_number)
    with open("pdfs/{}".format(pdf_file), 'rb') as attachment:
        pdf = MIMEBase("application", "pdf")
        pdf.set_payload(attachment.read())
        encoders.encode_base64(pdf)
        pdf.add_header(
            "Content-Disposition",
            "attachment; filename={}.pdf".format(order_number)
        )
        email.attach(pdf)

    s = smtplib.SMTP(os.environ.get('SMTP_HOST'), int(os.environ.get('SMTP_PORT')))
    s.ehlo()
    s.starttls()
    s.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'))
    s.sendmail(from_email, [to] + bcc, email.as_string())
    s.quit()

    # deleting pdf file from the server
    os.remove("pdfs/{}.pdf".format(order_number))

if __name__ == "__main__":
    customer = {
		"name": "Rakib Hasan Amiya",
		"email": "rakib@telenorhealth.com",
		"address": "56, North Dhanmondi, Kalabagan, Dhaka - 1205",
		"msisdn": "+8801701227013"
	}
    items = [
		{
            "name": "Diabeties Medicine",
            "price": 6522.50,
            "discount": 200.0
        },
        {
            "name": "Diabetes Machine",
            "price": 1200.00,
            "discount": 1200.00
        }
	]
    order_number = "Order-2780-2019"
    delivery_fee = 60.0
    mailer(customer, order_number, items, delivery_fee)