from django.contrib import admin

from .models import Property, Address, Pond, Cycle

admin.site.register(Property)
admin.site.register(Address)
admin.site.register(Pond)
admin.site.register(Cycle)
