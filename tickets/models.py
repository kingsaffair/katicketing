import uuid

from django.db import models
from django.db.models import Sum
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
    primary.boolean = True

    def has_paid(self):
        return self.paid is not None
    has_paid.boolean = True

    def has_collected(self):
        return self.collected is not None
    has_collected.boolean = True

    def has_checked_in(self):
        return self.checked_in is not None
    has_checked_in.boolean = True

    def create_namechange(self, first_name, last_name):
        nc = GuestNameChange(
            guest = self,
            old_first_name = self.first_name,
            old_last_name = self.last_name,
            new_first_name = first_name,
            new_last_name = last_name,
            owner = self.owner)
        nc.save()

        if self.owner.has_perm('free_name_changes'):
            nc.complete()

    def has_pending_namechange(self):
        changes = GuestNameChange.objects.filter(guest=self, pending=True)
        return changes.exists()

    class Meta:
        permissions = [
            ("buy_cheaper_ticket", "Can buy members' tickets (£70)"),
            ("buy_guests", "Can buy two guest tickets"),
            ("buy_extra_guest", "Can buy an extra guest ticket"),
            ("free_primary_ticket", "Entitled to a free primary ticket"),
            ("free_name_changes", "Entitled to free name changes")
        ]

class GuestNameChange(models.Model):
    """
    create one of these every time the name changes
    """
    guest = models.ForeignKey(Guest)
    owner = models.ForeignKey(User)

    new_first_name = models.CharField(max_length=100)
    new_last_name = models.CharField(max_length=100)

    old_first_name = models.CharField(max_length=100)
    old_last_name = models.CharField(max_length=100)

    cost = models.DecimalField(max_digits=5, decimal_places=2)
    pending = models.BooleanField(default=True)

    @staticmethod
    def has_pending_namechange(user):
        changes = GuestNameChange.objects.filter(owner=user, pending=True)
        return changes.exists()

    @staticmethod
    def namechange_total_cost(user):
        changes = GuestNameChange.objects.filter(owner=user, pending=True).aggregate(Sum('cost'))
        return changes['cost__sum']

    def complete(self):
        self.guest.first_name = self.new_first_name
        self.guest.last_name = self.new_last_name
        self.pending = False
        self.guest.save()

    def __str__(self):
        return '%s %s -> %s %s' % (self.old_first_name, self.old_last_name, self.new_first_name, self.new_last_name)

    class Meta:
        verbose_name = 'Name Change'
        verbose_name_plural = 'Name Changes'
