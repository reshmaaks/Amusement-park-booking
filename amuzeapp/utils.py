from fpdf import FPDF
class TicketPDF(FPDF):
    def __init__(self, adult_count=0, child_count=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticket_details = {}
        self.adult_count = adult_count
        self.child_count = child_count
        self.food_options = []

    def set_ticket_details(self, ticket_details):
        self.ticket_details = ticket_details

    def set_food_options(self, food_options):
        self.food_options = food_options

    def generate_ticket(self):
        self.add_page('A4')
        self.set_xy(0, 0)
        self.image('static/images/logo2.jpg', x=15, y=10, w=30)
        self.set_font('Arial', 'B', 24)
        self.cell(0, 60, 'Amusement Park Ticket', ln=1, align='C')

        # Set up border for ticket details
        self.set_line_width(0.5)
        self.rect(65, 50, 160, 85, 'D')
        self.set_font('Arial', '', 14)
        self.cell(0, 10, f'Package_Adult: {self.ticket_details["Package_Adult"]}', ln=1, align='C')
        self.cell(0, 10, f'Package_Child: {self.ticket_details["Package_Child"]}', ln=1, align='C')
        self.cell(0, 10, f'Date: {self.ticket_details["date"]}', ln=1, align='C')
        self.cell(0, 10, f'Adult Count: {self.adult_count}', ln=1, align='C')
        self.cell(0, 10, f'Child Count: {self.child_count}', ln=1, align='C')
        self.cell(0, 10, f'Total Price: {self.ticket_details["total_price"]}', ln=1, align='C')
        self.set_font('Arial', '', 12)
        y_position = self.get_y() + 10
        self.set_xy(30, y_position)

        self.cell(0, 10, ln=1, align='C')
        for option in self.food_options:
            self.cell(0, 10,  f'{option.count} - {option.food_option.name}', ln=1, align='C')
        self.ln(10)
        self.cell(0, 10,  ln=1, align='C')

    def get_pdf_bytes(self):
        self.generate_ticket()
        self.set_creator('your_name')
        self.set_title('Ticket')
        self.set_author('amusement_park')
        self.set_subject('Ticket to Amusement Park')
        self.set_keywords('ticket, amusement park')
        self.set_font('Arial', '', 12)
        self.set_margins(10, 10, 10)
        self.set_auto_page_break(True, 10)
        return self.output(dest='S').encode('latin1')
