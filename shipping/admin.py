from django.contrib import admin
from .models import Zone, Country, ShippingRate


class CountryAdmin(admin.TabularInline):
    model = Country
    extra = 3


# class ZoneAdmin(admin.ModelAdmin):
# 	model = Zone
# 	inlines =(CountryAdmin,)
admin.site.register(Zone)
admin.site.register(Country)
admin.site.register(ShippingRate)
