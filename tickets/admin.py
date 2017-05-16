from django.contrib import admin
from datetime import datetime

from .tasks import send_cancel_messages
from .models import Guest, GuestNameChange

class IsPrimaryFilter(admin.filters.SimpleListFilter):
    title = 'is primary'
    parameter_name = 'is_primary'

    def lookups(self, request, queryset):
        return (
            ('1', 'Primary'),
            ('0', 'Guest')
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(parent__isnull=True)
        elif self.value() == '0':
            return queryset.filter(parent__isnull=False)

        return queryset

class HasPaidFilter(admin.filters.SimpleListFilter):
    title = 'has paid'
    parameter_name = 'has_paid'

    def lookups(self, request, queryset):
        return (
            ('0', 'Not Paid'),
            ('1', 'Paid')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(paid__isnull=True)
        elif self.value() == '1':
            return queryset.filter(paid__isnull=False)
        return queryset

class GuestAdmin(admin.ModelAdmin):
    raw_id_fields=('owner', 'parent')
    search_fields=('first_name', 'last_name', 'owner__username')

    list_display = ('__str__', 'owner', 'category', 'has_paid', 'has_collected', 'has_checked_in', 'premium')
    list_filter = ('category', 'waiting', IsPrimaryFilter, 'payment_method', HasPaidFilter)

    ordering = ('id', )

    actions = ['mark_cancelled', 'mark_paid']
    def mark_cancelled(self, request, queryset):
        queryset_children = Guest.objects.filter(parent__in=queryset)
        time = datetime.now()

        queryset.update(cancelled=time)
        queryset_children.update(cancelled=time)

        count = queryset_children.count() + queryset.count()
        self.message_user(request, "%d ticket%s marked as cancelled." % (count, 's' if count > 1 else ''))

        # send cancel messages to all these people.
        send_cancel_messages.delay(time)

    def mark_paid(self, request, queryset):
        queryset.update(paid=datetime.now())

        count = queryset.count()
        self.message_user(request, "%d ticket%s marked as paid." % (count, 's' if count > 1 else ''))

class GuestNameChangeAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner', 'guest')

    list_display = ('__str__', 'owner', 'pending')
    list_filter = ('pending', )

    actions = ['mark_complete']
    def mark_complete(self, request, queryset):
        queryset.update(pending=False)
        for nc in queryset.iterator():
            nc.guest.first_name=nc.new_first_name
            nc.guest.last_name=nc.new_last_name
            nc.guest.save()
    mark_complete.short_description = 'Mark selected name changes as processed'

admin.site.register(Guest, GuestAdmin)
admin.site.register(GuestNameChange, GuestNameChangeAdmin)

