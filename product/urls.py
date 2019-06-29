from django.urls import  path
from product.views import ProductDetailView

urlpatterns = [
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
]
