from datetime import datetime as dt
from flask import render_template

import app.constants as constants
from app.mailers import Mailer
from app.extensions import token

class PurchaseReceipt(Mailer):
    TEMPLATE = 'email/purchase_receipt.html'
    DEFAULT_SUBJECT = "Your purchase of Ignite Starter"

    def send(self):
        key = "{email}-{timestamp}".format(email=self.recipient.email, timestamp=dt.now())
        license = token.generate(key, salt=constants.PURCHASE_LICENSE_SALT)
        html_body = render_template(self.TEMPLATE, license=license)
        return self.deliver_now(self.recipient_email, self.subject, html_body)
