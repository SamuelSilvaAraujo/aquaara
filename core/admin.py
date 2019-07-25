from django.contrib import admin

from .models import Property, Pond, Cycle, Population, Biometria, Cost, WaterQuality

admin.site.register(Property)
admin.site.register(Pond)
admin.site.register(Cycle)
admin.site.register(Population)
admin.site.register(Biometria)
admin.site.register(Cost)
admin.site.register(WaterQuality)