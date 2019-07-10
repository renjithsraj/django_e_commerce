from django.urls import  path
from django.contrib.auth.decorators import login_required
from product.views import ProductDetailView, WishlistView, AddProductCartView

urlpatterns = [
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('wish-list/',
         login_required(WishlistView.as_view()), name='wish-list'),
    path('add-product-cart/',
         AddProductCartView.as_view(), name='add-product-cart')


   


    
]
