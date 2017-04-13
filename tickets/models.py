from django.db import models
from django.contrib.auth.models import User

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
    SHADOW = 'SC'

    CATEGORY_CHOICES = [
        (GENERAL, 'General Admission'),
        (WORKER, 'Worker'),
        (MUSICIAN, 'Musician'),
        (COMMITTEE, 'Committee'),
        (SHADOW, 'Shadow Committee')
    ]

    owner = models.ForeignKey(User)

    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)

    reentry_allowed = models.BooleanField(default=False)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)

    price = models.DecimalField(max_digits=5, decimal_places=2)
    waiting = models.BooleanField(default=True)

    payment_method = models.CharField(max_length=5, choices=PAYMENT_CHOICES)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.fname + ' ' + self.lname

    class Meta:
        permissions = [
            ("buy_cheaper_ticket", "Can buy members' tickets (£70)"),
            ("buy_guests", "Can buy two guest tickets"),
            ("buy_extra_guest", "Can buy an extra guest ticket"),
            ("free_primary_ticket", "Entitled to a free primary ticket"),
        ]