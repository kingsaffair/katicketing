from django.contrib import admin
from .models import Guest

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


class GuestAdmin(admin.ModelAdmin):
	raw_id_fields=('owner', 'parent')
	search_fields=('first_name', 'last_name', 'owner__username')

	list_display = ('__str__', 'owner', 'category', '_hash')
	list_filter = ('category', 'waiting', IsPrimaryFilter, 'payment_method')

	ordering = ('id', )

admin.site.register(Guest, GuestAdmin)
