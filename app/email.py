from flask_mail import Message
from app.extensions import mail

DEFAULT_FROM = ('league ninja', 'leagueninja@example.com')

def send_basic_welcome_message(recipients):
    """
    This function sends an email with the subject "hello!" and the body "testing
    1 2 3" to the specified recipients using the default "FROM" address.

    Args:
        recipients (list): The `recipients` input parameter is a list of email
            addresses that will receive the email message.

    """
    message = Message('hello!',
                      sender=DEFAULT_FROM,
                      recipients=[recipients],
                      body="testing 1 2 3")
    mail.send(message)