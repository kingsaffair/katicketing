from django.contrib import admin
from datetime import datetime

from .tasks import send_cancel_messages
from .models import Guest, GuestNameChange

class BaseIsNullFilter(admin.filters.SimpleListFilter):
    title = 'is null'
    parameter_name = 'is_null'

    positive_name = 'not null'
    negative_name = 'null'

    def lookups(self, request, queryset):
        return (
            ('1', self.positive_name),
            ('0', self.negative_name)
        )

    def queryset(self, request, queryset):
        kwargs = {
            self.parameter_name + '__isnull': self.value() == '1'
        }

        if self.value() in ('1', '0'):
            return queryset.filter(**kwargs)

        return queryset

def IsNullFilter(field, title_=None, pname=None, nname=None):
    class NullListFieldFilter(BaseIsNullFilter):
        parameter_name = field
        title = title_ or parameter_name

        positive_name = pname or 'not ' + parameter_name
        negative_name = nname or parameter_name
    return NullListFieldFilter

class GuestAdmin(admin.ModelAdmin):
    raw_id_fields=('owner', 'parent')
    search_fields=('first_name', 'last_name', 'owner__username')

    list_display = ('__str__', 'owner', 'category', 'has_paid', 'has_collected', 'has_checked_in', 'is_cancelled', 'premium')
    list_filter = ('category', 'waiting', IsNullFilter('parent', 'primary', 'primary', 'guest'), 'payment_method', IsNullFilter('paid'), IsNullFilter('cancelled'))

    ordering = ('id', )

    actions = ['mark_cancelled', 'mark_paid', 'mark_not_cancelled']
    def mark_cancelled(self, request, queryset):
        queryset_children = Guest.objects.filter(parent__in=queryset)
        count = queryset_children.count() + queryset.count()
        
        time = datetime.now()

        queryset.update(cancelled=time)
        queryset_children.update(cancelled=time)

        # send cancel messages to all these people (celery task).
        send_cancel_messages.delay(time)

        self.message_user(request, "%d ticket%s marked as cancelled." % (count, 's' if count > 1 else ''))

    def mark_not_cancelled(self, request, queryset):
        queryset_children = Guest.objects.filter(parent__in=queryset)
        count = queryset_children.count() + queryset.count()

        queryset.update(cancelled=None)
        queryset_children.update(cancelled=None)

        self.message_user(request, "%d ticket%s marked as not cancelled." % (count, 's' if count > 1 else ''))

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

