from ticket_qr import create_tickets
from send_qr_email import send_tickets
from update_sheet import update_sheet


df = create_tickets()
send_tickets()
update_sheet(df)