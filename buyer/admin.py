from django.contrib import admin
from .models import Buyer, WishList, Pincode


class BuyerAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_joined'
    list_display = ('first_name', 'last_name', 'email', 'username',
              'is_active', 'is_superuser', 'is_verified', 'is_staff')


admin.site.register(Buyer, BuyerAdmin)
admin.site.register(WishList)
admin.site.register(Pincode)

