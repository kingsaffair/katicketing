import uuid

from django.db import models
from django.contrib.auth.models import User

def gen_hash():
    return str(uuid.uuid4())[:8]

class Guest(models.Model):
    STRIPE = 'ST'
    BANK_TRANSFER = 'BT'
    COLLEGE_BILL = 'CB' 
    NONE = 'NO'

    PAYMENT_CHOICES = [
        (STRIPE, 'Stripe'),
        (BANK_TRANSFER, 'Bank Transfer'),
        (COLLEGE_BILL, 'College Bill'),
        (NONE, 'None')
    ]

    GENERAL = 'GA'
    WORKER = 'WK'
    MUSICIAN = 'MU'
    COMMITTEE = 'CO'
    EX_COMMITTEE = 'EC'
    SHADOW = 'SC'

    CATEGORY_CHOICES = [
        (GENERAL, 'General Admission'),
        (WORKER, 'Worker'),
        (MUSICIAN, 'Musician'),
        (COMMITTEE, 'Committee'),
        (SHADOW, 'Shadow Committee'),
        (EX_COMMITTEE, 'Ex-Committee')
    ]

    owner = models.ForeignKey(User)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    _hash = models.CharField(max_length=8, default=gen_hash, unique=True)

    reentry_allowed = models.BooleanField(default=False)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    premium = models.BooleanField(default=False)

    price = models.DecimalField(max_digits=5, decimal_places=2)
    waiting = models.BooleanField(default=True)

    payment_method = models.CharField(max_length=5, choices=PAYMENT_CHOICES)
    qr_code = models.ImageField(upload_to='user_static', default=None, null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)

    paid = models.DateTimeField(null=True, default=None, blank=True)
    collected = models.DateTimeField(null=True, default=None, blank=True)
    checked_in = models.DateTimeField(null=True, default=None, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def primary(self):
        return self.parent is None

    class Meta:
        permissions = [
            ("buy_cheaper_ticket", "Can buy members' tickets (£70)"),
            ("buy_guests", "Can buy two guest tickets"),
            ("buy_extra_guest", "Can buy an extra guest ticket"),
            ("free_primary_ticket", "Entitled to a free primary ticket"),
        ]

class GuestNameChange(models.Model):
    """
    create one of these every time the name changes
    """
    guest = models.ForeignKey(Guest)
    
