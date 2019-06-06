import os
import datetime
from fpdf import FPDF


class InvoiceGenerator:
    def __init__(self, customer, items, delivery_fee, order_number, today):
        """
        customer object
        {
            "name": "Customer Name",
            "address": "Customer Address",
            "msisdn": "Customer msisdn"
        }
        """
        self._customer = customer
        self._today = today

        # delivery fee for the order
        self._delivery_fee = delivery_fee

        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

        # fonts
        self._regular_font_path = os.path.join(font_path, 'Roboto-Medium.ttf')
        self._italic_font_path = os.path.join(font_path, 'Roboto-MediumItalic.ttf')
        self._bold_font_path = os.path.join(font_path, 'Roboto-Bold.ttf')
        self._normal_font_path = os.path.join(font_path, 'Roboto-Regular.ttf')

        # images
        self._th_logo = os.path.join(image_path, 'tonic-logo.png')
        self._thy_logo = os.path.join(image_path, 'thyrocare-logo.png')
        self._paid_banner = os.path.join(image_path, 'paid-banner.png')

        """
        items = [
            {
                "name": 'Diabeties Medicine',
                "price": 6522.50,
                "discount": 200.0,
            },
            {
                "name": "Diabetes Machine",
                "price": 1200.00,
                "discount": 1200.00,
            }
        ]
        """
        self._items = items
        self._order_number = order_number
        self._sub_total = sum([item["price"] for item in self._items])
        self._discount = sum([item['discount'] for item in self._items])
        self._total_amount = self._sub_total - self._discount
        self._net_payable_amount = self._total_amount + self._delivery_fee

        self._pdf = FPDF(unit='pt')
        self._initial_x = 72.0
        self._inital_y = 72.0

        # font size
        self._header_font = 13.0
        self._para_font = 8.0
        self._medium_font = 10.0
    
    def setup_fpdf(self):
        self._pdf.set_author("Rakib Hasan Amiya")
        self._pdf.set_auto_page_break(True, 72.0)
        self._pdf.set_margins(72.0, 72.0, 72.0)
        self._pdf.add_page()
        self._pdf.set_creator("Telenor Health")
        self._pdf.set_subject("Telenor Health Product Invoice")
        self._pdf.set_auto_page_break(True)
        self._pdf.add_font('robotoN', fname=self._regular_font_path, uni=True)
        self._pdf.add_font('robotoI', fname=self._regular_font_path, uni=True)
        self._pdf.add_font('robotoB', fname=self._bold_font_path, uni=True)
        self._pdf.add_font('roboto', fname=self._normal_font_path, uni=True)
    
    def setup_cell(self, rgb,
        font, font_size, align, text, is_new_line=True, y_val=None, height=0.0):
        self._pdf.set_x(72.0)
        if is_new_line:
            self._pdf.ln()
        if y_val:
            self._pdf.set_y(self._pdf.get_y() + y_val)
        # print(self._pdf.get_y(), y_val)
        self._pdf.set_font(font, '', float(font_size))
        self._pdf.set_text_color(r=rgb['r'],g=rgb['g'],b=rgb['b'])
        self._pdf.cell(ln=0, h=height, align=align, w=0.0, txt=text, border=0.0)
    
    def setup_image(self, image, width, x_val=None, y_val=None, height=0.0):
        x = 72.0
        y = self._pdf.get_y()
        self._pdf.set_x(72.0)
        if x_val:
            x = x + x_val
        if y_val:
            y = y + y_val
        self._pdf.image(image, x=x, y=y, w=width, h=height)
    
    def setup_line(self, x_val_start, y_val, x_val_end, line_width=1):
        self._pdf.set_line_width(line_width)
        x = 72.0
        if y_val:
            self._pdf.set_y(self._pdf.get_y() + y_val)
        self._pdf.line(x+x_val_start, self._pdf.get_y(), x+x_val_end, self._pdf.get_y())
    
    def create_invoice(self):
        self.setup_fpdf()
        self._pdf.set_x(72.0)
        # date cell
        grey_clr = dict(r=73, g=83, b=99)
        self.setup_cell(grey_clr, 'roboto', self._para_font, 'L', self._today, False)
        # th_logo
        self.setup_image(self._th_logo, 130.0, x_val=320, y_val=0.0)
        # set invoice text
        self.setup_cell(grey_clr, 'robotoB', self._header_font, 'L', "invoice".upper(), y_val=70.0)
        # set order number
        self.setup_cell(grey_clr, 'roboto', self._para_font, 'L', self._order_number, y_val=15.0)
        # thy_logo
        self.setup_image(self._thy_logo, 135.0, x_val=328.0, y_val=-35.0)
        # thank you text
        self.setup_cell(grey_clr, 'robotoB', self._header_font, 'L', "Thank you for your purchase!", y_val=65.0)
        # getting order ready text
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', "Hi, We're getting your order to be shipped. We will notify you when it", y_val=15.0)
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', 'has been sent', y_val=15.0)
        # set line
        self.setup_line(-50, 40.0, 500)
        # order summary
        self.setup_cell(grey_clr, 'robotoB',self._header_font, 'L', "Order Summary", y_val=30.0)
        # paid image
        self.setup_image(self._paid_banner, 50.0, x_val=400.0, y_val=-13.0)
        # type of items heading
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', 'Type-Item', y_val=40.0)
        # price heading
        self.setup_cell(grey_clr, 'robotoB',self._para_font, 'R', 'Price(tk)')
        # item and price loop
        counter = 1
        for item in self._items:
            self.setup_cell(grey_clr, 'robotoB',self._header_font, 'L', "{}. {}".format(counter, item.get("name")), y_val=30.0)
            self.setup_cell(grey_clr, 'roboto',self._para_font, 'R', str(item.get("price")))
            counter += 1
        self.setup_line(0, 20.0, 450, line_width=0.5)
        # sub total
        self.setup_cell(grey_clr, 'roboto', self._medium_font, 'L', 'Sub total', y_val=15.0)
        self.setup_cell(grey_clr, 'roboto', self._medium_font, 'R', str(self._sub_total))
        # discount
        green_clr = dict(r=13, g=173, b=1)
        self.setup_cell(green_clr, 'robotoB', self._medium_font, 'L', 'Tonic Discount', y_val=20.0)
        self.setup_cell(green_clr, 'robotoB', self._medium_font, 'R', str(self._discount))
        # total price
        self.setup_cell(grey_clr, 'roboto', self._para_font, 'L', 'Total Price', y_val=20.0)
        self.setup_cell(grey_clr, 'roboto', self._para_font, 'R', str(self._total_amount))
        # delivery fee
        self.setup_cell(grey_clr, 'roboto', self._para_font, 'L', 'Delivery Fee', y_val=20.0)
        self.setup_cell(grey_clr, 'roboto', self._para_font, 'R', str(self._delivery_fee))
        # line
        self.setup_line(0, 20.0, 450, line_width=0.5)
        # net payable
        self.setup_cell(grey_clr, 'robotoB', self._para_font, 'L', 'Net Payable Amount', y_val=20.0)
        blue_clr = dict(r=4, g=232, b=244)
        self.setup_cell(blue_clr, 'robotoB', self._para_font, 'R', str(self._net_payable_amount))
        # line
        self.setup_line(-50, 40.0, 500)
        # customer information
        self.setup_cell(grey_clr, 'robotoB',self._header_font, 'L', "Customer Information", y_val=30.0)
        self.setup_cell(grey_clr, 'robotoB', 13.0, 'L', self._customer.get("name"), y_val=20.0)
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', "Address: {}".format(self._customer.get("address")), y_val=15.0)
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', "Phone: {}".format(self._customer.get("msisdn")), y_val=15.0)
        # line
        self.setup_line(-50, 40.0, 500)
        # contact us
        self.setup_cell(grey_clr, 'robotoB',self._header_font, 'L', "Contact Us", y_val=30.0)
        self.setup_cell(grey_clr, 'robotoB', self._medium_font, 'L', "Hot Line: (+88) 09666737373/ (+88) 01944443850", y_val=15.0)
        self.setup_cell(grey_clr, 'robotoB', self._medium_font, 'L', "(+88) 01944443851", y_val=15.0)
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', "Address: Confidence Centre (12th floor), Kha-9 Pragoti Sarani, Shazadpur", y_val=15.0)
        self.setup_cell(grey_clr, 'roboto',self._para_font, 'L', "Gulshan. Dhaka - 1212, Bangladesh", y_val=10.0)
        # create pdfs dir if not exists
        try:
            os.mkdir("pdfs")
        except FileExistsError:
            pass
        self._pdf.output('./pdfs/{}.pdf'.format(self._order_number), 'F').encode('latin-1')

if __name__ == "__main__":
    customer = {
        "name": "Rakib Hasan Amiya",
        "address": "56, North Dhanmondi",
        "msisdn": "+8801701227019",
    }
    items = [
        {
            "name": 'Diabeties Medicine',
            "price": 6522.50,
            "discount": 200.0,
        },
        {
            "name": "Diabetes Machine",
            "price": 1200.00,
            "discount": 1200.00,
        }
    ]
    delivery = 60.00
    today = datetime.datetime.today()
    str_today = str(today.strftime("%d/%m/%Y"))

    inv = InvoiceGenerator(customer, items, delivery, "Order-20178-2019", str_today)
    inv.create_invoice()
    import sys
    if sys.platform.startswith("linux"):
        os.system("xdg-open ./pdfs/Order-20178-2019.pdf")
    else:
        os.system("./invoice.pdf")
