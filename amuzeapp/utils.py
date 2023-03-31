from fpdf import FPDF
class TicketPDF(FPDF):
    def __init__(self, adult_count=0, child_count=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticket_details = {}
        self.adult_count = adult_count
        self.child_count = child_count

    def set_ticket_details(self, ticket_details):
        self.ticket_details = ticket_details
        

    def generate_ticket(self):
        self.add_page('Letter')
        self.image('static/images/x1.jpg', x=0, y=0, w=500, h=500)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Amusement Park Ticket', ln=1, align='C')
        self.ln(20)
        self.cell(0, 10, f'Package_Adult: {self.ticket_details["Package_Adult"]}', ln=1,align='C')
        self.cell(0, 10, f'Package_Child: {self.ticket_details["Package_Child"]}', ln=1,align='C')
        self.cell(0, 10, f'Date: {self.ticket_details["date"]}', ln=1,align='C')
        self.cell(0, 10, f'Adult Count: {self.adult_count}', ln=1,align='C')
        self.cell(0, 10, f'Child Count: {self.child_count}', ln=1,align='C')
        self.cell(0, 10, f'Total Price: {self.ticket_details["total_price"]}', ln=1,align='C')
        self.ln(20)
        self.cell(0, 10, 'Thank you for visiting!', ln=1, align='C')
        self.image('static/images/logo2.jpg', x=10, y=10, w=25)
        # self.rect(5, 5, 200, 287)

    def get_pdf_bytes(self):
        self.generate_ticket()
        self.set_creator('your_name')
        self.set_title('Ticket')
        self.set_author('amusement_park')
        self.set_subject('Ticket to Amusement Park')
        self.set_keywords('ticket, amusement park')
        self.set_font('Arial', '', 12)
        # self.set_margins(10, 10, 10)
        self.set_auto_page_break(True, 10)
        return self.output(dest='S').encode('latin1')
 
# from fpdf import FPDF

# class TicketPDF(FPDF):
#     def __init__(self, adult_count=0, child_count=0, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.ticket_details = {}
#         self.adult_count = adult_count
#         self.child_count = child_count

#     def set_ticket_details(self, ticket_details):
#         self.ticket_details = ticket_details

#     def generate_ticket(self):
#         # Set up page
#         self.add_page('L')
#         self.set_margins(0, 0, 0)

#         # Draw background image
#         # self.image('static/images/x1.jpg', x=0, y=0, w=self.w, h=self.h)

#         # Draw logo image
#         self.image('static/images/logo2.jpg', x=10, y=10, w=25)

#         # Add ticket details
#         self.set_font('Arial', '', 14)
#         self.set_text_color(0, 0, 0)
#         self.cell(0, 10, 'Amusement Park Ticket', ln=1, align='C')
#         self.ln(10)
#         self.cell(0, 10, f'Date: {self.ticket_details["date"]}', ln=1,align='C')
#         self.ln(5)
#         self.cell(0, 10, f'Adult Count: {self.adult_count}', ln=1,align='C')
#         self.cell(0, 10, f'Child Count: {self.child_count}', ln=1,align='C')
#         self.cell(0, 10, f'Total Price: {self.ticket_details["total_price"]}', ln=1,align='C')
#         self.ln(10)

#         # Draw medium image section
#         # self.image('static/images/swing-ride.jpg', x=100, y=50, w=350, h=200)

#         # Add image details in a row with image
#         # self.set_x(100)
#         # self.set_y(260)
#         # self.cell(0, 10, 'Image details 1', ln=0)
#         # self.cell(0, 10, 'Image details 2', ln=0)
#         # self.cell(0, 10, 'Image details 3', ln=0)

#     def get_pdf_bytes(self):
#         self.generate_ticket()
#         self.set_creator('your_name')
#         self.set_title('Ticket')
#         self.set_author('amusement_park')
#         self.set_subject('Ticket to Amusement Park')
#         self.set_keywords('ticket, amusement park')
#         self.set_font('Arial', '', 12)
#         self.set_auto_page_break(False)
        
#         return self.output(dest='S').encode('latin1')