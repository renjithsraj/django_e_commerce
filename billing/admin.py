from django.contrib import admin
from .models import ( CartItem, Cart, OrderItem, MyOrder, 
                        Invoice, Tax, ShippingAddress, Dispatched)
                        
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(MyOrder)
admin.site.register(Invoice)
admin.site.register(Tax)
admin.site.register(ShippingAddress)
admin.site.register(Dispatched)
