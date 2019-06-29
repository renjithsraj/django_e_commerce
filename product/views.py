from django.shortcuts import render
from django.views.generic.detail import DetailView
from product.models import Products
from product.utils import JSONResponseMixin

class ProductDetailView(JSONResponseMixin, DetailView):
    model = Products

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print ("the data is", self.object.price)



    

