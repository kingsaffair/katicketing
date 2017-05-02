from django.contrib import admin
from .models import Guest

class GuestAdmin(admin.ModelAdmin):
	raw_id_fields=('owner', 'parent')

admin.site.register(Guest, GuestAdmin)
