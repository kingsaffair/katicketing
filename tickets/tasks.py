# Create your tasks here
from __future__ import absolute_import, unicode_literals

import qrcode

from celery import shared_task
from django.db import transaction

from .models import Guest

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
