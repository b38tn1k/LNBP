from flask_mail import Message
from app.extensions import mail

DEFAULT_FROM = ('league ninja', 'leagueninja@example.com')

def send_basic_welcome_message(recipients):
    message = Message('hello!',
                      sender=DEFAULT_FROM,
                      recipients=[recipients],
                      body="testing 1 2 3")
    mail.send(message)