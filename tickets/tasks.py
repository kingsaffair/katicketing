# Create your tasks here
from __future__ import absolute_import, unicode_literals

import qrcode

from celery import shared_task

from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Guest
from .psd_ticket import PSDTicketGenerator

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

@shared_task(bind=True)
def process_tickets(self, new_tickets):
    with transaction.atomic():
        # TODO: we can certainly do more of this in SQL and avoid calling
        #       Python in between synchronous SQL calls. We can certainly
        #       aim to to do this in one round trip to the db.
        # maybe using something like:
        # https://docs.djangoproject.com/en/1.10/ref/models/conditional-expressions/

        tickets = Guest.objects.filter(waiting=False).count()

        available_tickets = 1600 - tickets

        # allocate tickets as available
        for t in new_tickets:
            t = Guest.from_dict(t)
            if available_tickets >= 1:
                t.waiting = False
            else:
                t.waiting = True

            t.save()
            available_tickets -= 1

@shared_task(bind=True)
def generate_qrcode(self, guest, hash):
    # TODO: use Amazon S3 or something to store these
    img = qrcode.make('https://beta.kingsaffair.com/checkin/%s' % hash)
    img.save('qr-%s.png' % hash)

    guest = Guest.objects.get(id=guest)
    guest.qr_code.name = 'qr-%s.png' % hash
    guest.save()

@shared_task
def send_cancel_messages(time):
    # send one for all of the primary tickets
    cancellations = Guest.objects.filter(cancelled=time, parent__isnull=True)

    for ticket in cancellations:
        body = render_to_string('emails/cancel.tpl', {'first_name': ticket.first_name})
        email = ticket.owner.email

        if email is None:
            # this is potentially an issue, but we'll deal with that if we come to it.
            continue

        email = EmailMessage(
            'King\'s Affair Ticket Cancellation',
            body,
            'tickets@noreply.kingsaffair.com',
            [email],
            reply_to=('ticketing@kingsaffair.com',)
        )
        email.send()

@shared_task
def ticket_generator(ids):
    tickets = Guest.objects.filter(id__in=ids)

    sans = settings.SANS_FONT_FILE
    mono = settings.MONO_FONT_FILE
    psd_location = settings.PSD_LOCATION

    pdfmetrics.registerFont(TTFont("sans", sans))
    pdfmetrics.registerFont(TTFont("mono", mono))

    psd = PSDTicketGenerator(psd_location, 156, 66)
    buf = psd.generate(tickets)
    
    # Write the PDF to a file
    with open('output.pdf', 'wb') as fd:
        fd.write(buf.getvalue())
