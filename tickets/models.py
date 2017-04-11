from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    STRIPE = 'ST'
    BANK_TRANSFER = 'BT'
    COLLEGE_BILL = 'CB'

    PAYMENT_CHOICES = [
        (STRIPE, 'Stripe'),
        (BANK_TRANSFER, 'Bank Transfer'),
        (COLLEGE_BILL, 'College Bill')
    ]

    owner = models.ForeignKey(User)

    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=5, decimal_places=2)
    waiting = models.BooleanField(default=True)

    payment_method = models.CharField(max_length=5, choices=PAYMENT_CHOICES)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.fname + ' ' + self.lname

    def to_dict(self):
        return {
            'owner': self.owner.pk,
            'fname': self.fname,
            'lname': self.lname,
            'price': self.price,
            'waiting': self.waiting,
            'payment_method': self.payment_method,
            'parent': None if self.parent is None else self.parent.pk
        }

    @staticmethod
    def from_dict(d):
        d['owner'] = User.objects.get(pk=d['owner'])
        d['parent'] = None if d['parent'] is None else Ticket.objects.get(pk=d['parent'])
        return Ticket(**d)

    class Meta:
        permissions = [
            ("buy_cheaper_ticket", "Can buy members' tickets (£70)"),
            ("buy_guests", "Can buy two guest tickets"),
            ("buy_extra_guest", "Can buy an extra guest ticket"),
            ("free_primary_ticket", "Entitled to a free primary ticket"),
        ]
