from django.urls import  path
from django.contrib.auth.decorators import login_required
from product.views import ProductDetailView, WishlistView

urlpatterns = [
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('wish-list/',
         WishlistView.as_view(), name='wish-list'),


    
]
