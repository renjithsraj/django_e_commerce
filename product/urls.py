from django.urls import  path
from product.views import (
    ProductDetailView, WishlistView, AddProductCartView,
    ProductCategoryListView, checkout)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('wish-list/', login_required(WishlistView.as_view()), name='wish-list'),
    path('product-items-category/<slug:slug>',
         ProductCategoryListView.as_view(), name="products-category"),
    path('add-product-cart/',
         AddProductCartView.as_view(), name='add-product-cart'),
    path('checkout/', checkout, name='checkout')
]

